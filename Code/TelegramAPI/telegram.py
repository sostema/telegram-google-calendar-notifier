import datetime

import pytz
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import Code.CalendarAPI.helpers
import Code.TelegramAPI.helpers
import Code.time_helpers
import Code.utils

config = None
logger = None


def main():
    global config, logger
    config = Code.utils.get_config()
    logger = Code.utils.setup_logger('telegram')

    token = config.get("credentials", "telegram_api_key")
    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher

    now_timetable_handler = CommandHandler('now', now_timetable)
    dispatcher.add_handler(now_timetable_handler)
    today_timetable_handler = CommandHandler('today', today_timetable)
    dispatcher.add_handler(today_timetable_handler)
    tomorrow_timetable_handler = CommandHandler('tomorrow', tomorrow_timetable)
    dispatcher.add_handler(tomorrow_timetable_handler)
    date_timetable_handler = CommandHandler('date', date_timetable)
    dispatcher.add_handler(date_timetable_handler)
    notify_handler = CommandHandler('notify', notify, pass_job_queue=True)
    dispatcher.add_handler(notify_handler)
    stop_notify_handler = CommandHandler('stop_notify', stop_notify, pass_job_queue=True)
    dispatcher.add_handler(stop_notify_handler)
    notify_button_handler = CallbackQueryHandler(notify_button, pass_job_queue=True)
    updater.dispatcher.add_handler(notify_button_handler)

    job_queue = updater.job_queue

    # Periodically save jobs
    job_queue.run_repeating(Code.TelegramAPI.helpers.save_jobs_job, datetime.timedelta(minutes=1))

    try:
        Code.TelegramAPI.helpers.load_jobs(job_queue)

    except FileNotFoundError:
        # First run
        pass

    updater.start_polling()
    updater.idle()

    Code.TelegramAPI.helpers.save_jobs(job_queue)


def send_timetable(context, date, chat_id):
    calendar = Code.CalendarAPI.helpers.setup_calendar_from_config(config)
    events = calendar.get_events(date.datetime_begin, date.datetime_end)
    text = date.__str__() + '\n'
    if events:
        text += "Расписание: \n\n"
        for event in events:
            text += event.__str__() + '\n'
    else:
        text += "Ура! Пар нет."

    msg_id = None
    try:
        message = context.bot.send_message(chat_id=chat_id, text=text)
        msg_id = message.message_id
    except Exception as e:
        pass
    try:
        context.bot.pinChatMessage(chat_id=chat_id, message_id=msg_id)
    except Exception as e:
        pass


def date_timetable(update, context):
    if context.args:
        date_str = context.args[0]
        try:
            date = Code.time_helpers.Date().parse_datetime(date_str)
        except Exception as e:
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,
                                     text="Неправильно введена дата! Должен быть формат YYYY/MM/DD или MM/DD")
            pass
        else:
            send_timetable(context, date, update.message.chat_id)
    else:
        date = Code.time_helpers.Date(full_day=True)
        send_timetable(context, date, update.message.chat_id)


def now_timetable(update, context):
    date = Code.time_helpers.Date(datetime.datetime.now(), False)
    send_timetable(context, date, update.message.chat_id)


def today_timetable(update, context):
    date = Code.time_helpers.Date(datetime.datetime.today(), True)
    send_timetable(context, date, update.message.chat_id)


def tomorrow_timetable(update, context):
    date = Code.time_helpers.Date(datetime.datetime.today() + datetime.timedelta(1), True)
    send_timetable(context, date, update.message.chat_id)


def callback_notify_today(context):
    date = Code.time_helpers.Date(datetime.datetime.today(), True)
    send_timetable(context, date, context.job.context)


def callback_notify_tomorrow(context):
    date = Code.time_helpers.Date(datetime.datetime.today() + datetime.timedelta(1), True)
    send_timetable(context, date, context.job.context)


def notify(update, context):
    if context.args:
        try:
            delay = datetime.datetime.strptime(context.args[0], "%H:%M").replace(year=datetime.datetime.today().year,
                                                                                 month=datetime.datetime.today().month,
                                                                                 day=datetime.datetime.today().day)
            delay = Code.time_helpers.local_timezone.localize(delay)
            logger.debug(delay)
        except Exception as e:
            pass
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,
                                     text="Неправильно введено время! Должен быть формат hh:mm")
            return
    else:
        delay = datetime.datetime.today()
        delay = datetime.datetime(delay.year, delay.month, delay.day, hour=21, minute=0, second=0, microsecond=0,
                                  tzinfo=None)
        delay = Code.time_helpers.local_timezone.localize(delay)
        logger.debug(delay)

    for job in context.job_queue.get_jobs_by_name(f"{update.message.chat_id}"):
        job.schedule_removal()

    delay = delay.astimezone(pytz.utc)

    keyboard = [[InlineKeyboardButton("Сегодня", callback_data=f"{delay.strftime('%H:%M')}_1"),
                 InlineKeyboardButton("Завтра", callback_data=f"{delay.strftime('%H:%M')}_2")],
                [InlineKeyboardButton("Сегодня и завтра", callback_data=f"{delay.strftime('%H:%M')}_3")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"Выберите вид расписания: ", reply_markup=reply_markup)


def notify_button(update, context):
    query = update.callback_query
    data = query.data.split('_')
    date = datetime.datetime.strptime(data[0], "%H:%M")
    time = date.time()
    result = data[1]
    if result == '1':
        context.job_queue.run_daily(callback_notify_today, time, context=query.message.chat_id,
                                    name=f"{query.message.chat_id}")
        result_text = "сегодня"
    elif result == '2':
        context.job_queue.run_daily(callback_notify_tomorrow, time, context=query.message.chat_id,
                                    name=f"{query.message.chat_id}")
        result_text = "завтра"
    else:
        context.job_queue.run_daily(callback_notify_today, time, context=query.message.chat_id,
                                    name=f"{query.message.chat_id}")
        context.job_queue.run_daily(callback_notify_tomorrow, time, context=query.message.chat_id,
                                    name=f"{query.message.chat_id}")
        result_text = "сегодня и завтра"
    date = datetime.datetime.strptime(data[0], "%H:%M").replace(year=datetime.datetime.today().year,
                                                                month=datetime.datetime.today().month,
                                                                day=datetime.datetime.today().day)
    date = (pytz.utc.localize(date)).astimezone(Code.time_helpers.local_timezone)
    query.edit_message_text(
        text=f"На том и решили! В {date.strftime('%H:%M:%Z')} вы будете получать расписание на {result_text}!")


def stop_notify(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,
                             text=f"Хорошо! Больше не будем оповещать!")

    for job in context.job_queue.get_jobs_by_name(f"{update.message.chat_id}"):
        job.schedule_removal()


if __name__ == "__main__":
    main()

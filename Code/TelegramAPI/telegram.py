import datetime

from telegram.ext import Updater, CommandHandler

import Code.CalendarAPI.helpers
import Code.time_helpers
import Code.utils

config = None
logger = None


def main():
    import logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

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

    updater.start_polling()


def send_timetable(update, context, calendar, date):
    events = calendar.get_events(date.datetime_begin, date.datetime_end)
    logger.debug(events)
    text = date.__str__() + '\n'
    if events:
        text += "Расписание: \n\n"
        for event in events:
            text += event.__str__() + '\n'
    else:
        text += "Ура! Пар нет."

    msg_id = None
    try:
        message = context.bot.send_message(chat_id=update.message.chat_id, text=text)
        msg_id = message.message_id
    except Exception as e:
        logger.debug(e)
    try:
        context.bot.pinChatMessage(chat_id=update.message.chat_id, message_id=msg_id)
    except Exception as e:
        logger.debug(e)


def date_timetable(update, context):
    calendar = Code.CalendarAPI.helpers.setup_calendar_from_config(config)
    if context.args:
        date_str = context.args[0]
        try:
            date = Code.time_helpers.Date().parse_datetime(date_str)
        except Exception as e:
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,
                                     text="Неправильно введена дата! Должен быть формат YYYY/MM/DD или MM/DD")
            logger.debug(e)
        else:
            send_timetable(update, context, calendar, date)
    else:
        date = Code.time_helpers.Date(full_day=True)
        send_timetable(update, context, calendar, date)


def now_timetable(update, context):
    calendar = Code.CalendarAPI.helpers.setup_calendar_from_config(config)
    date = Code.time_helpers.Date()
    send_timetable(update, context, calendar, date)


def today_timetable(update, context):
    calendar = Code.CalendarAPI.helpers.setup_calendar_from_config(config)
    date = Code.time_helpers.Date(datetime.datetime.today(), True)
    send_timetable(update, context, calendar, date)


def tomorrow_timetable(update, context):
    calendar = Code.CalendarAPI.helpers.setup_calendar_from_config(config)
    date = Code.time_helpers.Date(datetime.datetime.today() + datetime.timedelta(1), True)
    send_timetable(update, context, calendar, date)


if __name__ == "__main__":
    main()

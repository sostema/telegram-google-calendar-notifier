import logging

from telegram.ext import Updater, CommandHandler

from Code.calendar import get_parsed_events, get_date_events
from Code.time_helpers import *
from Code.utils import config


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, )

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


def send_timetable(update, context, date):
    events = get_date_events(date)
    parsed_events = get_parsed_events(events)
    if parsed_events:
        text = get_date_string(date) + "\n" + "Расписание:\n\n" + parsed_events
    else:
        text = get_date_string(date) + "\n" + "Ура! Пар нет."
    msg_id = None
    try:
        message = context.bot.send_message(chat_id=update.message.chat_id, text=text)
        msg_id = message.message_id
    except Exception as e:
        logging.debug(e)
    try:
        context.bot.pinChatMessage(chat_id=update.message.chat_id, message_id=msg_id)
    except Exception as e:
        logging.debug(e)


def date_timetable(update, context):
    if not context.args:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,
                                 text="Неправильно введена дата! Должен быть формат YYYY/MM/DD")
        return
    try:
        date = get_datetime_from_string(context.args[0])
    except Exception as e:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,
                                 text="Неправильно введена дата! Должен быть формат YYYY/MM/DD")
        logger.debug(e)
    else:
        send_timetable(update, context, date)


def now_timetable(update, context):
    date = get_now_date()
    send_timetable(update, context, date)


def today_timetable(update, context):
    date = get_today_date()
    send_timetable(update, context, date)


def tomorrow_timetable(update, context):
    date = get_tomorrow_date()
    send_timetable(update, context, date)


if __name__ == "__main__":
    main()

import logging

from telegram.ext import Updater, CommandHandler

from Code.calendar import *
from Code.utils import config


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, )

    token = config.get("credentials", "telegram_api_key")
    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher

    today_timetable_handler = CommandHandler('today', today_timetable)
    dispatcher.add_handler(today_timetable_handler)
    tomorrow_timetable_handler = CommandHandler('tomorrow', tomorrow_timetable)
    dispatcher.add_handler(tomorrow_timetable_handler)

    updater.start_polling()


def today_timetable(update, context):
    text = get_date() + "\n" + "Расписание:\n\n" + get_today_parsed_events()
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


def tomorrow_timetable(update, context):
    text = get_date() + "\n" + "Расписание:\n\n" + get_today_parsed_events()
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


if __name__ == "__main__":
    main()

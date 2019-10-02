import telebot
from Code.utils import get_config, get_date
import schedule
from Code.calendar import get_today_parsed_events

config = get_config()
api_key = config.get("credentials", "telegram_api_key")

bot = telebot.TeleBot(api_key)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    text = get_date() + "\n" + "Текущее расписание:\n\n" + get_today_parsed_events()
    sent_message = send_message(bot, message.chat.id, text)
    try:
        bot.pin_chat_message(sent_message.chat.id, sent_message.message_id)
    except Exception as e:
        print(e)


def send_message(bot: telebot.TeleBot, chat_id, msg):
    sent_message = bot.send_message(chat_id, msg)
    return sent_message


def start():
    bot.polling(none_stop=True)


def stop():
    bot.stop_bot()
import telebot
import time
bot = telebot.TeleBot('7427442280:AAGTi4xAjbIsuoB0Gag2-Fjcv8PcnOrEtDc')
@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):
    if message.text == "/start":
        while True:
            bot.send_message(message.from_user.id,"Ссылка на покупку билетов," "https://tickets.lakhta.events/event/23FA307410B1F9BE84842D1ABE30D6AB48EA2CF8/2025-03-21")
            time.sleep(60)
    elif message.text == "/stop":
        bot.stop_bot()
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Не могу тебе помочь)")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)


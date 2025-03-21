import json
import requests
import telebot
import time

need_date = '21.03.2025'
need_date = None

def load_available_times():
    url = 'https://tickets.lakhta.events/api/no-scheme'
    request_body = {'hash': '23FA307410B1F9BE84842D1ABE30D6AB48EA2CF8'}
    req = requests.post(url, json = request_body)
    response = req.text
    data = json.loads(response)
    calendar = (data["response"]["calendar"])
    results = []
    for item in calendar:
#        if (need_date is not None) and (need_date != item['day']):
#            continue
        for schedule in item['_time']:
            if int(schedule['quantity']) > 0:
                free_time = {'date': item['day'], 'time': schedule['time'], 'quantity': schedule['quantity']}
                results.append(free_time)
    return results

bot = telebot.TeleBot('7427442280:AAGTi4xAjbIsuoB0Gag2-Fjcv8PcnOrEtDc')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        while True:
            results = load_available_times()
            if len(results) > 0:
                for available_time in results:
                    url = 'https://tickets.lakhta.events/event/23FA307410B1F9BE84842D1ABE30D6AB48EA2CF8'
                    url += '/' + available_time['date']
                    url += '/' + available_time['time']
                    print(url)
                    bot.send_message(
                        message.from_user.id,
                        'Ссылка на покупку билетов на ' + available_time['date'] + ' ' + available_time['time'] + " " + url
                    )
            time.sleep(60)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Не могу тебе помочь)")

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)
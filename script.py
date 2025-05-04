import json
import sys

import requests
import telebot
from telebot import types
import time
import datetime as dt

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
        if (need_date is not None) and (need_date != item['day']):
            continue
        for schedule in item['_time']:
            if int(schedule['quantity']) == 0:
                free_time = {'date': item['day'], 'time': schedule['time'], 'quantity': schedule['quantity']}
                results.append(free_time)
    return results


bot = telebot.TeleBot('7427442280:AAGTi4xAjbIsuoB0Gag2-Fjcv8PcnOrEtDc')
@bot.message_handler(commands=['start'])
def start(message):
    global stop_bot
    stop_bot = True
    results = load_available_times()
    if len(results) > 0:
        for available_time in results:
            if stop_bot == False:
                break
            url = 'https://tickets.lakhta.events/event/23FA307410B1F9BE84842D1ABE30D6AB48EA2CF8'
            url += '/' + dt.datetime.strptime(available_time['date'], "%d.%m.%Y").strftime("%Y-%m-%d")
            url += '/' + available_time['time']
            print(url)
            bot.send_message(message.from_user.id, 'Ссылка на покупку билетов на ' + available_time['date'] + ' ' + available_time['time'] + " " + url)
            time.sleep(1)

@bot.message_handler(commands=['stop'])
def stop_message(message):
    global stop_bot
    stop_bot = False
    bot.send_message(message.chat.id, 'Бот остановлен!')
@bot.message_handler(commands=['info'])
def info(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт Лахта центр", url='https://lakhta.center/')
    markup.add(button1)
    button2 = types.InlineKeyboardButton("Мой ютуб", url='https://youtube.com/@l3sha1337?si=PoAdsN4k3DtORM--')
    markup.add(button2)
    bot.send_message(message.chat.id,"Привет, тут ссылки на сайт с котрым я роботаю и на мой ютуб".format(message.from_user),reply_markup=markup)

bot.polling(none_stop=True, interval=0)

import json

import requests
import telebot
from telebot import types
import time
import datetime as dt

required_date = '24.05.2025'
required_quantity = 2
required_time = '10:30'
bot_started = False


def load_available_times():
    global required_time, required_quantity, required_date

    url = 'https://tickets.lakhta.events/api/no-scheme'
    request_body = {'hash': '23FA307410B1F9BE84842D1ABE30D6AB48EA2CF8'}
    req = requests.post(url, json = request_body)
    response = req.text
    data = json.loads(response)
    calendar = (data["response"]["calendar"])
    results = []
    for item in calendar:
        if (required_date is not None) and (required_date != item['day']):
            continue
        for schedule in item['_time']:
            if (required_quantity is not None) and (int(schedule['quantity']) < int(required_quantity)):
                continue
            if (required_time is not None) and (required_time != schedule['time']):
                continue
            free_time = {'date': item['day'], 'time': schedule['time'], 'quantity': schedule['quantity']}
            results.append(free_time)
    return results

bot = telebot.TeleBot('7997374049:AAG4F4reje3Bn_xBivGAaChc9kkymJErEAU')


@bot.message_handler(commands=['start'])
def start(message):
    global bot_started
    bot_started = True
    info_message = 'Вы подписались на информацию о билетах на дату: ' + required_date
    if required_time:
        info_message += ', время: ' + required_time
    if required_quantity:
        info_message += ', количество билетов: ' + str(required_quantity)
    bot.send_message(message.from_user.id, info_message)
    results = load_available_times()
    if len(results) > 0:
        for available_time in results:
            if not bot_started:
                break
            url = 'https://tickets.lakhta.events/event/23FA307410B1F9BE84842D1ABE30D6AB48EA2CF8'
            url += '/' + dt.datetime.strptime(available_time['date'], "%d.%m.%Y").strftime("%Y-%m-%d")
            url += '/' + available_time['time']
            print(url)
            bot.send_message(
                message.from_user.id,
                'Ссылка на покупку билетов на ' + available_time['date']
                + ' ' + available_time['time']
                + ' свободных билетов: ' + available_time['quantity']
                + " " + url
            )
    time.sleep(60)


@bot.message_handler(commands=['stop'])
def stop_message(message):
    global bot_started
    if bot_started:
        bot_started = False
        bot.send_message(message.chat.id, 'Вы отписалить от рассылки о билетах!')
    else:
        bot.send_message(message.chat.id, 'Вы не были подписаны на рассылку!')

@bot.message_handler(commands=['info'])
@bot.message_handler()
def info(message):
    button1 = types.InlineKeyboardButton("Сайт Лахта центр", url='https://lakhta.center/')
    button2 = types.InlineKeyboardButton("Мой ютуб", url='https://youtube.com/@l3sha1337?si=PoAdsN4k3DtORM--')

    markup = types.InlineKeyboardMarkup()
    markup.add(button1)
    markup.add(button2)
    bot.send_message(
        message.chat.id,
        'Привет, тут ссылки на сайт, с котрым я роботаю и на мой ютуб'.format(message.from_user),
        reply_markup=markup
    )

bot.polling(none_stop=True, interval=0)

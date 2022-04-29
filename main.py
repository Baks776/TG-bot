import requests
from datetime import datetime
import telebot
from congig import token



def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_messenage(message):
        hi_user = f'<b>Привет,{message.from_user.first_name}</b>\n' \
                  f'Напиши в чат\n' \
                  f'- BTC и ввыведу тебе на данный моемнт курс биткоина\n' \
                  f'- USD и получишь курс доллара'
        bot.send_message(message.chat.id,hi_user,parse_mode='html')


    @bot.message_handler(content_types=['text'])
    def send_txt(message):
        if message.text.lower() == 'btc':
            req_rur = requests.get("https://yobit.net/api/3/ticker/btc_rur")
            req_usd = requests.get("https://yobit.net/api/3/ticker/btc_usd")
            responce_rur = req_rur.json()
            responce_usd = req_usd.json()
            sell_price_rur = responce_rur['btc_rur']['sell']
            sell_price_usd = responce_usd['btc_usd']['sell']
            bot.send_message(message.chat.id,
            f'{datetime.now().strftime("%Y-%m-%d %H:%M")} \nBTC Sell:\n'
            f'Dollar - {sell_price_usd}\U0001F4B0\n'
            f'Rub - {sell_price_rur}\U0001F333')
        elif message.text.lower() == 'usd':
                data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
                bot.send_message(message.chat.id,"{}\nКурс\U0001F4B0 \n{}".format(datetime.now().strftime("%Y-%m-%d %H:%M"),data['Valute']['USD']['Value']))
                #bot.send_message(message.chat.id, f'Такую валюта я не знаю')
        else:
            bot.send_message(message.chat.id,"None command,I dodn't know this")

    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

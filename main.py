import telebot
from config import TOKEN, keys
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def first_command(message):
    text = ('чтобы начать работу введите команду боту в следующем формате:\n'
            '<имя валюты> \n'
            '<имя валюты, в которой надо узнать цену первой валюты> \n'
            '<количество переводимой валюты> \n'
            'увидеть список всех доступных валют:  /value ')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['value'])
def value(message):
    text = 'доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def conversion(message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров')
        if len(values) <= 2:
            raise APIException('Слишком мало параметров')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользоватeля:\n      {e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду:\n        {e}')

    else:
        text = f'Цена {amount} {base} в {quote} - {round(total_base, 5)}'
        bot.send_message(message.chat.id, text)


bot.polling()

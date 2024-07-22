import telebot
from config import keys, TOKEN
from extensions import ApiException, CriptoConverter


bot = telebot.TeleBot(TOKEN)    #создаем объект бота


@bot.message_handler(commands=['start', 'help'])    #обработчик который выводит инструкцию по работе с ботом по комадам /start и /help
def help(message: telebot.types.Message):
    text = (" Чтобы начать работу введите команду боту в следующем формате, через пробел:\n\
<имя валюты, цену которой вы хотите узнать> <имя валюты в которую вы хотите перевести> <количество переводимой валюты>"
 "\nЧтобы увидеть список всех доступных валют для конвертирования введите команду: /values")
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])    #обработчик который выводит перечень доступных валют по команде /values
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертирования:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])    #основной обработчик запроса стоимости валют
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ApiException('Слишком много параметров.\n Для успешной конвертации требуется ввести три параметра.')
        if len(values) < 3:
            raise ApiException('Мало параметров. \n Для успешной конвертации требуется ввести три параметра.')

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except ApiException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()


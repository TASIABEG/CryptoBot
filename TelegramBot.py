import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Прошу введите следующую информацию <имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> " \
           "<количество первой валюты> \n \nДля того чтобы увидеть список всех доступных валют введите: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(massage: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text,key, ))
    bot.reply_to(massage, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Слишком много или мало параметров.")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        if amount != 1:
            text = f"Цена {amount} {quote} в {base} - {float(total_base)*float(amount)}"
            bot.send_message(message.chat.id, text)
        else:
            text = f"Цена {amount} {quote} в {base} - {total_base}"
            bot.send_message(message.chat.id, text)


bot.polling()
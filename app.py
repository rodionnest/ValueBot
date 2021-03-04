import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValueConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите боту команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести><количество переводимой валюты>\n/values - увидеть список доступных валют: '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def start(message: telebot.types.Message):
    text = 'Доступные валюты:\n\n'
    text += '\n'.join(f"{i+1}. {key}" for i, key in enumerate(keys.keys()))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        values = list(map(str.lower, values))

        if len(values) != 3:
            raise ConvertionException('Неправильное количество параметров')

        quote, base, amount = values
        total_base = ValueConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{quote} количеством {amount} -- {float(total_base)*float(amount):.2f} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()

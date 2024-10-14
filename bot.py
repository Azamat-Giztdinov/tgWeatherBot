import telebot
from dotenv import load_dotenv
import os
import requests
import logging


logging.basicConfig(level=logging.INFO)


load_dotenv()
bot = telebot.TeleBot(os.getenv('TELEGRAM_API_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello dear friend! I'm a bot that will show you the weather!\nLet's start! Send the city whose weather you want to know")


@bot.message_handler(func=lambda message: not message.text.startswith('/'))
def city(message):
    city = message.text
    try:
        m = bot.send_message(message.chat.id, "Please wait, I'm looking for information")
        res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPENWEATHERMAP_API')}')
        data = res.json()
        if str(data['cod']) == '404':
            rewrite(message, m.message_id, 'City not found. Try another city.')
        elif str(data['cod']) == '200':
            weather = int(data['main']['temp'] - 273.15)
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            rewrite(message, m.message_id, f'Weather in {data['name']}: \ntemperature {weather}°C\nhumidity {humidity}%\n{description}.')
        else:            
            rewrite(message , m.message_id,'Oops, sorry, the bot is temporarily down')
    except Exception as e:
        logging.error(e)
        rewrite(message, m.message_id, 'Oops, sorry, the bot is temporarily down')


@bot.message_handler(func=lambda message: message.text.startswith('/'))
def not_command(message):
    bot.send_message(message.chat.id, 'Sorry, commands are not supported here. Please send a valid city name.')


def rewrite(message, message_id, text):
    return bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,  
                            text=text, parse_mode="Markdown")


if __name__ == '__main__':
    bot.polling()


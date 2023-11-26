
import time
import requests
from bs4 import BeautifulSoup
import telebot
import random
from telebot import types



telegram_token = 'токен'  # Токен вашего телеграм-бота
bot = telebot.TeleBot(telegram_token)
        
url = ''  # Ссылка которую можно задать через бота

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Начать")
    button2 = types.KeyboardButton("Задать ссылку")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, 
                   text="Привет, {0.first_name}! Нажми 'Начать', чтобы отслеживать форму.".format(message.from_user), reply_markup=markup)


    

@bot.message_handler(content_types=['text'])
def parser_form(message):
    
    global url
    
    count = 0
    if(message.text == "Начать"):
        bot.send_message(message.chat.id, text="Начал отслеживать форму.")
    
        while True:
            interval = random.randint(5, 10)
            response = requests.get(url)
            bs = BeautifulSoup(response.text, "lxml")
            soup = bs.find(class_="UatU5d")
            elem_soup = BeautifulSoup(str(soup), 'html.parser')
            elem_soup = elem_soup.text
            
            if soup and count == 0:
                bot.send_message(message.chat.id, text=elem_soup)
                count = 1
                time.sleep(interval)
                continue
            if soup and count == 1:
                continue
            else:
                bot.send_message(message.chat.id, text="Ссылка формы изменила свой статус. Проверь ссылку{0}".format(url))
                count = 0
                time.sleep(interval)
                break
    if (message.text == "Задать ссылку"):
        text_bot = bot.send_message(message.chat.id, text="Скопируй ссылку и отправь мне.")
        bot.register_next_step_handler(text_bot, returning)

@bot.message_handler(commands=['return'])
def returning(message):
    global url
    url = message.text


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)  
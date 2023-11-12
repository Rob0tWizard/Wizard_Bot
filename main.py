import telebot
import webbrowser
from telebot import types

bot = telebot.TeleBot('6530655301:********')

name = ''
age = 0


# @bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['start'])
def main(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Привет! Как тебя зовут? ')  # , parse_mode=True )
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')
        # Он принимает айди чата и текст
        #       #третий аргумет, позволяет вкл HTTP


def get_age(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_loop_age)


def get_loop_age(message):
    global age
    if age == 0:
        try:
            age = int(message.text)
        except ValueError:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
            bot.send_message(message.from_user.id, 'Сколько тебе лет?')
            bot.register_next_step_handler(message, get_loop_age)
            return
    else:
        age = int(message.text)

    # bot.send_message(message.from_user.id, f'Тебе {str(age)} лет, и тебя зовут {name}?')
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Тебе {str(age)} лет, и тебя зовут {name}?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню, тебе пизда')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Давай сначала, напиши /start')


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'Бот не сильно функционален, рабочие команды: /start, /site')


@bot.message_handler(commands=['site', 'web'])
def site():
    webbrowser.open(
        'https://www.google.com/search?q=rick+roll&oq=rick+roll&aqs=chrome..69i57.1964j0j1&sourceid=chrome&ie=UTF-8#fpstate=ive&vld=cid:dd379760,vid:eBGIQ7ZuuiU')


bot.polling(none_stop=True)
# запрашивает ответы от бота по сообщ

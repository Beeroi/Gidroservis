import os
import telebot
import logging
from flask import Flask, request
#import sqlite3
from telebot import types
from config import *

bot=telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    #bot.send_message(message.chat.id, message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    name = f'Здравствуйте, {message.from_user.first_name}, что вас интересует?'
    btn_remont = types.KeyboardButton("Ремонт спецтехники")
    btn_magaz = types.KeyboardButton("Магазин запчастей")
    markup.add(btn_remont, btn_magaz)
    bot.send_message(message.chat.id, name, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "Магазин запчастей":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_salnik = types.KeyboardButton("Сальник")
        btn_manjet = types.KeyboardButton("Манжет")
        markup.add(btn_salnik, btn_manjet)
        bot.send_message(message.chat.id, 'Выберете деталь', reply_markup=markup)
    elif message.text == "Ремонт спецтехники":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_gidromotor = types.KeyboardButton("Гидромотор")
        btn_gidrocilindr = types.KeyboardButton("Гидроцилиндр")
        btn_dvigatel = types.KeyboardButton("Дизельный двигатель")
        btn_kovsh = types.KeyboardButton("Ковш")
        btn_shtok = types.KeyboardButton("Шток")
        btn_raspred = types.KeyboardButton("Гидрораспределитель")
        markup.add(btn_gidromotor, btn_gidrocilindr, btn_dvigatel, btn_kovsh, btn_shtok, btn_raspred)
        bot.send_message(message.chat.id, 'Что вы хотите отремонтировать?', reply_markup=markup)
    elif message.text == "Гидромотор" or message.text == "Гидроцилиндр" or message.text == "Дизельный двигатель" or message.text == "Ковш" or message.text == "Шток" or message.text == "Гидрораспределитель" or message.text == "Сальник" or message.text == "Манжет":
        Info = message.text
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text='Отправить номер', request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, 'Нажмите "Отправить номер". Мы позвоним и проконсультируем вас', reply_markup=keyboard)
        @bot.message_handler(content_types=['contact'])
        def contact(message):
            if message.contact is not None:
                bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
                bot.send_message(TO_CHAT_ID, Info)
                bot.send_message(message.chat.id, 'Заявка принята. Очень скоро мы позвоним вам. \n Если вам нужно что-то ещё, нажмите /start', reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так... \n Нажмите /start и начните сначала')
bot.polling(none_stop=True)
import logging
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder

def keyboards_start():
    logging.info("keyboards_superadmin")
    button_1 = KeyboardButton(text='Опрос')
    button_2 = KeyboardButton(text='Рекомендации')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2]],
        resize_keyboard=True
    )
    return keyboard


def keyboards_question1():
    logging.info(f'keyboards_question1')
    button_1 = InlineKeyboardButton(text='А) Да', callback_data='question1_1A')
    button_2 = InlineKeyboardButton(text='Б) Нет', callback_data='question1_1B')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]],)
    return keyboard


def keyboards_question2():
    logging.info(f'keyboards_question2')
    button_1 = InlineKeyboardButton(text='А) Да', callback_data='question2_2A')
    button_2 = InlineKeyboardButton(text='Б) Нет', callback_data='question2_2B')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]],)
    return keyboard


def keyboards_question3():
    logging.info(f'keyboards_question3')
    button_1 = InlineKeyboardButton(text='А) полная тишина', callback_data='question3_3A')
    button_2 = InlineKeyboardButton(text='Б) негромкие звуки (белый шум, негромкая музыка)', callback_data='question3_3B')
    button_3 = InlineKeyboardButton(text='В) совсем не громко', callback_data='question3_3C')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3]],)
    return keyboard


def keyboards_question4():
    logging.info(f'keyboards_question4')
    button_1 = InlineKeyboardButton(text='А) Да', callback_data='question4_4A')
    button_2 = InlineKeyboardButton(text='Б) Нет', callback_data='question4_4B')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]],)
    return keyboard


def keyboards_recomendation():
    logging.info(f'keyboards_recomendation')
    button_1 = InlineKeyboardButton(text='правило 1 «режим сна»', callback_data='recomendation_1')
    button_2 = InlineKeyboardButton(text='правило 2 «физическая активность', callback_data='recomendation_2')
    button_3 = InlineKeyboardButton(text='правило 3 «питание»', callback_data='recomendation_3')
    button_4 = InlineKeyboardButton(text='правило 4 «гигиена спального места»', callback_data='recomendation_4')
    button_5 = InlineKeyboardButton(text='правило 5 «температура в спальне»', callback_data='recomendation_5')
    button_6 = InlineKeyboardButton(text='правило 6 «воздух»', callback_data='recomendation_6')
    button_7 = InlineKeyboardButton(text='правило 7 «освещение»', callback_data='recomendation_7')
    button_8 = InlineKeyboardButton(text='правило 8 «звуки»', callback_data='recomendation_8')
    button_9 = InlineKeyboardButton(text='правило 9 «мелатонин или во сколько засыпаете»', callback_data='recomendation_9')
    button_10 = InlineKeyboardButton(text='правило 10 «на чем вы спите»', callback_data='recomendation_10')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5],
                                                     [button_6], [button_7], [button_8], [button_9], [button_10]],)
    return keyboard
from telebot import types

# ВОРКЕР БОТ

def ban_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('Вы заблокированы')

    markup.add(btn1)
    return markup    
 
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('💁🏻‍♀️ Мой профиль')
    btn2 = types.KeyboardButton('🥀 Панель воркера')
    btn3 = types.KeyboardButton('О проекте')
    btn4 = types.KeyboardButton('Другое')

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('💁🏻‍♀️ Мой профиль')
    btn2 = types.KeyboardButton('🥀 Панель воркера')
    btn3 = types.KeyboardButton('О проекте')
    btn4 = types.KeyboardButton('Другое')
    btn5 = types.KeyboardButton('Админ. панель')

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    return markup


def panel_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('Оплата (ручка)')
    btn3 = types.KeyboardButton('Изменить чат')

    btn2 = types.KeyboardButton('Добавить саппорта')
    btn4 = types.KeyboardButton('Удалить саппорта')

    btn5 = types.KeyboardButton('Состояние казино')
    btn6 = types.KeyboardButton('Мой кошелек')
    btn7 = types.KeyboardButton('Назад')

    markup.add(btn1, btn3)
    markup.add(btn2, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)
    return markup


def other_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('Отрисовка')
    btn3 = types.KeyboardButton('Скрины')

    btn6 = types.KeyboardButton('Назад')

    markup.add(btn1, btn3)
    markup.add(btn6)
    return markup 


def pillow_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('Qiwi баланс')
    btn3 = types.KeyboardButton('Qiwi перевод')
    btn4 = types.KeyboardButton('Qiwi получение (ПК)')

    btn4 = types.KeyboardButton('Баланс Сбербанк')
    btn5 = types.KeyboardButton('Баланс ЮMoney')

    btn6 = types.KeyboardButton('Назад')

    markup.add(btn1, btn3)
    markup.add(btn4)

    markup.add(btn4, btn5)

    markup.add(btn6)
    return markup


# КАЗИНО БОТ


def casino_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('Играть')
    btn2 = types.KeyboardButton('Тех. поддержка')
    btn3 = types.KeyboardButton('Личный кабинет')

    markup.add(btn1)
    markup.add(btn2, btn3)
    return markup


def game_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('Казино')
    btn2 = types.KeyboardButton('Орел & Решка')
    btn3 = types.KeyboardButton('Краш')
    btn4 = types.KeyboardButton('Назад')

    markup.row(btn1, btn2, btn3)
    markup.add(btn4)
    return markup

def endgame_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn4 = types.KeyboardButton('Завершить игру')

    markup.add(btn4)
    return markup    

def deposit_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn4 = types.KeyboardButton('Отменить пополнение')

    markup.add(btn4)
    return markup  

# Орел и Решка
def coinflip_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('Орел')
    btn2 = types.KeyboardButton('Решка')

    markup.row(btn1, btn2)
    return markup


# Нвути
def nvuti_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)

    btn1 = types.KeyboardButton('< 50')
    btn2 = types.KeyboardButton('= 50')
    btn3 = types.KeyboardButton('> 50')

    markup.row(btn1, btn2, btn3)
    return markup

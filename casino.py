import casino_config, configparser, threading, worker
from casino_config import (bot, types, db, keyboard, support)
from casino_config import (status_deposit, cancel_deposit, casino_deposit, set_nickname, set_code, new_referal, casino_receive, casino_promo, coinflip, crash, crash_start, nvuti, float_2f)

@bot.message_handler(commands=['start'])  
def start_command(message):
	try:

		chat_id = message.chat.id
		start = message.text.split()

		if not db.user_exists_casino(chat_id):

			if len(start) == 2:
				exists = db.workers_exists_code(start[1])

				if exists is not False:

					db.user_add_casino(chat_id, 'Скрыт', start[1])
					set_nickname(message)

					bot.send_message(chat_id, f"Добро пожаловать, <b>{message.from_user.first_name}</b>\nУ нас очень большой выбор вида игр, которые подойдут для каждого пользователя",
						parse_mode="html", reply_markup = keyboard.casino_keyboard())

					new_referal(message)
				else:
					db.user_add_casino(chat_id, 'Скрыт', 0)
					set_nickname(message)

					message = bot.send_message(chat_id, f"⚠️ Введите <b>правильный код</b> пригласившего вас человека", parse_mode="html")
					bot.register_next_step_handler(message, set_code)
			else:
				db.user_add_casino(chat_id, 'Скрыт', 0)
				set_nickname(message)

				message = bot.send_message(chat_id, f"Для начала <b>введите код</b> пригласившего вас человека", parse_mode="html")
				bot.register_next_step_handler(message, set_code)
		else:

			code = db.casino_code(chat_id)

			if code == 0:
				message = bot.send_message(chat_id, f"Для начала <b>введите</b> 589016", parse_mode="html")
				bot.register_next_step_handler(message, set_code)
			else:
				bot.send_message(chat_id, f"Добро пожаловать, <b>{message.from_user.first_name}</b>\nУ нас очень большой выбор вида игр, которые подойдут для каждого пользователя",
					parse_mode="html", reply_markup = keyboard.casino_keyboard())

	except Exception as e:
		print(e)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	try:

		chat_id = message.chat.id

		config = configparser.ConfigParser()
		config.read("default.ini")
		status = config['Telegram']['messages']

		if status == '1':
			

			if message.text == 'Личный кабинет':
				balance = float_2f(db.casino_balance(chat_id))
				win = db.casino_win(chat_id)
				lose = db.casino_lose(chat_id)
				deposit = db.casino_deposit(chat_id)
				receive = db.casino_receive(chat_id)
				All = win + lose

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
				inline_1 = types.InlineKeyboardButton(text = "Пополнить", callback_data = 'DEPOSIT')
				inline_2 = types.InlineKeyboardButton(text = "Вывести", callback_data = 'RECEIVE')
				inline_3 = types.InlineKeyboardButton(text = "Промокод", callback_data = 'PROMO')
				inline_4 = types.InlineKeyboardButton(text = "Обнулить", callback_data = 'RESET')
				inline_keyboard.add(inline_1, inline_2, inline_3, inline_4)

				bot.send_message(chat_id, f'💸 Ваш <b>личный кабинет</b>\n\nБаланс: {balance} ₽\n\nИгр всего - {All}\nИгр выиграно - {win}'
					+ f'\nИгр проиграно - {lose}\n\nЗаявок на вывод - {receive}\nПополнений - {deposit}', parse_mode = 'html', reply_markup = inline_keyboard)
			elif message.text == 'Тех. поддержка':

				bot.send_message(chat_id, f'💻 Техническая <b>поддержка</b> - {support}', parse_mode = 'html')
			elif message.text == 'Играть':

				bot.send_message(chat_id, 'Выберите <b>режим</b> игры', parse_mode = 'html', reply_markup = keyboard.game_keyboard())
			elif message.text == 'Орел & Решка':
				balance = float_2f(db.casino_balance(chat_id))
				message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
				bot.register_next_step_handler(message, coinflip, balance)
			elif message.text == 'Краш':
				balance = float_2f(db.casino_balance(chat_id))
				message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
				bot.register_next_step_handler(message, crash, balance)
			elif message.text == 'Казино':
				balance = float_2f(db.casino_balance(chat_id))
				message = bot.send_message(chat_id, f'Введите <b>сумму</b> ставки\nДоступно: {balance} ₽', parse_mode = 'html', reply_markup = keyboard.endgame_keyboard())
				bot.register_next_step_handler(message, nvuti, balance)
			elif message.text == 'Завершить игру':

				bot.send_message(chat_id, f'Вы вернулись в <b>список</b> игр', parse_mode="html", reply_markup = keyboard.game_keyboard())
			elif message.text == 'Отменить пополнение':

				cancel_deposit(message)
			elif message.text == 'Назад':

				bot.send_message(chat_id, 'Вы вернулись в <b>главное</b> меню', parse_mode = 'html', reply_markup = keyboard.casino_keyboard())
		else:

			bot.send_message(chat_id, '🕔 Бот на <b>технических</b> работах', parse_mode = 'html')

		Thread = threading.Thread(target = set_nickname, args = (message,))
		Thread.start()

	except Exception as e:
		print(e)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	try:
		chat_id = call.message.chat.id

		if call.data == 'RESET':
			db.casino_reset(chat_id)

			balance = db.casino_balance(chat_id)
			win = db.casino_win(chat_id)
			lose = db.casino_lose(chat_id)
			deposit = db.casino_deposit(chat_id)
			receive = db.casino_receive(chat_id)
			All = win + lose

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "Пополнить", callback_data = 'DEPOSIT')
			inline_2 = types.InlineKeyboardButton(text = "Вывести", callback_data = 'RECEIVE')
			inline_3 = types.InlineKeyboardButton(text = "Промокод", callback_data = 'PROMO')
			inline_4 = types.InlineKeyboardButton(text = "Обнулить", callback_data = 'RESET')
			inline_keyboard.add(inline_1, inline_2, inline_3, inline_4)

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'💸 Ваш <b>личный кабинет</b>\n\nБаланс: {balance} ₽\n\nИгр всего - {All}\nИгр выиграно - {win}'
				+ f'\nИгр проиграно - {lose}\n\nЗаявок на вывод - {receive}\nПополнений - {deposit}', parse_mode = 'html', reply_markup = inline_keyboard)
		elif call.data == 'RECEIVE':

			balance = db.casino_balance(chat_id)

			if (balance > 0):
				message = bot.send_message(chat_id, '💸 Введите <b>реквизиты</b> для вывода\nДля избежания мошенничества выводить разрешается исключительно на тот кошелек, с которого было последнее пополнение', parse_mode = 'html')
				bot.register_next_step_handler(message, casino_receive, balance)
			else:
				bot.send_message(chat_id, '⚠️ <b>Не достаточно</b> средств на балансе', parse_mode = 'html')
		elif call.data == 'PROMO':
			message = bot.send_message(chat_id, 'Введите <b>промокод</b>', parse_mode = 'html')
			bot.register_next_step_handler(message, casino_promo)
		elif 'CRASH_' in call.data:
			RegEx = call.data.split('_')

			Thread = threading.Thread(target = crash_start, args = (call, RegEx[1], RegEx[2]))
			Thread.start()
		elif call.data == 'DEPOSIT':

			code = db.casino_code(chat_id)

			if code == 0:
				message = bot.send_message(chat_id, f"Для начала <b>введите код</b> пригласившего вас человека", parse_mode="html")
				bot.register_next_step_handler(message, set_code)
			else:
				message = bot.send_message(chat_id, 'Введите <b>сумму</b> пополнения баланса, от 250 ₽ до 5000 ₽', parse_mode = 'html', reply_markup = keyboard.deposit_keyboard())
				bot.register_next_step_handler(message, casino_deposit)
		elif 'STATUS_' in call.data:

			RegEx = call.data.split('_')

			billId = f'{RegEx[2]}_{RegEx[3]}'

			status_deposit(call, RegEx[1], billId)



	except Exception as e:
		raise e

bot.polling(none_stop = True, interval = 0)		
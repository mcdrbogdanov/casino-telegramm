import sqlite3, datetime, numpy
from datetime import timedelta
from function import float_2f, create_code

sql = 'database/sql.db'
connect = sqlite3.connect(sql)

# Информация о проекте

def project_amount_profit():
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			rows = cur.execute('SELECT count(*) FROM `profit`').fetchall()[0]
			rows = list(rows)
			return rows[0]
	except:
		pass	

def project_total_profit():
	try:
		total = 0.0

		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			rows = cur.execute('SELECT * FROM `profit`').fetchall()
			for row in rows:
				total += float(row[2])

		return round(total)			
	except:
		pass

# Подача заявок и воркер бот

def user_exists_ticket(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `ticket` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	except:
		return False

def user_add_ticket(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `ticket` (`user_id`, `thread`) VALUES(?,?)", (user_id, 0))
	except:
		pass

def user_exists_workers(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	except:
		return False

def user_add_workers(user_id, username, phone):
	try:
		date = datetime.date.today()
		code = create_code(user_id)
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `workers` (`user_id`, `username`, `balance`, `receive`, `amount_profit`, `total_profit`, `status`, `date`, `phone`, `code`) VALUES(?,?,?,?,?,?,?,?,?,?)", 
				(user_id, username, 0, 0, 0, 0, 'Воркер', date, phone, code))
	except:
		pass

# Получение значений подача заявок и воркер бот

def ticket_thread(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `ticket` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass

def workers_username(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass

def workers_balance(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[2]
	except:
		pass		

def workers_receive(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[3]
	except:
		pass

def workers_amount_profit(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[4]
	except:
		pass

def workers_total_profit(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[5]
	except:
		pass

def workers_status(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[6]
	except:
		pass

def workers_phone(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[8]
	except:
		pass

def workers_code(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[9]
	except:
		pass

def workers_rage_profit(user_id):
	try:
		array = []

		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `profit` WHERE `worker` = ?', (user_id,)).fetchall()
			for row in result:
				array.append(row[2])
			
		if (len(array) > 0):	
			middle = numpy.mean(array)
			return float_2f(middle)
		else:
			return 0

	except:
		pass

def workers_last_profit(user_id):
	try:
		array = []
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `profit` WHERE `worker` = ? LIMIT 0,10', (user_id,)).fetchall()
			
			for row in result:
				array.append(f'- {row[1]} | {row[2]} ₽')

		return array
	except Exception as e:
		print(e)

def workers_last_receive(user_id):
	try:
		array = []
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `receive` WHERE `worker` = ? LIMIT 0,10', (user_id,)).fetchall()
			
			for row in result:
				array.append(f'- {row[1]} | {row[2]} ₽')

		return array
	except Exception as e:
		print(e)

def workers_user_id(code):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `code` = ?', (code,)).fetchall()

			for row in result:
				return row[0]
	except:
		return False

def workers_code_to_username(code):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `code` = ?', (code,)).fetchall()

			for row in result:
				return row[1]
	except:
		return False		

def workers_exists_code(code):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `code` = ?', (code,)).fetchall()
			return bool(len(result))
	except:
		return False

def workers_mamonts(code):
	try:
		array = []

		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `invite` = ?', (code,)).fetchall()
			for row in result:
				array.append(f'#{row[10]} | {row[1]} - {row[2]} ₽ - {row[9]}')

		return array
	except:
		pass

def workers_delete_mamonts(code):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			rows = cur.execute("UPDATE `casino` SET `invite` = ? WHERE `invite` = ?", (0, code))
			return rows.rowcount
	except:
		pass

# Обновление значений подача заявок и воркер бот

def workers_update_thread(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `ticket` SET `thread` = ? WHERE `user_id` = ?", (value, user_id))
	except:
		pass

def workers_update_username(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `username` = ? WHERE `user_id` = ?", (value, user_id))
	except:
		pass

def balance_to_receive(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `receive` = ? WHERE `user_id` = ?", (value, user_id))
			cur.execute("UPDATE `workers` SET `balance` = ? WHERE `user_id` = ?", (0, user_id))
	except:
		pass

def workers_clear_receive(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `receive` = ? WHERE `user_id` = ?", (0, user_id))
	except:
		pass

def workers_add_profit(user_id, share):
	try:
		date = datetime.date.today()
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `balance` = balance + ? WHERE `user_id` = ?", (share, user_id))
			cur.execute("UPDATE `workers` SET `amount_profit` = amount_profit + ? WHERE `user_id` = ?", (1, user_id))
			cur.execute("UPDATE `workers` SET `total_profit` = total_profit + ? WHERE `user_id` = ?", (share, user_id))

			cur.execute("INSERT INTO `profit` (`worker`, `date`, `amount`) VALUES (?,?,?)", (user_id, date, share))
	except:
		pass


def workers_add_administator(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `status` = ? WHERE `user_id` = ?", ('Администратор', user_id))
	except:
		pass


def workers_add_support(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `status` = ? WHERE `user_id` = ?", ('Саппорт', user_id))
	except:
		pass	


def workers_add_unsetsupport(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `status` = ? WHERE `user_id` = ?", ('Воркер', user_id))
	except:
		pass	

# Регистрация казино бот

def user_exists_casino(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	except:
		return False

def user_add_casino(user_id, username, invite):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `casino` (`user_id`, `username`, `balance`, `invite`, `win`, `lose`, `deposit`, `receive`, `fake`, `status`) VALUES(?,?,?,?,?,?,?,?,?,?)", (user_id, username, 0, invite, 0, 0, 0, 0, 0, 1))
	except Exception as e:
		print(e)

# Получение значений казино бот

def casino_username(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass
		
def casino_code(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[3]
	except:
		pass

def casino_balance(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[2]
	except:
		pass

def casino_win(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[4]
	except:
		pass

def casino_lose(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[5]
	except:
		pass

def casino_deposit(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[6]
	except:
		pass

def casino_receive(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[7]
	except:
		pass	

def casino_status(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[9]
	except:
		pass			

def casino_fake(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[8]
	except:
		pass					

def casino_user_id(mamont_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `casino` WHERE `id` = ?', (mamont_id,)).fetchall()
			for row in result:
				return row[0]
	except:
		pass

# Обновление значений казино

def casino_update_username(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `username` = ? WHERE `user_id` = ?", (value, user_id))
	except:
		pass

def casino_update_invite(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `invite` = ? WHERE `user_id` = ?", (value, user_id))
	except:
		pass		

def casino_update_balance(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `balance` = ? WHERE `user_id` = ?", (value, user_id))
	except:
		pass		

def casino_update_status(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `status` = ? WHERE `user_id` = ?", (value, user_id))
	except:
		pass				

def casino_reset(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `win` = ? WHERE `user_id` = ?", (0, user_id))
			cur.execute("UPDATE `casino` SET `lose` = ? WHERE `user_id` = ?", (0, user_id))
	except:
		pass	

def casino_to_receive(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `balance` = ? WHERE `user_id` = ?", (0, user_id))
			cur.execute("UPDATE `casino` SET `receive` = receive + ? WHERE `user_id` = ?", (1, user_id))
	except:
		pass	

def casino_add_balance(user_id, pay):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `balance` = balance + ? WHERE `user_id` = ?", (pay, user_id))
	except:
		pass	

def casino_remove_mamont(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `invite` = ? WHERE `user_id` = ?", (0, user_id))
	except:
		pass

def casino_add_win(user_id, win):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `balance` = balance + ? WHERE `user_id` = ?", (win, user_id))
			cur.execute("UPDATE `casino` SET `win` = win + ? WHERE `user_id` = ?", (1, user_id))
	except:
		pass

def casino_add_lose(user_id, bet):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `balance` = balance - ? WHERE `user_id` = ?", (bet, user_id))
			cur.execute("UPDATE `casino` SET `lose` = lose + ? WHERE `user_id` = ?", (1, user_id))
	except:
		pass		

def casino_add_fake(user_id, value):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `fake` = ? WHERE `user_id` = ?", (value, user_id))
	except:
		pass		

def casino_add_deposit(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `deposit` = deposit + ? WHERE `user_id` = ?", (1, user_id))
	except:
		pass				

def casino_fake_clear(user_id):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("UPDATE `casino` SET `fake` = ? WHERE `user_id` = ?", (0, user_id))
	except:
		pass				

# Добавление промокода и проверка

def promo_add(md, pay):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `promo` (`name`, `pay`) VALUES(?,?)", (md, pay))
	except:
		pass

def promo_exists(promo):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `promo` WHERE `name` = ?', (promo,)).fetchall()
			return bool(len(result))
	except:
		return False

def promo_pay(promo):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `promo` WHERE `name` = ?', (promo,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass

def promo_delete(promo):
	try:
		with sqlite3.connect(sql) as con:
			cur = con.cursor()
			cur.execute("DELETE FROM `promo` WHERE `name` = ?", (promo,))
	except:
		pass

	
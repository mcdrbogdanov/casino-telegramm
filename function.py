import random, string, sqlite3, notification
import configparser, datetime

def workers_date(user_id):
	try:
		with sqlite3.connect("database/sql.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[7]
	except:
		pass

def create_code(string_0):
	try:
		
		code = ''
		for i in range(6):
			code += string_0[i]

		return code

	except:
		pass

def create_phone():
	try:

		operators = ['910', '915', '916', '919', '925', '926', '929', '903', '905', '906', '909', '961', '962', '963', '964', '965', '977']
		nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		choice = random.choice(operators)
		psw = ''.join([random.choice(nums) for x in range(7)])

		return f'+7{choice}{psw}'

	except:
		pass

def bill_create(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))	

def float_2f(value):
	try:

		return float("{0:.2f}".format(float(value)))

	except:
		return 0

def share_pay(value):
	try:

		config = configparser.ConfigParser()
		config.read("default.ini")

		percent = config['Telegram']['pay']

		payments = float(value) / 100 * int(percent)
		return float_2f(payments)

	except:
		pass

def share_pay_support(value):
	try:
		config = configparser.ConfigParser()
		config.read("default.ini")

		percent = config['Telegram']['pay_support']

		payments = float(value) / 100 * int(percent)
		return float_2f(payments)
	except:
		pass						

def plural_days(n):
    days = ['день', 'дня', 'дней']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]

def plural_profit(n):
    days = ['профит', 'профита', 'профитов']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
       p = 2

    return str(n) + ' ' + days[p]		

def convert_date(user_id):
	try:
		date = datetime.datetime.strptime(workers_date(user_id), '%Y-%m-%d')
		date = str(date - datetime.datetime.now()).split(',')
		date = date[0]
		date = date.replace('-', '')

		if ('days' in date):
			date = date.replace('days', '')
		elif ('day' in date):
			date = date.replace('day', '')

		date = plural_days(int(date))
		return date
	except Exception as e:
		print(e)

def create_promo(length):
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def is_float(floats):
	try:
		floats = float(floats)
		return True
	except ValueError as e:
		return False

# Уведомления от воркер бота

def new_referal(worker_id, sended_message):
	try:
		
		notification.notification_new_ref(worker_id, sended_message)

	except Exception as e:
		print(e)


def new_deposit(worker_id, mamont_id, value, sended_message):
	try:
		
		notification.notification_new_deposit(worker_id, mamont_id, value, sended_message)

	except Exception as e:
		print(e)		

def new_profit(worker_id, chat_workers, chat_channel, value, sended_message, username_worker, share):
	try:
		
		notification.notification_new_profit(worker_id, chat_workers, chat_channel, value, sended_message, username_worker, share)

	except Exception as e:
		print(e)

def to_receive(worker_id, mamont_id, sended_message):
	try:
		
		notification.notification_to_receive(worker_id, mamont_id, sended_message)

	except Exception as e:
		print(e)


# Уведомления от казино бота

def to_accept_receive(mamont_id):
	try:
		
		notification.notification_to_accept_receive(mamont_id)

	except Exception as e:
		print(e)

def message_to_mamont(mamont_id, sended_message):
	try:

		notification.sended_message_to_mamont(mamont_id, sended_message)

	except Exception as e:
		print(e)	
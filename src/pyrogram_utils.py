from classic_utils import *

from pyrogram import Client, filters, types
import tgcrypto
import asyncio
import random

from main import *
from mysql_utils import *

code = [123456]


START_CMD = "/start"

HELLO_TXT = "Привет, я - бот Школы 21 для приглашения гостей в школу. Для авторизации напиши свой школьный никнейм, либо школьную почту (@student.21-school.ru - для студентов, @21-school.ru - для персонала)"

STUD_MAIL_ADDRESS = "@student.21-school.ru"
SCH_MAIL_ADDRESS = "@21-school.ru"
MAIL_HAS_SENT = "Введи код подтверждения, отправленный на почту!"

CREATE_PASS_BUTTON = "✅Создать пропуск"
VIEW_MY_PASS_BUTTON = "📄Мои пропуски"

api_id = 10439243 #API id
api_hash = "a98d30318fc4d1cd274bc750fa34c8b9" #API hash
bot_token = "5761358088:AAGoBiwLt69qRkI439sKdfCz__tCS3jRLNk"

app = Client(
	"21passbot",
	api_id=api_id,
	api_hash=api_hash,
	bot_token=bot_token
)

active_users = []

async def getUserState(user_id):
	if len(database_select_user(user_id)) > 6:
		return 2
	state = database_select_from_temp(user_id)
	if state == "":
		return int(-1)
	else:
		return int(state[1])

async def simpleMessage(message, text):
	await app.send_message(message.chat.id, text)

@app.on_message(filters.all)
async def message_handler(client, message):
	if message.from_user.id not in active_users:
		active_users.append(message.from_user.id)
		print("new active user")
	try:
		text = str(message.text)
	except:
		pass
# ЗДЕСЬ БУДЕТ ПРОВЕРКА НА НАЛИЧИЕ ЮЗЕРА В БД
	state = int(await getUserState(message.from_user.id))
	user = User()
	user.user_id = message.from_user.id
	if state == -1:
		if text == START_CMD:
			await simpleMessage(message, HELLO_TXT)
			insertUserToTemp(message.from_user.id)
	elif state == 0:
		if STUD_MAIL_ADDRESS in text or SCH_MAIL_ADDRESS in text:
			await simpleMessage(message, MAIL_HAS_SENT)
			print_log(text)
			user.email = text
			user.nickname = text.split("@")[0]
			code[0] = random.randint(100000, 999999)
			print_log("code: " + str(code[0]))
			# отправка сообщения
			setUserState(message.from_user.id, 1)
	elif state == 1:
			if text == str(code[0]):
				create_pass_button = types.KeyboardButton(CREATE_PASS_BUTTON)
				my_passes_button = types.KeyboardButton(VIEW_MY_PASS_BUTTON)
				markup = types.ReplyKeyboardMarkup(keyboard=[[create_pass_button, my_passes_button]], resize_keyboard=True)
				user = User()
				user.campus = 2
				user.full_name = "Secret"
				user.verified = 1
				user.role = 1
				database_add_user(user)
				setUserState(message.from_user.id, 2)
				await app.send_message(message.chat.id, "Авторизация прошла успешно", reply_markup=markup)
			else:
				await app.send_message(message.chat.id, "Неверный код подтверждения!")
	elif state >= 2:
		if text == CREATE_PASS_BUTTON:
			await simpleMessage(message, "Введи ФИО гостя! Если гостей несколько, пиши через запятую.\nВажно: при отсутствии одной из части имени тебе могут ОТКАЗАТЬ в пропуске!")
		elif text == VIEW_MY_PASS_BUTTON:
			await simpleMessage(message, "Список твоих пропусков")
		else:
			create_pass_button = types.KeyboardButton(CREATE_PASS_BUTTON)
			my_passes_button = types.KeyboardButton(VIEW_MY_PASS_BUTTON)
			markup = types.ReplyKeyboardMarkup(keyboard=[[create_pass_button, my_passes_button]], resize_keyboard=True)
			await app.send_message(message.chat.id, "Нажми на кнопку!", reply_markup=markup)

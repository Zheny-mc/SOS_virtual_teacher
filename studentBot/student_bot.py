import telebot

from studentBot.data.connectDB import db

bot = telebot.TeleBot("5274095592:AAG3dGQeLDE5_JnOH05WbPqjFEdk8b3JWOQ")

@bot.message_handler(commands=["start"])
def start(message):
	user = db.get_user(message.chat.id)

	if user["is_passed"]:
		bot.send_message(message.from_user.id, "Вы уже прошли эту викторину. Второй раз пройти нельзя 😥")
		return

	if user["is_passing"]:
		return

	user["question_index"] = 0
	user["is_passing"] = True
	db.set_user(message.chat.id, {"question_index": 0, "is_passing": True})

	post = get_question_message(user)
	if post is not None:
		bot.send_message(message.from_user.id, post["text"], reply_markup=post["keyboard"])

@bot.callback_query_handler(func=lambda query: query.data.startswith("?ans"))
def answered(query):
	user = db.get_user(query.message.chat.id)

	if user["is_passed"] or not user["is_passing"]:
		return

	user["answers"].append(int(query.data.split("&")[1]))
	db.set_user(query.message.chat.id, {"answers": user["answers"]})

	post = get_answered_message(user)
	if post is not None:
		bot.edit_message_text(post["text"], query.message.chat.id, query.message.message_id,
						 reply_markup=post["keyboard"])

@bot.callback_query_handler(func=lambda query: query.data == "?next")
def next(query):
	user = db.get_user(query.message.chat.id)

	if user["is_passed"] or not user["is_passing"]:
		return

	user["question_index"] += 1
	db.set_user(query.message.chat.id, {"question_index": user["question_index"]})

	post = get_question_message(user)
	if post is not None:
		bot.edit_message_text(post["text"], query.message.chat.id, query.message.message_id,
						 reply_markup=post["keyboard"])


def get_question_message(user):
	count_question = db.get_count_question()
	if user["question_index"] == count_question:
		count = 0
		for question_index, question in enumerate( sorted(db.get_all_question(), key=lambda q: q['id']) ):
			if question["correct"] == user["answers"][question_index]:
				count += 1
		percents = round(100 * count / count_question)

		db.set_user(user["chat_id"],
					{"percentages": percents, 'true_count': count, "false_count": count_question})

		if percents < 40:
			smile = "😥"
		elif percents < 60:
			smile = "😐"
		elif percents < 90:
			smile = "😀"
		else:
			smile = "😎"

		text = f"Вы ответили правильно на {percents}% вопросов {smile}"

		db.set_user(user["chat_id"], {"is_passed": True, "is_passing": False})

		return {
			"text": text,
			"keyboard": None
		}

	question = db.get_question(user["question_index"])

	if question is None:
		return

	keyboard = telebot.types.InlineKeyboardMarkup()
	for answer_index, answer in enumerate(question["answers"]):
		keyboard.row(telebot.types.InlineKeyboardButton(f"{chr(answer_index + 97)}) {answer}",
														callback_data=f"?ans&{answer_index}"))

	text = f"Вопрос №{user['question_index'] + 1}\n\n{question['text']}"

	return {
		"text": text,
		"keyboard": keyboard
	}

def get_answered_message(user):
	question = db.get_question(user["question_index"])

	text = f"Вопрос №{user['question_index'] + 1}\n\n{question['text']}\n"

	for answer_index, answer in enumerate(question["answers"]):
		text += f"{chr(answer_index + 97)}) {answer}"

		if answer_index == question["correct"]:
			text += " ✅"
		elif answer_index == user["answers"][-1]:
			text += " ❌"

		text += "\n"

	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.row(telebot.types.InlineKeyboardButton("Далее", callback_data="?next"))

	return {
		"text": text,
		"keyboard": keyboard
	}


bot.polling()
import telebot

from Analize_result_tests import *
from data.connectDB import db

bot = telebot.TeleBot("5976670407:AAFRFqrMLx0l4vxydqyXicvnwWDanaetanw")


def get_contacts(query):
    return (query.message.chat.id, query.message.message_id)

@bot.message_handler(commands=["start"])
def start(message):
    buttons = {'тест': '?test', 'статистика': '?analize'}

    keyboard = telebot.types.InlineKeyboardMarkup()
    for name, command in buttons.items():
        keyboard.row(telebot.types.InlineKeyboardButton(name, callback_data=command))

    name = message.from_user.first_name
    text = f"Привет, {name}"
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda query: query.data == "?analize")
def analize(query):
    chat_id, message_id = get_contacts(query)

    text = 'Выбери график:'
    buttons = {
        'график 1': '?analize_chart&1',
        'график 2': '?analize_chart&2',
        'график 3': '?analize_chart&3'
    }
    keyboard = telebot.types.InlineKeyboardMarkup()
    for name, command in buttons.items():
        keyboard.row(telebot.types.InlineKeyboardButton(name, callback_data=command))

    bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda query: query.data.startswith("?analize_chart"))
def analize_chart_all(query):
    chat_id, message_id = get_contacts(query)

    numb_chart = int(query.data.split("&")[1])
    text = f'График {numb_chart}:'
    bot.edit_message_text(text, chat_id, message_id)

    get_one_graphic(numb_chart)
    my_dir = f'./analize/graphics/graph{numb_chart}.png'
    bot.send_photo(chat_id, photo=open(my_dir, 'rb'))

# ---------------------------- test -------------------------------------
@bot.callback_query_handler(func=lambda query: query.data == "?test")
def test(query):
    chat_id, message_id = get_contacts(query)

    text = 'Работа с тестом:'
    buttons = {
        'создать': '?test_create',
        # 'изменить': '?test_change',
        'удалить': '?test_delete',
        'посмотреть': '?test_read'
    }
    keyboard = telebot.types.InlineKeyboardMarkup()
    for name, command in buttons.items():
        keyboard.row(telebot.types.InlineKeyboardButton(name, callback_data=command))

    bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda query: query.data == "?test_read" or query.data == "?test_delete")
def test_read(query):
    chat_id, message_id = get_contacts(query)

    count = db.get_count_question()
    buttons_question = {f'В{i}': f'{query.data}_question&{i}' for i in range(1, count+1)}

    keyboard = get_keyboard(buttons_question)

    text = 'Выбери вопрос для '
    if query.data == "?test_read":
        text += 'просмотра:'
    elif query.data == "?test_delete":
        text += 'удаления:'

    bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

# ------------------------ test create -----------------------------
def get_text_create():
    return 'Конструктор вопроса:'

def get_menu_creare():
    return {
        'ввод формулировка': '?question_input_text',
        'ввод варианта ответа': '?question_input_answer',
        'ввод номер правильного ответа': '?question_input_correct',
        'готово': '?question_ready',
        'отмена': '?question_canel'
    }

def get_keyboard(dict_button):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for name, command in dict_button.items():
        keyboard.row(telebot.types.InlineKeyboardButton(name, callback_data=command))
    return keyboard


@bot.callback_query_handler(func=lambda query: query.data == "?test_create")
def test_create(query):
    chat_id, message_id = get_contacts(query)
    text, buttons_question = get_text_create(), get_menu_creare()
    db.get_current_question(chat_id)
    keyboard = get_keyboard(buttons_question)
    bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

# ----------------------- формулировка вопроса -----------------------------
@bot.callback_query_handler(func=lambda query: query.data == "?question_input_text")
def test_question_input_text(query):
    chat_id, message_id = get_contacts(query)
    db.get_current_question(chat_id)
    text = 'Введи команду:\n/q_text <значение>'
    bot.edit_message_text(text, chat_id, message_id)

@bot.message_handler(func=lambda query: query.text.startswith("/q_text"))
def test_q_title(query):
    chat_id = query.chat.id
    args = query.text.split(' ')
    if (len(args) == 2):
        text_cur_question = query.text.split(' ')[1] # исходный текст
        db.update_current_question(chat_id, {"text": text_cur_question})

        text, buttons_question = get_text_create(), get_menu_creare()
        keyboard = get_keyboard(buttons_question)
        bot.send_message(chat_id, text, reply_markup=keyboard)

# ----------------------- ответы для вопроса -----------------------------
@bot.callback_query_handler(func=lambda query: query.data == "?question_input_answer")
def test_question_input_answer(query):
    chat_id, message_id = get_contacts(query)
    text = 'Введи команду:\n/q_answer <значение>'
    bot.edit_message_text(text, chat_id, message_id)

@bot.message_handler(func=lambda query: query.text.startswith("/q_answer"))
def test_q_answer(query):
    chat_id = query.chat.id
    args = query.text.split(' ')
    if (len(args) == 2):
        answer_cur_question = query.text.split(' ')[1]  # исходный текст
        cur_question = db.get_current_question(chat_id)
        answers = cur_question["answers"]
        answers.append(answer_cur_question)
        db.update_current_question(chat_id, {"answers": answers})

        text, buttons_question = get_text_create(), get_menu_creare()
        keyboard = get_keyboard(buttons_question)
        bot.send_message(chat_id, text, reply_markup=keyboard)

# ----------------------- правильный ответ для вопроса -----------------------------
@bot.callback_query_handler(func=lambda query: query.data == "?question_input_correct")
def test_question_input_correct(query):
    chat_id, message_id = get_contacts(query)
    text = 'Введи команду:\n/q_correct <значение>'
    bot.edit_message_text(text, chat_id, message_id)

@bot.message_handler(func=lambda query: query.text.startswith("/q_correct"))
def test_q_correct(query):
    chat_id = query.chat.id
    args = query.text.split(' ')
    if (len(args) == 2):
        correct_cur_question = int(query.text.split(' ')[1]) # исходный текст
        db.update_current_question(chat_id, {"correct": correct_cur_question})


        text, buttons_question = get_text_create(), get_menu_creare()
        keyboard = get_keyboard(buttons_question)
        bot.send_message(chat_id, text, reply_markup=keyboard)


# ----------------------- кнопка применения собранного вопроса -----------------------------
@bot.callback_query_handler(func=lambda query: query.data == "?question_ready")
def test_question_input_correct(query):
    chat_id, message_id = get_contacts(query)

    cur_question = db.get_current_question(chat_id)
    id_cur_q = db.get_count_question()
    cur_question["id"] = id_cur_q
    db.create_question(cur_question)
    db.delete_current_question(chat_id)

    text = 'Работа с тестом:'
    buttons_question = {
        'создать': '?test_create',
        # 'изменить': '?test_change',
        'удалить': '?test_delete',
        'посмотреть': '?test_read'
    }
    keyboard = get_keyboard(buttons_question)
    bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

# ----------------------- кнопка применения собранного вопроса -----------------------------
@bot.callback_query_handler(func=lambda query: query.data == "?question_canel")
def test_question_input_correct(query):
    chat_id, message_id = get_contacts(query)

    db.delete_current_question(chat_id)

    text = 'Работа с тестом:'
    buttons_question = {
        'создать': '?test_create',
        # 'изменить': '?test_change',
        'удалить': '?test_delete',
        'посмотреть': '?test_read'
    }
    keyboard = get_keyboard(buttons_question)
    bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard)

# ------------------------ test read -----------------------------
@bot.callback_query_handler(func=lambda query: query.data.startswith("?test_read_question"))
def test_read_question(query):
    chat_id, message_id = get_contacts(query)

    numb_question = int(query.data.split("&")[1])
    question = db.get_question(numb_question-1)

    text_question = question['text']

    text_answer = ''
    for i, ans in enumerate(question['answers']):
        is_check = " ✅" if i == question['correct'] else ''
        text_answer += f'{i+1}) {ans} {is_check}\n'

    text = f'Вопрос {text_question}:\n{text_answer}'
    bot.edit_message_text(text, chat_id, message_id)

# ------------------------ test delete -----------------------------
@bot.callback_query_handler(func=lambda query: query.data.startswith("?test_delete_question"))
def test_delete_question(query):
    numb_question = int(query.data.split("&")[1])
    db.delete_question(numb_question-1)
    text = f'Вопрос {numb_question} удален:'
    bot.edit_message_text(text, query.message.chat.id, query.message.message_id)



bot.polling()
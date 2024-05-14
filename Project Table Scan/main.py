import telebot
import sqlite3
from telebot import types
from classRecognizer import Recognizer
from classCompareson import Compareson
from classDataBase import DataBase

TOKEN = "Токен бота"
bot = telebot.TeleBot(TOKEN)
user = None
school_ID = None
Answer = None
percent = None
teachers_school_ID = "123321"
students_school_ID_list = ["234432", "345543"]

@bot.message_handler(commands=["start"])
def start(message):
    DataBase('database.sql').create_table()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("Teacher")
    btn2 = types.KeyboardButton("Student")
    markup.row(btn1, btn2)
    bot.send_message(
        message.chat.id,
        "Welcome to Automatic Test Checking Service!",
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, user_type)

def user_type(message):
    global user
    user = message.text.strip()
    if user == "Teacher":
        bot.send_message(message.chat.id, "Send the teacher's ID")
        bot.register_next_step_handler(message, user_school_ID)
    elif user == "Student":
        total_users = DataBase('database.sql').count()
        if total_users >= 1:
            bot.send_message(message.chat.id, "Send the student's ID")
            bot.register_next_step_handler(message, user_school_ID)
        else:
            bot.send_message(
                message.chat.id,
                "The teacher has not uploaded the answers yet! Please try again later!",
            )
            bot.register_next_step_handler(message, user_type)

    else:
        bot.send_message(message.chat.id, "Click on the button!")
        bot.register_next_step_handler(message, user_type)

def user_school_ID(message):
    global school_ID
    if message.content_type == "text":
        school_ID = message.text.strip()
        if school_ID == teachers_school_ID:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Upload photo")
            btn2 = types.KeyboardButton("Get results")
            btn3 = types.KeyboardButton("Clear DataBase")
            markup.row(btn1, btn2, btn3)
            bot.send_message(
                message.chat.id, "What would you like to do?", reply_markup=markup
            )
            bot.register_next_step_handler(message, selection_btn)
        elif school_ID in students_school_ID_list:
            bot.send_message(
                message.chat.id, "Send a photo with answers")
            bot.register_next_step_handler(message, get_photo)
        elif school_ID == "/restart":
            bot.send_message(message.chat.id, "Send /start to start over!")
            bot.register_next_step_handler(message, start)
        else:
            bot.reply_to(message, "Write the school ID correctly or send /restart!")
            bot.register_next_step_handler(message, user_school_ID)
    elif school_ID == "/restart":
        bot.send_message(message.chat.id, "Send /start to start over!")
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, "Write the school ID!")
        bot.register_next_step_handler(message, user_school_ID)

def selection_btn(message):
    selection = message.text.strip()
    if selection == "Upload photo":
        bot.send_message(message.chat.id, "Send a photo with the answers")
        bot.register_next_step_handler(message, get_photo)
    elif selection == "Get results":
        users = DataBase('database.sql').select()
        info = ""
        if len(users) > 1:
            for el in users[1:]:
                info += f"School ID: {el[1]} , correctAnswersPercentage: {el[3]}%\n"
            bot.send_message(message.chat.id, info)
        elif len(users) == 0:
            bot.send_message(
                message.chat.id,
                "Upload a photo first by clicking the upload photo button!",
            )
        else:
            bot.send_message(
                message.chat.id, "The students did not upload the answers!"
            )
        bot.register_next_step_handler(message, selection_btn)
    elif selection == "Clear DataBase":
        DataBase('database.sql').delete_all()
        bot.send_message(message.chat.id, "The Data Base has been cleared!")
        bot.register_next_step_handler(message, selection_btn)
    elif selection == "/restart":
        bot.send_message(message.chat.id, "Send /start to start over!")
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, "Select the button or send /restart")
        bot.register_next_step_handler(message, selection_btn)

def get_photo(message):
    global Answer
    if message.content_type == "photo":
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        full_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
        Answer = Recognizer(full_url, 20, 6).data_sheet()
        DataBase('database.sql').add_data(user, school_ID, Answer, percent)
        user_data = DataBase('database.sql').select_last()
        user_ = user_data[0]
        if user_ == "Student":
            markup = types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("Get results", callback_data="student"))
            bot.send_message(message.chat.id, "The results are ready!", reply_markup=markup)
        if user_ == "Teacher":
            bot.send_message(message.chat.id, "The Data has been uploaded!")
            bot.register_next_step_handler(message, selection_btn)
    elif message.text == "/restart":
        bot.send_message(message.chat.id, "Send /start to start over!")
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, "Upload an image or send /restart!")
        bot.register_next_step_handler(message, get_photo)

@bot.callback_query_handler(func=lambda call: True)
def callback1(call):
    if call.data == "student":
        global percent
        teacher_user_data = DataBase('database.sql').select_first()
        student_user_data = DataBase('database.sql').select_last()
        data1 = teacher_user_data[2]
        data2 = student_user_data[2]
        wrong = ", ".join(Compareson(data1, data2, 6, 20).compare())
        percent = Compareson(data1, data2, 6, 20).correct_answers_percentage()
        bot.send_message(call.message.chat.id, f"Wrong answers: {wrong}")
        bot.send_message(
            call.message.chat.id, f"Percentage of correct answers: {percent}%"
        )
        DataBase('database.sql').update(school_ID, percent)

bot.polling(none_stop=True)

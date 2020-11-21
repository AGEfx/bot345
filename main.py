import telebot
from telebot import types
from threading import Thread
import re
import methods as m
import time
import markups
import schedule

TOKEN = "1427085342:AAGpA8twshUqW0Sgicor-X84p_VDfaOua-0"

bot = telebot.TeleBot(TOKEN)

schedule_time = "10:00"
change_time = "00:00"

currentDay = 0
is_ready = False

award = ""
id =""

@bot.message_handler(commands=['start'])
def start(message):
    global id
    id = message
    text = "Привет. Я бот... (добавить текст). \n" +\
           "Чтобы получить всю информацию нажми кноппку помощь(в разработке)\n" +\
           "Прежде, чем начать введи текущее время. Это нужно для настройки ежедневной отправки ботом планирования\n\n" +\
           "Отправь текущее время в таком формате 10:34"
    msg = bot.send_message(message.chat.id, text ,reply_markup=markups.markup)
    m.logger(message.from_user.username, message.from_user.id, message.text, text)
    bot.register_next_step_handler(msg, get_time)

def get_time(message):
    global schedule_time
    if re.match("^([0-2]\d:[0-5]\d)$",message.text) is not None:
        server_time = time.strftime("%H:%M", time.localtime())
        schedule_time = m.set_the_right_time(server_time, message.text)
        text = "Отлично, я запомнил"
        m.logger(message.from_user.username, message.from_user.id, message.text, text)
        bot.send_message(message.chat.id, text)
    else:
        text = "Отправьте мне время в верном формате"
        msg = bot.send_message(message.chat.id, text)
        m.logger(message.from_user.username, message.from_user.id, message.text, text)
        bot.register_next_step_handler(msg,get_time)

@bot.message_handler(commands=['reset'])
def reset(message):
    print(id)
    m.habits.clear()
    text = "Список успешно очищен. Вы можете создать новый с помощью кнопки добавить"
    m.logger(message.from_user.username, message.from_user.id, message.text, text)
    bot.send_message(message.chat.id, text, reply_markup=markups.markup)


@bot.message_handler(commands=['change'])
def change(message):
    text = "Изменено"
    m.generatePlan()
    bot.send_message(message.chat.id, text, reply_markup=markups.markup1)
@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text == "Добавить":
        add(message)
    elif message.text == "План на день":
        day(message)
    elif message.text ==  "Награда":
        get_award(message)
    elif message.text == "Есть. Выполнено":
        ready(message)

    else:
        text = "Я не знаю, что вам ответить"
        m.logger(message.from_user.username, message.from_user.id, message.text, text)
        bot.send_message(message.chat.id, text)

def add(message):
    text = "Введи список (чего) в таком формате\n\n" +\
           "Название привычки 1\n" +\
           "Название привычки 2\n" +\
           "Название привычки 3\n" +\
           "Название привычки 4\n" +\
           "Название привычки 5\n"
    msg = bot.send_message(message.chat.id, text)
    #(если привычк ежедневная, то в конце поставьте + или * :
    m.logger(message.from_user.username, message.from_user.id, message.text, text)
    bot.register_next_step_handler(msg,getList)

def getList(message):
    print(message.text)
    m.parseList(message.text)
    m.generatePlan()
    text = "Готово, я записал, вот смотрите, все верно?\n" + m.toStr()
    btn_1 = types.InlineKeyboardButton('Да', callback_data='yes')
    btn_2 = types.InlineKeyboardButton('Нет', callback_data='no')
    markup = types.InlineKeyboardMarkup().add(btn_1).add(btn_2)
    m.logger(message.from_user.username, message.from_user.id, message.text, text)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == 'yes')
def process_callback_button1(query):
    message = query.message
    bot.answer_callback_query(query.id)
    text = 'Отлично, теперь введите название награды. (например, покупка нового телефона, поход в мак и тп.)'
    msg = bot.send_message(query.from_user.id, text, reply_markup=markups.markup)

    m.logger(message.from_user.username, message.from_user.id, message.text, text)

    bot.edit_message_reply_markup(message.chat.id, message_id=message.message_id)
    bot.register_next_step_handler(msg,create_award)

def create_award(message):
    global award
    award = message.text
    text = 'Отлично я записал. Пора идти в бой.\n\n' \
          'Вот задачи на сегодня. Выполняй все и жми кнопку "Есть. Выполнено. \n\n"'
    m.logger(message.from_user.username, message.from_user.id, message.text, text)
    bot.send_message(message.chat.id, text, reply_markup=markups.markup1)
    day(message)

def get_award(message):
    bot.send_message(message.chat.id, award, markups.markup1)

def ready(message):
    global is_ready
    if not is_ready:
        global currentDay

        bot.send_message(message.chat.id, "Красава",reply_markup=markups.markup1)
        currentDay+=1
        is_ready = True
    else:
        bot.send_message(message.chat.id, "Вы уже выполнили все задач на сегодня. Ждите новые", reply_markup=markups.markup1)

@bot.callback_query_handler(func=lambda c: c.data == 'no')
def process_callback_button1(query):
    message = query.message
    bot.answer_callback_query(query.id)
    reset(query.message)
    m.logger(message.from_user.username, message.from_user.id, message.text, "Сообщения нет(комментарий - Кнопка нет)")
    bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id)
    add(query.message)


@bot.message_handler(commands=['day'])
def day(message):
    global currentDay
    if m.habits != []:
        if not is_ready:
            msg = m.getPlan()
            text = "Вот, это тебе на сегодня:\n\n" + msg
            m.logger(message.from_user.username, message.from_user.id, message.text, text)
            bot.send_message(message.chat.id, text, reply_markup=markups.markup1)
        else:
            text = "Сегодня ты уже все выполнил"
            m.logger(message.from_user.username, message.from_user.id, message.text, text)
            bot.send_message(message.chat.id, text, reply_markup=markups.markup1)
    else:
        text = "Сначала необходимо добавить список"
        m.logger(message.from_user.username, message.from_user.id, message.text, text)
        bot.send_message(message.chat.id, text)


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(30)

def function_to_run():
    global is_ready
    is_ready = False
    m.generatePlan()
    day(id)

if __name__ == "__main__":
    # Create the job in schedule.
    schedule.every().day.at(schedule_time).do(function_to_run)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start()

    # And then of course, start your server.




bot.polling()

# TODO План бота
#   defdw
#TODO: --OK!-- 1. Деплой приложения.
#TODO: --OK!-- 2.Проверка работы
#TODO: --OK!-- 3. создание класса привычек(поля: название, параметр (булев)
#TODO: --OK!-- 4. Метод, запрашивающий ввод в определенном формате
#TODO: 5. Метод устанавливающий количество дней.
#TODO: --OK!-- 5.5. Метод создающий награду
#TODO: --OK!-- 6. Метод выводящий список всех привычек
#TODO: 7. --OK-- Метод генерирующий привычки на день
#TODO: 8. --OK!-- Метод запрашивающий потверждение выполнения в конце дня.
#TODO: 9. Метод наказывающий за невыполнение или поощряющий
#TODO: 10. --OK!-- #  Добавить клавиатуру


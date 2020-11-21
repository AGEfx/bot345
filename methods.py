from random import shuffle
from datetime import datetime
from habit import Habit

habits = []
tHabits = []

def parseList(text):
    title = ""
    d = False

    list = text.split("\n")
    for i in range(len(list)):
        d = False
        if(list[i].endswith('+')):
            title = list[i].replace("+","")
            d = True
        else:
            title = list[i]
        habits.append(Habit(title,d))

def toStr():
    s = ""
    for i in range(len(habits)):
        if habits[i].isDaily == True:
            s+=s(i+1) +". " +habits[i].name+ "\n"
                           #^" (Ежедневная)"
        else:
            s += str(i+1)+". " + habits[i].name + "\n"
    return s


def generatePlan():
    d = round(len(habits)/2)
    shuffle(habits)
    for i in range(d):
        tHabits.append(habits[i])

def getPlan():
    return  toStr()


def set_the_right_time(server_time, time):
    hours = int(time.split(":")[0])
    delta = hours - 10
    server_time_hours = int(server_time.split(":")[0])
    server_time_hours -= delta
    if server_time_hours < 10:
        right_time = "0" + str(server_time_hours) + ":00"
    else:
        right_time = str(server_time_hours) + ":00"


    print("Serv:", server_time)
    print("User time" ,time)
    print("Right time", right_time)
    #print("Change time", change_time)
    return right_time


def logger(user, id, text, message):
    log_message = "--------------------------------------------------\n" +\
        "Пользователь: " + user + " (" + str(id) + ")\n" +\
        "Сообщение от пользователя: " + text + "\n" +\
        "Сообщение от бота: " + message + "\n" +\
        "--------------------------------------------------"
    print(log_message)

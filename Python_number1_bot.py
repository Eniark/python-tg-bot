import telebot
import config
import mysql.connector
from telebot import types
import keyboards
import time

bot=telebot.TeleBot(config.TOKEN)


students={"юранус":"Юра Гуліватий", "Yurii":"Юрій Кошкін"}
queue=[]
hours=0
minutes=0

# def add_record(msg):
#     if msg.from_user.first_name in queue:
#         bot.send_message(msg.chat.id, "Ти вже у черзі, двічі додаватись у чергу не можна.", parse_mode="html")
#         return
#     queue.append(msg.from_user.first_name)
#     bot.send_message(msg.chat.id, "Тебе успішно додано!", parse_mode="html", reply_markup=keyboards.WASHING_KEYBOARD)
#     print(queue)
#     print("Added new user")
#
# def show_records(msg):
#     formatted_record=""
#     print(result)
#     if len(queue)==0:
#         bot.send_message(msg.chat.id, "В черзі нікого ще немає...")
#     else:
#         for record in queue:
#             formatted_record+=str(record[0])+". "+record[1]+" --> "+record[2]+"\n"
#         bot.send_message(msg.chat.id, formatted_record)

@bot.message_handler(func=lambda x:x.text=="Записатися у чергу")
def add_to_queue(msg):
    # if msg.from_user.first_name in queue:
    #     bot.send_message(msg.chat.id, "Ти вже у черзі, двічі додаватись у чергу не можна.", parse_mode="html")
    #     return
    queue.append([msg.from_user.first_name, "В очікуванні"])
    bot.send_message(msg.chat.id, "Тебе успішно додано!", parse_mode="html", reply_markup=keyboards.WASHING_KEYBOARD)
    print(queue)
    print("Added new user")

@bot.message_handler(func=lambda x:x.text=="Переглянути чергу")
def peek_in_the_queue(msg):
    pos=1
    formatted_record = ""
    if len(queue)==0:
        bot.send_message(msg.chat.id, "В черзі нікого ще немає...")
    else:
        for record in queue:
            print(record)
            formatted_record+=str(pos)+". "+record[0]+" --> "+str(record[1])+"\n"
            pos+=1
        bot.send_message(msg.chat.id, formatted_record)
    pos=1
@bot.message_handler(commands=["start"])
def welcome(msg):
    if msg.from_user.last_name==None:
        bot.send_message(msg.chat.id, "Вітання {} 😁  \nЯ - полегшення твого життя в УАЛ.\n"
                                      "Зі мною ти зможеш ще краще тайм менеджити свої завдання і бути ще більш свідомим студентом.".format(
            msg.from_user.first_name.capitalize()),
                         parse_mode="html", reply_markup=keyboards.IN_QUEUE_KEYBOARD)
    else:
        bot.send_message(msg.chat.id, "Вітання {} {} 😁 \nЯ - полегшення твого життя в УАЛ.\n"
                                      "Зі мною ти зможеш ще краще тайм менеджити свої завдання і бути ще більш свідомим студентом.".format(msg.from_user.first_name.capitalize(), msg.from_user.last_name ),
                         parse_mode="html", reply_markup=keyboards.IN_QUEUE_KEYBOARD)
@bot.message_handler(func=lambda x:x.text == "Покинути чергу")
def leave_queue(msg):
    print(queue)
    for i in queue:
        for j in i:
        # print("exec")
            if j==msg.from_user.first_name:
                queue.pop(queue.index(i))
                print("Succesfully popped the user")
                bot.send_message(msg.chat.id, "Тебе успішно видалено з черги!", parse_mode="html", reply_markup=keyboards.IN_QUEUE_KEYBOARD)
                return
@bot.message_handler(func=lambda x:x.text == "Закласти прання")
def start_washing(msg):
    bot.send_message(msg.chat.id, "Будь ласка, оберіть режим прання:", parse_mode="html", reply_markup = keyboards.REGIME_OF_WASHING_KEYBOARD)

@bot.message_handler(func=lambda x:x.text=="1 година")
def one_hour(msg):
    remove_keyboard=types.ReplyKeyboardRemove(selective=False)
    bot.send_message(msg.chat.id, "Ваш таймер на 1 годину успішно налаштований!", parse_mode="html", reply_markup=keyboards.WAITING_KEYBOARD)
    time_to_wait = 0
    converted_washing_time=60
    for record in queue:
        if msg.from_user.first_name in record:
            record_index=queue.index(record)
            break

    while time_to_wait!=20:
        queue[record_index][1]= "Миється: залишилось {} хвилин".format(str(60 - time_to_wait))
        time_to_wait+=1
        time.sleep(1)
        print(time_to_wait)

    bot.send_message(msg.chat.id, "ЗАБЕРИ СВОЄ ПРАННЯ!", parse_mode="html",
                     reply_markup=keyboards.IN_QUEUE_KEYBOARD)
    time_to_wait=0
@bot.message_handler(func=lambda x:x.text=="2 години")
def two_hours(msg):
    hours=0
    minutes=0
    washing_time = 120
    time_to_wait=0
    bot.send_message(msg.chat.id, "Ваш таймер на 2 години успішно налаштований!", parse_mode="html", reply_markup=keyboards.WAITING_KEYBOARD)

    for record in queue:
        if msg.from_user.first_name in record:
            record_index=queue.index(record)
            break

    while washing_time>=60:
        washing_time-=60
        hours+=1
    minutes=washing_time
    while time_to_wait!=120:
        queue[record_index][1]="Миється: залишилось {} години {} хвилин.".format(hours, minutes)

        time_to_wait+=1
        time.sleep(60)
    bot.send_message(msg.chat.id, "ЗАБЕРИ СВОЄ ПРАННЯ!", parse_mode="html", reply_markup=keyboards.IN_QUEUE_KEYBOARD)
    time_to_wait=0
@bot.message_handler(func=lambda x:x.text=="30 хвилин")
def thirty_mins(msg):
    hours=0
    minutes=0
    time_to_wait = 0
    bot.send_message(msg.chat.id, "Ваш таймер на 30 хвилин успішно налаштований!", parse_mode="html", reply_markup=keyboards.WAITING_KEYBOARD)

    for record in queue:
        if msg.from_user.first_name in record:
            record_index=queue.index(record)
            break

    while time_to_wait!=30:
        queue[record_index][1]="Миється: залишилось {} хвилин".format(30 - time_to_wait)
        time_to_wait+=1
        time.sleep(60)
    time_to_wait=0
    bot.send_message(msg.chat.id, "ЗАБЕРИ СВОЄ ПРАННЯ!", parse_mode="html", reply_markup=keyboards.IN_QUEUE_KEYBOARD)

bot.polling(none_stop=True)

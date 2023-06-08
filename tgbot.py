import telebot,random
from telebot import types
from threading import Thread
import secret
bot = telebot.TeleBot(secret.nothing)
users=[-1001806756228]
@bot.message_handler(commands=['start'])
def start(message):
    print("Started")
    users.append(message.chat.id)
    bot.send_message(message.chat.id, text="Вы добавлены")


def send(name,priz):
    global users
    print(users)
    for i in users:
        print(i,f"{name} купил {priz}")
        bot.send_message(i, text=f"{name} купил {priz}")
#Thread(target=func).start()
#Thread(target=lambda:bot.polling(none_stop=True)).start()

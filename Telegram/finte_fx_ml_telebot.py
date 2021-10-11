import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.accounts as accounts
from oanda import *
from telebot import types
import telebot
from Credentials import *
import datetime


bot = telebot.TeleBot(token)
chat_ids = ["497602206", "697913165", "459345300", "234788486", "894452777", "966101210"]

def main_keyboard():
    key1 = types.InlineKeyboardButton(text = "View Positions", callback_data = "vpos")
    key2 = types.InlineKeyboardButton(text = "View Summary", callback_data = "vsum")
    return (key1, key2)

def keyboardCompiler(chat_id, keys, message):
    keyboard = types.InlineKeyboardMarkup()
    for key in keys:
        keyboard.add(key)
    reply_markup = keyboard
    bot.send_message(chat_id, message, reply_markup=reply_markup)
    return None

@bot.callback_query_handler(func = lambda call: True)
def button(call):
    chat_id = str(call.message.chat.id)
    query = call.data
    time = str(datetime.datetime.now())
    print("[" + time + "]: Query by " + chat_id, flush = True) ##getVisitorName(chat_id) locates in help_functions
    if query == "vpos":
        bot.send_message(chat_id, "There are no orders")
    if query == "vsum":
        t = formatAccountSummary()
        bot.send_message(chat_id, formatAccountSummary())


@bot.message_handler(commands = ['start'])
def start(msg):
    chat_id = str(msg.chat.id)
    #bot.send_message(chat_id, "Hello! Your chat ID is " + str(chat_id))
    if chat_id in chat_ids:
        keyboardCompiler(chat_id, main_keyboard(), "Welcome!")
    else:
        bot.send_message(chat_id, "You are denied access")
    
@bot.message_handler(commands = ['Positions'])
def show_positions(msg):
    chat_id = msg.chat.id
    searchCustomer(chat_id, keyboardCompiler, bot, customerKeyboardNoHide, agent_contact)

print("OK")
bot.infinity_polling()


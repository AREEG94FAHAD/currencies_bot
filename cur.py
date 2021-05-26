from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

import os
APITOKEN = os.environ.get('APITOKEN')

currencies = ['Bitcoin', 'Ethereum', 'Tether', 'Cardano', 'Chainlink', 'Chainlink',
              'Dogecoin', 'Ethereum-Classic', 'Polkadot', 'USD-Coin', 'Internet-Computer', 'Bitcoin-Cash', 'THORChain', 'Uniswap', 'Algorand']

bot = telebot.TeleBot(APITOKEN)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for i in range(0, 14, 3):
        markup.add(InlineKeyboardButton(currencies[i], callback_data=currencies[i]), InlineKeyboardButton(
            currencies[i+1], callback_data=currencies[i+1]), InlineKeyboardButton(
            currencies[i+2], callback_data=currencies[i+2]))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(
        message.chat.id, "Select the currency", reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    try:

        x = cg.get_price(ids=call.data, vs_currencies='usd')

        bot.send_message(call.from_user.id, str(
            x[str(call.data).lower()]['usd'])+" $")

    except:
        bot.send_message(call.from_user.id,
                         'something went wrong try agin later')


bot.polling()

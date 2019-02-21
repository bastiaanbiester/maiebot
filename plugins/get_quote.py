from plugins import new_message
import random
import os


# opens chat_id.txt and sends a random quote to the chat
def get_quote(bot, update):
    new_message.new_message(update.message.from_user.username, update.message.text)

    if not os.path.exists('quotes'):
        os.makedirs('quotes')

    with open(f'./quotes/{update.message.chat_id}.txt', 'r', encoding='utf-8') as list_of_quotes:
        quotes = list_of_quotes.readlines()
        quote = quotes[random.randint(0, len(quotes) - 1)]
        bot.send_message(chat_id=update.message.chat_id, text=quote)

import logging
from config import TOKEN

import contentFetcher as cf


from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=main_menu_message(), reply_markup=main_menu_keyboard())


def first_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=first_menu_message(), reply_markup=first_menu_keyboard()
    )


def second_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=second_menu_message(), reply_markup=second_menu_keyboard()
    )


# and so on for every callback_data option
def first_submenu(bot, update):
    pass


def second_submenu(bot, update):
    pass


def echo(update, context):
    """Get random quote"""
    quote = cf.getRandom("Learning.txt")
    update.message.reply_text(quote)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="m1")],
        [InlineKeyboardButton("Option 2", callback_data="m2")],
        [InlineKeyboardButton("Option 3", callback_data="m3")],
    ]
    return InlineKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Submenu 1-1", callback_data="m1_1")],
        [InlineKeyboardButton("Submenu 1-2", callback_data="m1_2")],
        [InlineKeyboardButton("Main menu", callback_data="main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("Submenu 2-1", callback_data="m2_1")],
        [InlineKeyboardButton("Submenu 2-2", callback_data="m2_2")],
        [InlineKeyboardButton("Main menu", callback_data="main")],
    ]
    return InlineKeyboardMarkup(keyboard)


############################# Messages #########################################
def main_menu_message():
    return "Choose the option in main menu:"


def first_menu_message():
    return "Choose the submenu in first menu:"


def second_menu_message():
    return "Choose the submenu in second menu:"


"""Start the bot."""
# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(
    TOKEN,
    use_context=True
    # Get the dispatcher to register handlers
)
dp = updater.dispatcher
# on different commands - answer in Telegram

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(main_menu, pattern="main"))
dp.add_handler(CallbackQueryHandler(first_menu, pattern="m1"))
dp.add_handler(CallbackQueryHandler(second_menu, pattern="m2"))
dp.add_handler(CallbackQueryHandler(first_submenu, pattern="m1_1"))
dp.add_handler(CallbackQueryHandler(second_submenu, pattern="m2_1"))
# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))
# log all errors
dp.add_error_handler(error)
# Start the Bot
updater.start_polling()
# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()

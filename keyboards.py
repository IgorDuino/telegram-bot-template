from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton('Привет! 👋'))

    return keyboard

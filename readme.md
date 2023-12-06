# Telegram Bot Template

### Useful and multifunction bot template, which use aiogram
> based on https://github.com/rodion-gudz/telegram-bot-template, but in Docker, without pyrogram, with poetry, decouple, last versions and fixed migrations

![Telegram](https://img.shields.io/badge/Telegram-blue?style=flat&logo=telegram)
![CodeStyle](https://img.shields.io/badge/code%20style-black-black)

## Features
* ![aiogram 3](https://img.shields.io/badge/dev--3.x-aiogram-blue) as a main library
  resolve by username and list participants in a group
* ![aiogram-dialog](https://img.shields.io/badge/beta--2.x-aiogram__dialog-green) (Optional) for creating multi-step
  dialogs
* ☁️ Webhook and long polling with local Bot API server support
* 🎨 Beautiful and informative colored logs
* 🛠 Throttling and db middlewares by default
* 📝 Changing UI commands
* 👨🏻‍💻 Owner filter
* ℹ️ Demo usage of dialogs and inline queries

## Usage

* 📌 [Create](https://github.com/igorduino/telegram-bot-template/generate) and clone repo from this template
* 🔑 Rename `example.env` to `.env` and change bot settings
* 📎 Install requirements by `poetry install`
* 🚀 Run bot via `python main.py`

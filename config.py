from decouple import config


class Config:
    LOG_LEVEL = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30,
                 "INFO": 20, "DEBUG": 10}.get(config('LOG_LEVEL', default="WARNING"), 30)

    TOKEN = config('BOT_TOKEN')

    DB_HOST = config('DB_HOST')
    DB_PORT = config('POSTGRES_PORT')
    DB_USER = config('POSTGRES_USER')
    DB_PASS = config('POSTGRES_PASSWORD')
    DB_NAME = config('POSTGRES_DB')

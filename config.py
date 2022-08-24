from decouple import config


class Config:
    LOG_LEVEL = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30,
                 "INFO": 20, "DEBUG": 10}.get(config('LOG_LEVEL', default="WARNING"), 30)

    TOKEN = config('TOKEN')

    DB_HOST = config('DB_HOST')
    DB_PORT = config('DB_PORT')
    DB_USER = config('DB_USER')
    DB_PASS = config('DB_PASS')
    DB_NAME = config('DB_NAME')

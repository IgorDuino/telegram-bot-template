from decouple import config as c
from dataclasses import MISSING, dataclass, fields


bot_token = c("BOT_TOKEN")
owner_id = c("OWNER_ID", cast=int)

db_protocol = c("DB_PROTOCOL")
db_name = c("DB_NAME")
db_user = c("DB_USER")
db_pass = c("DB_PASS")
db_host = c("DB_HOST")
db_port = c("DB_PORT", cast=int)

db_url = f"{db_protocol}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

tortoise_config = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": ["db.functions", "aerich.models"],
            "default_connection": "default",
        },
    },
}

use_persistent_storage = c("USE_PERSISTENT_STORAGE", cast=bool, default=False)
redis_url = c("REDIS_URL") if use_persistent_storage else c("REDIS_URL", default="")

use_webhook = c("USE_WEBHOOK", cast=bool, default=False)
webhook_port = c("WEBHOOK_PORT", cast=int) if use_webhook else None
webhook_path = c("WEBHOOK_PATH") if use_webhook else None
webhook_url = c("WEBHOOK_URL") if use_webhook else None

throttling_rate = c("THROTTLING_RATE", cast=float, default=0.5)
drop_pending_updates = c("DROP_PENDING_UPDATES", cast=bool, default=False)

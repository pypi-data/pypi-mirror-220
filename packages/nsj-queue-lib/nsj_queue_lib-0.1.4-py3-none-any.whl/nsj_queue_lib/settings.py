import logging
import logging_loki
import os
import sys
import uuid

# Resolvendo as variáveis de ambiente
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_BASE = os.environ["DB_BASE"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]

QUEUE_NAME = os.environ["QUEUE_NAME"]
QUEUE_TABLE = os.environ["QUEUE_TABLE"]

QUEUE_MAX_RETRY = int(os.getenv("QUEUE_MAX_RETRY", "100"))
QUEUE_BASE_INTERVAL_RETRY = int(os.getenv("QUEUE_BASE_INTERVAL_RETRY", "5"))

QUEUE_MINUTE_RETRY_THREAD = os.getenv(
    "QUEUE_MINUTE_RETRY_THREAD", "0,5,10,15,20,25,30,35,40,45,50,55"
)
QUEUE_MINUTE_PURGE_THREAD = os.getenv("QUEUE_MINUTE_PURGE_THREAD", "0")
QUEUE_MINUTE_NOTIFY_THREAD = os.getenv(
    "QUEUE_MINUTE_NOTIFY_THREAD", "0,5,10,15,20,25,30,35,40,45,50,55"
)

QUEUE_PURGE_MAX_AGE = int(os.getenv("QUEUE_PURGE_MAX_AGE", "60"))
QUEUE_PURGE_LIMIT = int(os.getenv("QUEUE_PURGE_LIMIT", "1000"))

ENV = os.getenv("ENV", "DEV").upper()
GRAFANA_URL = os.getenv("GRAFANA_URL")
LOG_DEBUG = os.getenv("LOG_DEBUG", "False").upper() == "TRUE"

# Resolvendo as constantes e variáveis globais
WORKER_NAME = f"{QUEUE_NAME}_WORKER_{uuid.uuid4()}"
GLOBAL_RUN = True

# Configurando o logger
logger = logging.getLogger(WORKER_NAME)
if LOG_DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
if GRAFANA_URL is not None:
    loki_handler = logging_loki.LokiHandler(
        url=GRAFANA_URL,
        tags={ENV.upper() + "_flask_api_skeleton": ENV.lower() + "_log"},
        version="1",
    )

console_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler.setFormatter(console_format)

logger.addHandler(console_handler)
if GRAFANA_URL is not None:
    logger.addHandler(loki_handler)

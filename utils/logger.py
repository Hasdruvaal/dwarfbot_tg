"""
Logging module.

There are two ways of determine the source of log message:
1) By getting previous stack record from logger;
2) By getting class/module name based logger instance.

"""

from logging.config import dictConfig
import os
import json

defaultConfig = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)-12s [%(levelname)-5s] %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": "info.log",
            "maxBytes": 104857600,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "standard",
            "filename": "errors.log",
            "maxBytes": 104857600,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "default",
            "info_file_handler",
            "error_file_handler"
        ]
    }
}


def init_logging(configFilePath='config/logging.json'):
    path = configFilePath
    if os.path.exists(configFilePath):
        with open(path, 'rt') as configFile:
            config = json.load(configFile)
            dictConfig(config)
    else:
        dictConfig(defaultConfig)


import colorlog
import os
import sys
import logging
import traceback
import logging.config


logfile = 'fsimport.log'
loggingConf = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)-15s [%(levelname)-4s] %(name)s %(funcName)s:%(lineno)s - %(message)s",
        }
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
            "level": "ERROR"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": logfile,
            "backupCount": 3,
            "maxBytes": 10485760  # 10MB
        }
    },
    "loggers": {
        "": {
            "level": "ERROR",
            "handlers": ["file"],
        },
        "fsimport": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False
        }
    },
}
logging.config.dictConfig(loggingConf)

# special handling for console due to coloring
console = logging.StreamHandler()
console.setFormatter(colorlog.ColoredFormatter("%(levelname)8s %(log_color)s%(message)s%(reset)s"))
console.setLevel(logging.INFO)
logger = colorlog.getLogger('fsimport')
logger.addHandler(console)


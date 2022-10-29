""" General settings and configurations for the project """
# todo create local and general settings modules to create different settings for dev and prod
import os

# Project Details
from fileinput import filename

PROJECT_NAME = "OnlyTraders"
PROJECT_DESCRIPTION = "OnlyTraders API project"
PROJECT_VERSION = "1.0"

ALLOWED_HOSTS = ['*']

DEBUG = True

# Authentication
SECRET_KEY = "393e8ccc16ad95f541248f3ff582726ee916bb923488e6165a37a68fb96f631b"  # use command openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database Settings
DATABASES = {
    'default': {
        'USER': os.getenv("POSTGRES_USER", "postgres"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "dev123"),
        'SERVER': os.getenv("POSTGRES_SERVER", "127.0.0.1"),
        'PORT':  os.getenv("POSTGRES_PORT", 5432),
        'DB': os.getenv("POSTGRES_DB", "sample_db"),
    },
    'test': {
        'USER': "postgres",
        'PASSWORD': "dev123",
        'SERVER': "127.0.0.1",
        'PORT':  5432,
        'DB': "test_db",
    },
}

DB = DATABASES['test']

DATABASE_URL = f"postgresql://{DB['USER']}:{DB['PASSWORD']}@{DB['SERVER']}:{DB['PORT']}/{DB['DB']}"

# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": '%(asctime)s %(levelname)-8s %(name)s: %(message)s'
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.WatchedFileHandler",
            "formatter": "simple",
            "filename": "app.log"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "file"
        ]
    }
}

# Login Settings
LOGIN_URL = '/auth/login'

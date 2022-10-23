""" General settings and configurations for the project """
# todo create local and general settings modules to create different settings for dev and prod
import os

# Project Details
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
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "dev123")
POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "127.0.0.1")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sample_db")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Login Settings
LOGIN_URL = '/auth/login'

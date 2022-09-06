""" General settings and configurations for the project """
# todo create local and general settings modules to create different settings for dev and prod
import os

# Project Details
PROJECT_NAME = "OnlyTraders"
PROJECT_DESCRIPTION = "OnlyTraders API project"
PROJECT_VERSION = "1.0"


# Database Settings
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "dev123")
POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "127.0.0.1")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sample_db")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


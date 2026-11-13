"""Database settings, read from environment variables (or a local .env file).

Copy .env.example to .env and set your own values. .env is git-ignored,
so credentials never end up in the repository.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv is optional if variables are set another way
    pass

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "secure_pipeline")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD is not set. Copy .env.example to .env and fill it in.")

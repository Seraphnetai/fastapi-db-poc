"""Plik konfiguracyjny zawierający informacje o logowaniu, tagach itp."""

import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Opis usługi
APP_NAME = "fastapi-template"
API_TITLE = "fastapi-template"
API_SUMMARY = "fastapi-template - FastAPI template service"


# Logger
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)


# Tags
tags_metadata = [
    {"name": "test_endpoint", "description": "Test endpoint"},
    {"name": "health", "description": "Healthcheck"},
    {"name": "docs", "description": "App documentation"},
    {"name": "fetch", "description": "Fetch operation (GET) endpoints"},
    {"name": "list", "description": "List operation (GET) endpoints"},
    {"name": "get", "description": "Get operation (GET) endpoints"},
]

# Database

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Qdrant config
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")

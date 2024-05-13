"""Plik konfiguracyjny zawierający informacje o logowaniu, tagach itp."""

import logging


# Opis usługi
APP_NAME = "articles_tags"
API_TITLE = "articles-tags"
API_SUMMARY = "articles-tags"


# Logger
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)


# Tagi
tags_metadata = [
    {"name": "test_endpoint", "description": "Opis testowego endpointa"},
    {"name": "health", "description": "Sprawdzanie kondycji aplikacji"},
    {"name": "docs", "description": "Dokumentacja aplikacji"},
]

"""Модуль описания конфигурации приложения coins."""

from django.apps import AppConfig


class CoinsConfig(AppConfig):
    """Класс описания настроек."""

    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'apps.coins'

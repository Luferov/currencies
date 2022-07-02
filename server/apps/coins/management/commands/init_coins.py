"""Модуль для загрузки курса валют."""

from apps.coins.models import Rate
from apps.coins.services import get_rates
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда инициализации."""

    help: str = 'Инициализация валют'

    def handle(self, *args, **kwargs) -> None:
        """Функция вызова команды для инициализации."""
        rates: list[dict[str, str | int]] = get_rates()
        Rate.objects.bulk_create([
            Rate(**rate) for rate in rates
        ])
        self.stdout.write('Инициализация валют.')

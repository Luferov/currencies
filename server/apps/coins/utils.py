"""Модуль со вспомогательными функциями."""

from random import choice
from string import ascii_letters


def random_string(count: int) -> str:
    """Генерация случайной строки из count."""
    return ''.join(choice(ascii_letters) for _ in range(count))

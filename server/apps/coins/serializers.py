"""Сериализация моделей для API."""

from apps.coins.models import Rate, Value
from rest_framework import serializers


class RateSerializer(serializers.ModelSerializer):
    """Класс сериализации валют."""

    class Meta:
        """Метакласс настроек."""

        model = Rate
        fields = '__all__'


class ValueSerializer(serializers.ModelSerializer):
    """Класс сериализации валютных значений."""

    rate = RateSerializer()

    class Meta:
        """Метакласс настроек."""

        model = Value
        fields = '__all__'

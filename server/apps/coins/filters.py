"""Список фильтров."""

import django_filters
from apps.coins.models import Value


class ValueFilter(django_filters.FilterSet):
    """Фильтр по значениям."""

    rate__code: django_filters.BaseInFilter = django_filters.BaseInFilter(field_name='rate__code')

    class Meta:
        """Метакласс настроек."""

        model = Value
        fields = ('date',)

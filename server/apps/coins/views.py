"""Модуль для описания запросов."""

from apps.coins.filters import ValueFilter
from apps.coins.models import Rate, Value
from apps.coins.serializers import RateSerializer, ValueSerializer
from apps.coins.services import get_rates_actual_date, write_values_to_file
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response


class RateListView(ListAPIView):
    """Вьюха для получения списка доступных валют."""

    serializer_class = RateSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self) -> QuerySet[Rate]:
        """Построения queryset для выбираемой даты."""
        date = get_rates_actual_date(self.request.query_params.get('date') if self.request else None)
        rates_id: list[int] = Value.objects.filter(date=date).values_list('rate_id', flat=True)
        return Rate.objects.filter(pk__in=rates_id)


class ValueListVIew(ListAPIView):
    """Вьюха для просмотра котировок курсов валют."""

    serializer_class = ValueSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ValueFilter
    permission_classes = (AllowAny,)

    def get_queryset(self) -> QuerySet[Value]:
        """Формируем выборку для ответа."""
        date = get_rates_actual_date(self.request.query_params.get('date') if self.request else None)
        return Value.objects.select_related('rate').filter(date=date.date())


@api_view(['post'])
def unload_file(request: Request, file_type: str = 'csv') -> Response:
    """POST запрос для выгрузки файлов."""
    codes: str | None = request.data.get('codes')
    if codes is None:
        raise ValidationError('Необходимо указать код(ы) валют.')
    src: str = write_values_to_file(
        codes=codes.split(','),
        str_date=request.data.get('date'),
        writer_type=file_type
    )
    return Response({'src': f'/{src}'})

"""Модуль, содержащий сервисы."""

import xml.etree.ElementTree as ETree
from datetime import date, datetime
from pathlib import PosixPath

import requests
from apps.coins.helpers.coin_writer import ContainerWriter, HeaderOption, HeaderOptions, Writers
from apps.coins.models import Rate, Value
from apps.coins.utils import random_string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone


def get_rates() -> list[dict[str, str | int]]:
    """Функция для получения доступных валют."""
    keys: dict[str, str] = {
        'Name': 'name',
        'Nominal': 'nominal',
        'ParentCode': 'code'
    }
    url: str = settings.EXTERNAL_URLS['rates']
    response = requests.get(url)    # noqa
    rates_path: PosixPath = settings.BASE_DIR / 'apps' / 'coins' / 'management' / 'seed' / 'rates.xml'
    if response.status_code != 200:
        with open(rates_path) as f:
            content: str = f.read()
    else:
        content: str = response.text
        with open(rates_path, 'w+') as f:
            f.write(content)
    root: ETree = ETree.fromstring(content)
    rates: list[dict[str, str | int]] = [
        {
            keys[element.tag]: element.text.strip() for element in item if element.tag in keys
        } for item in root.findall('Item')
    ]
    return rates


def get_values_actual_date(str_data: str | None = None) -> datetime:
    """Возвращаем дату из фильтра, но не раньше сегодняшней."""
    now: datetime = timezone.now()
    current_date: datetime = timezone.make_aware(datetime.strptime(str_data, '%m/%d/%Y')) \
        if str_data \
        else timezone.now()
    return current_date if current_date <= now else now


def get_values(d: date) -> None:
    """Проверяем наличие записей в БД или подгружаем по API."""
    count: int = Value.objects.filter(date=d).count()
    if count == 0:
        keys: dict[str, str] = {
            'NumCode': 'num_code',
            'CharCode': 'char_code',
            'Value': 'value',
        }
        url: str = settings.EXTERNAL_URLS['coins'] % d.strftime('%d/%m/%Y')
        response = requests.get(url)
        if response.status_code != 200:
            return
        rates: dict[str, int] = {rate['code']: rate['id'] for rate in Rate.objects.values('id', 'code')}
        root: ETree = ETree.fromstring(response.text)
        current_date: datetime = datetime\
            .strptime(root.attrib.get('Date', d.strftime('%d.%m.%Y')), '%d.%m.%Y')
        with transaction.atomic():
            for coin in root.findall('Valute'):
                rate_id: str | None = rates.get(coin.attrib['ID'])
                if rate_id is None:
                    continue
                value: dict[str, str] = {
                    keys[element.tag]: element.text.strip()
                    if element.tag != 'Value'
                    else float(element.text.strip().replace(',', '.'))
                    for element in coin if element.tag in keys
                }
                Value.objects.update_or_create(date=current_date, rate_id=rate_id, defaults=value)


def get_rates_actual_date(str_data: str | None = None) -> datetime:
    """Сервис для получения списка котировок от центробанка."""
    d: datetime = get_values_actual_date(str_data)
    get_values(d.date())
    return d


def write_values_to_file(codes: list[str], str_date: str | None, writer_type: str = 'csv') -> str:
    """Запись в файл результатов."""
    if writer_type not in [w.value for w in Writers]:
        raise ValidationError(f'Тип {writer_type} не в списке разрешенных: {",".join(w.value for w in Writers)}')
    # client/components/views/CoinsView.vue # noqa
    headers: list[HeaderOptions] = [
        HeaderOptions('rate__code', HeaderOption('Код', str)),
        HeaderOptions('rate__name', HeaderOption('Название', str)),
        HeaderOptions('value', HeaderOption('Цена', float)),    # Нужно было сделать Decimal
        HeaderOptions('date', HeaderOption('Дата', date)),
        HeaderOptions('rate__nominal', HeaderOption('Номинал', int)),
        HeaderOptions('num_code', HeaderOption('Код валюты', int)),
        HeaderOptions('char_code', HeaderOption('Символьный код валюты', str)),
    ]
    current_date: datetime = get_values_actual_date(str_date)
    path_file = settings.DOCUMENTS_DIR / f'{timezone.now().strftime("%Y-%m-%d")}_{random_string(10)}.{writer_type}'
    container: ContainerWriter = ContainerWriter(headers, path_file, Writers(writer_type))
    values = Value.objects.filter(date=current_date, rate__code__in=codes).values(*[header.code for header in headers])
    container.write_dict(values)
    return container.relpath

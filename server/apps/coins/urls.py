"""Пути для приложения coins."""

from apps.coins.views import RateListView, ValueListVIew, unload_file
from django.urls import path

urlpatterns = [
    path('rates/', RateListView.as_view()),
    path('values/', ValueListVIew.as_view()),
    path('unload/<str:file_type>/', unload_file),
]

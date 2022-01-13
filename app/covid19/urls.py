from django.urls import path, include
from .views import (
    Covid19EntryListView,
    Covid19EntryCreateView,
    Covid19EntryDetailView,
    Covid19EntryUpdateView,
    Covid19EntryDeleteView
)
from . import views


app_name = 'covid19'

urlpatterns = [
    #path('clear_entries/', views.clear_entries, name='clear_covid19_entries'),
    path('entries/', Covid19EntryListView.as_view(), name='covid19_entries'),
    path('entry/<int:pk>/', Covid19EntryDetailView.as_view(), name='covid19_entry_detail'),
    path('entry/new/', Covid19EntryCreateView.as_view(), name='covid19_entry_create'),
    path('entry/<int:pk>/update/', Covid19EntryUpdateView.as_view(), name='covid19_entry_update'),
    path('entry/<int:pk>/delete/', Covid19EntryDeleteView.as_view(), name='covid19_entry_delete'),
]

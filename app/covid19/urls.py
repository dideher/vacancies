from django.urls import path
from .views import (
    Covid19EntryListView,
    Covid19EntryCreateView,
    Covid19EntryUpdateView,
    Covid19EntryDeleteView,
    export_covid19_entries
)

app_name = 'covid19'

urlpatterns = [
    path('entries/', Covid19EntryListView.as_view(), name='covid19_entries'),
    path('entry/new/', Covid19EntryCreateView.as_view(), name='covid19_entry_create'),
    path('entry/<int:pk>/update/', Covid19EntryUpdateView.as_view(), name='covid19_entry_update'),
    path('entry/<int:pk>/delete/', Covid19EntryDeleteView.as_view(), name='covid19_entry_delete'),
    path('export_entries_xls/', export_covid19_entries, name='covid19_export_entries_xls'),
]

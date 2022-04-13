from django.urls import path, include
from .views import (
    EntriesListView,
    EntriesVacanciesListView,
    EntriesSurplusListView,
    UserEntriesListView,
    EntryDetailView,
    EntryCreateView,
    EntryUpdateView,
    EntryDeleteView,
    SpecialtiesListView,
)
from . import views


app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('clear_entries/', views.clear_entries, name='clear_entries'),
    path('entries/', EntriesListView.as_view(), name='entries'),
    path('entries_vacancies/', EntriesVacanciesListView.as_view(), name='entries_vacancies'),
    path('entries_surplus/', EntriesSurplusListView.as_view(), name='entries_surplus'),
    path('user_entries/', UserEntriesListView.as_view(), name='user_entries'),
    path('entry/<int:pk>/', EntryDetailView.as_view(), name='entry_detail'),
    path('entry/new/', EntryCreateView.as_view(), name='entry_create'),
    path('entry/<int:pk>/update/', EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', EntryDeleteView.as_view(), name='entry_delete'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('specialties/', SpecialtiesListView.as_view(), name='specialties'),
]

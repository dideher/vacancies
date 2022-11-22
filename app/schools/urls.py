from django.urls import path
from . import views
from .views import SchoolsListView, SchoolDetailView


app_name = 'schools'

urlpatterns = [
    path('check_schools/', views.check_schools, name='check_schools'),
    path('schools/', SchoolsListView.as_view(), name='schools'),
    path('school/<int:pk>/', SchoolDetailView.as_view(), name='school_detail'),
    path('status_update/', views.status_update, name='status_update'),
    path('check_status/', views.check_status, name='check_status'),
    path('clear_status/', views.clear_status, name='clear_status'),
]
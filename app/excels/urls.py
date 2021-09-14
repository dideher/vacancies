from django.urls import path
from . import views


app_name = 'excels'

urlpatterns = [
    path('upload_schools/', views.upload_schools, name='upload_schools'),
    path('add_schools/', views.add_schools, name='add_schools'),
    path('upload_specialties/', views.upload_specialties, name='upload_specialties'),
    path('add_specialties/', views.add_specialties, name='add_specialties'),
    path('excel_entries/', views.excel_entries, name='excel_entries'),
    path('excel_aggregated_entries/', views.excel_aggregated_entries, name='excel_aggregated_entries'),
    path('excel_history/', views.excel_history, name='excel_history'),
    path('excel_user_history/', views.excel_user_history, name='excel_user_history'),
]

from django.urls import path
from .views import HistoryListView, UserHistoryListView
from . import views


app_name = 'history'

urlpatterns = [
    path('history/', HistoryListView.as_view(), name='history'),
    path('clear_history/', views.clear_history, name='clear_history'),
    path('user_history/', UserHistoryListView.as_view(), name='user_history'),
]

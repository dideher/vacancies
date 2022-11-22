from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserAuthenticationView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('info/', views.info, name='info'),
    path('login/', UserAuthenticationView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

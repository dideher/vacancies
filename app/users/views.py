from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserRegisterForm
from django.contrib.auth.views import LoginView
from .forms import UserAuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

@transaction.atomic
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ο χρήστης "{username}" δημιουργήθηκε με επιτυχία.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def info(request):
    if request.user.is_superuser:
        return render(request, 'main_app/home.html')
    else:
        user: User = request.user
        user_profile: Profile = user.profile

        return render(request, 'users/info.html')


class UserAuthenticationView(LoginView):
    authentication_form = UserAuthenticationForm

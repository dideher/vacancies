from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from .models import School
from users.models import Profile


class SchoolDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = School

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        return False


class SchoolsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = School
    template_name = 'schools/schools.html'
    context_object_name = 'schools'
    ordering = ['id']
    paginate_by = 10

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        return False


def check_schools(request):
    if request.user.is_superuser:
        superusers = User.objects.filter(is_superuser=True)
        p_verified_users = Profile.objects.filter(verified=True).exclude(user__in=superusers)
        p_not_verified_users = Profile.objects.filter(verified=False).exclude(user__in=superusers)
        not_connected_schools = School.objects.filter(connected_to_user=False)

        return render(request, 'schools/check_schools.html', {'p_verified_users': p_verified_users,
                                                              'p_not_verified_users': p_not_verified_users,
                                                              'not_connected_schools': not_connected_schools,
                                                              })
    else:
        return render(request, 'main_app/error.html', {})


def status_update(request):
    if request.method == 'POST':
        request.user.profile.status = True
        request.user.profile.save()

        return redirect('users:info')
    else:
        if request.user.profile.verified:
            return render(request, 'schools/status_update.html', {})
        else:
            return render(request, 'main_app/not_verified.html', {})


def check_status(request):
    if request.user.is_superuser:
        superusers = User.objects.filter(is_superuser=True)
        p_status_true = Profile.objects.filter(status=True).exclude(user__in=superusers)
        u_status_false = User.objects.filter(profile__status=False).exclude(pk__in=superusers).exclude(profile__verified=False)
        s_status_false = School.objects.filter(email__in=[u.email for u in u_status_false])
        # u_status_true = User.objects.filter(profile__status=True).exclude(pk__in=superusers).exclude(profile__verified=False)
        # s_status_true = School.objects.filter(email__in=[u.email for u in u_status_true])
        
        return render(request, 'schools/check_status.html', {'p_status_true': p_status_true,
                                                             's_status_false': s_status_false,
                                                             })
    else:
        return render(request, 'main_app/error.html', {})


def clear_status(request):
    if request.method == 'POST':
        Profile.objects.all().update(status=False)
        return redirect('schools:check_status')
    else:
        if request.user.is_superuser:
            return render(request, 'schools/clear_status.html')
        else:
            return render(request, 'main_app/error.html')

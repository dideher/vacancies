import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic import ListView, DetailView
from .models import School
from users.models import Profile
from main_app.models import Entry
from vacancies.utils.permissions import check_user_is_superuser


class SchoolDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = School

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.object is not None:
            current_school: School = self.object

            try:
                managed_by: Profile = current_school.managed_by
                data['is_finalized'] = managed_by.status is True
                data['finalized_on'] = managed_by.status_time
            except School.managed_by.RelatedObjectDoesNotExist:
                data['is_finalized'] = False
                data['finalized_on'] = None

            data['school_entries'] = Entry.objects.filter(school=current_school).order_by('specialty')
        return data

    def test_func(self):
        return check_user_is_superuser(self.request.user)


class SchoolsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = School
    template_name = 'schools/schools.html'
    context_object_name = 'schools'
    ordering = ['name']
    paginate_by = 10

    def test_func(self):
        return check_user_is_superuser(self.request.user)


@login_required
@user_passes_test(check_user_is_superuser)
def check_schools(request):

    superusers = User.objects.filter(is_superuser=True)
    p_verified_users = Profile.objects.filter(verified=True).exclude(user__in=superusers)
    p_not_verified_users = Profile.objects.filter(verified=False).exclude(user__in=superusers)
    not_connected_schools = School.objects.filter(managed_by=None)

    return render(request, 'schools/check_schools.html', {'p_verified_users': p_verified_users,
                                                          'p_not_verified_users': p_not_verified_users,
                                                          'not_connected_schools': not_connected_schools,
                                                          })


@login_required
def status_update(request):
    if request.method == 'POST':
        request.user.profile.status = True
        request.user.profile.status_time = timezone.now()
        request.user.profile.save()

        return redirect('users:info')
    else:
        if request.user.profile.verified:
            return render(request, 'schools/status_update.html', {})
        else:
            return render(request, 'main_app/not_verified.html', {})


@login_required
@user_passes_test(check_user_is_superuser)
def check_status(request):

    # superusers = User.objects.filter(is_superuser=True)
    # p_status_true = Profile.objects.filter(status=True).exclude(user__in=superusers)
    # u_status_false = User.objects.filter(profile__status=False).exclude(pk__in=superusers).exclude(profile__verified=False)
    # s_status_false = School.objects.filter(email__in=[u.email for u in u_status_false])
    # s_status_false = School.objects.filter(email__in=[u.email for u in u_status_false])
    s_status_true = School.objects.filter(managed_by__status=True).order_by('-managed_by__status_time')
    s_status_false = School.objects.filter(managed_by__status=False).order_by('name')

    return render(request, 'schools/check_status.html', {'s_status_true': s_status_true,
                                                         's_status_false': s_status_false,
                                                         })


@login_required
@user_passes_test(check_user_is_superuser)
def clear_status(request):
    if request.method == 'POST':
        Profile.objects.all().update(status=False, status_time=None)
        return redirect('schools:check_status')
    else:
        return render(request, 'schools/clear_status.html')


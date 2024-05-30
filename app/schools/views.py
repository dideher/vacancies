import datetime
import logging
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.mail import BadHeaderError, send_mail, send_mass_mail
from django.conf import settings
from tabulate import tabulate
from constance import config
from django.utils import timezone
from django.utils.formats import date_format
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic import ListView, DetailView
from .models import School
from users.models import Profile, User
from main_app.models import Entry, EntryVariantType

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

        user: User = request.user
        profile: Profile = user.profile
        school: School = profile.school
        utc_now = timezone.now()
        logging.info("school '%s' is trying to confirm data", school)

        profile.status = True
        profile.status_time = utc_now
        profile.save()
        if config.SEND_FINALIZATION_EMAILS is True:
            try:

                user_model_class = get_user_model()
                users = user_model_class.objects.filter(is_superuser=True)

                recipient_list = [user.email for user in users]
                logging.info("we will also notify via email the following users : %s", recipient_list)

                entries = Entry.objects.filter(school=school).order_by('specialty')
                headers = ['Ειδικότητα', 'Τύπος', 'Είδος', 'Ώρες']
                values = [(f'{entry.specialty.code} - {entry.specialty.lectic}', entry.type,
                           str(EntryVariantType(entry.variant).label), entry.hours) for entry in entries]

                entries_table = tabulate(tabular_data=values, headers=headers, tablefmt='simple_grid')
                status_time_localized = date_format(profile.status_time, format='SHORT_DATETIME_FORMAT', use_l10n=True)
                subject = f'{settings.EMAIL_SUBJECT_PREFIX}- Επικαιροποίηση Σχολικής Μονάδας \'{school.name}\''
                message = f'Σας ενημερώνουμε πως η σχολική μονάδα \'{school.name}\' επικαιροποιήθηκε επιτυχώς απο ' \
                          f'τον χρήστη \'{user.username}\' ως προς τα κενά και τα πλεονάσματά της στις ' \
                          f'\'{status_time_localized}\'.\n\n Τα επικαιροποιημένα στοιχεία κενών/πλεονασμάτων της μονάδας ' \
                          f'είναι τα παρακάτω :\n\n' + entries_table + f'\n\n\nΗ ειδοποίηση είναι μια αυτοματοποίηση ' \
                                                                       'του τμήματος Δ\' της ΔΔΕ Ηρακλείου'

                for recipient in recipient_list:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        fail_silently=True,
                        recipient_list=(recipient, )
                    )

            except Exception as e:
                logging.error("failed to notify users via email due to '%s'", str(e))
        else:
            logging.info("SEND_FINALIZATION_EMAILS is false, not sending finalization update")

        logging.info("school '%s' successfully confirmed data on '%s'", school, utc_now)

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


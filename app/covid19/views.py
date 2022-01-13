from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from shared import check_user_is_school
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Covid19Entry, Covid19EntryEventHistory
from .forms import Covid19EntryCreateForm, Covid19EntryUpdateForm
from users.models import Profile
from vacancies.commons import EntryHistoryEventType


class Covid19EntryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Covid19Entry
    context_object_name = 'entries'
    paginate_by = 10

    def test_func(self):
        return check_user_is_school(self.request.user)

    def get_queryset(self):

        user_profile: Profile = self.request.user.profile

        return Covid19Entry.objects.filter(school=user_profile.school, deleted_on__isnull=True).order_by('specialty__code')


class Covid19EntryDetailView(LoginRequiredMixin, DetailView):
    model = Covid19Entry


class Covid19EntryCreateView(LoginRequiredMixin, CreateView):
    model = Covid19Entry
    form_class = Covid19EntryCreateForm

    success_url = '/user_entries/'

    def get_form_kwargs(self):
        # kwargs = super(EntryCreateView, self).get_form_kwargs()
        # # https://stackoverflow.com/questions/32260785/django-validating-unique-together-constraints-in-a-modelform-with-excluded-fiel
        # current_user = self.request.user
        # user_profile = current_user.profile
        # kwargs['instance'] = Entry(owner=current_user, school=user_profile.school)
        # kwargs['user'] = current_user
        #
        # return kwargs
        return None

    def form_valid(self, form):
        # Setting form.instance.user in form_valid is too late, because the
        # form has already been validated by then.
        #form.instance.owner = self.request.user
        self.request.user.profile.status = False
        self.request.user.profile.status_time = None
        self.request.user.profile.save()
        return super().form_valid(form)


class Covid19EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Covid19Entry

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            entry_to_delete: Covid19Entry = self.get_object()
            deleted_datetime = timezone.now()
            self.request.user.profile.status = False
            self.request.user.profile.status_time = None
            self.request.user.profile.save()

            Covid19EntryEventHistory.objects.create(
                covid_entry=entry_to_delete,
                created_by=self.request.user,
                event_datetime=deleted_datetime,
                event_type=EntryHistoryEventType.HISTORY_EVENT_DELETE,
                event_description=f"H εγγραφή '{entry_to_delete}' διαγράφηκε"
            )

            entry_to_delete.deleted_on = deleted_datetime
            entry_to_delete.save()

            messages.success(self.request, "Η διαγραφή του κενού COVID-19 ήταν επιτυχής")

        return HttpResponseRedirect(reverse('covid19:covid19_entries'))

    def test_func(self):
        # entry = self.get_object()
        #
        # if self.request.user == entry.owner:
        #     return True
        #
        # return False
        return True


class Covid19EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Covid19Entry
    form_class = Covid19EntryUpdateForm
    template_name = 'main_app/entry_update.html'
    context_object_name = 'entry'

    success_url = '/user_entries/'

    def form_valid(self, form):
        original_data = self.get_object()
        self.request.user.profile.status = False
        self.request.user.profile.status_time = None
        self.request.user.profile.save()
        # HistoryEntry.objects.create(specialty=original_data.specialty, owner=original_data.owner,
        #                             hours=original_data.hours, date_time=original_data.date_time,
        #                             type=original_data.type,
        #                             description=original_data.description, variant=original_data.variant)

        return super().form_valid(form)

    def test_func(self):
        entry = self.get_object()

        if self.request.user == entry.owner:
            return True

        return False

from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
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
from vacancies.utils.view import UserIsAssociatedWithASchoolTestMixin


class Covid19EntryListView(LoginRequiredMixin, UserIsAssociatedWithASchoolTestMixin, ListView):
    model = Covid19Entry
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):

        user_profile: Profile = self.request.user.profile
        base_qs = super(Covid19EntryListView, self).get_queryset()
        return base_qs.filter(school=user_profile.school, deleted_on__isnull=True).order_by('specialty__code')


class Covid19EntryCreateView(LoginRequiredMixin, UserIsAssociatedWithASchoolTestMixin, CreateView):
    model = Covid19Entry
    form_class = Covid19EntryCreateForm

    success_url = reverse_lazy('covid19:covid19_entries')

    def get_form_kwargs(self):
        kwargs = super(Covid19EntryCreateView, self).get_form_kwargs()
        # https://stackoverflow.com/questions/32260785/django-validating-unique-together-constraints-in-a-modelform-with-excluded-fiel
        current_user = self.request.user
        user_profile = current_user.profile
        kwargs['instance'] = Covid19Entry(created_by=current_user, school=user_profile.school)
        kwargs['user'] = current_user

        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            
            created_datetime = timezone.now()

            current_user: User = self.request.user
            current_user.profile.status = False
            current_user.profile.status_time = None
            current_user.profile.save()
            
            covid19entry: Covid19Entry = form.instance
            covid19entry.save()
                        
            Covid19EntryEventHistory.objects.create(
                covid_entry=covid19entry,
                created_by=self.request.user,
                event_datetime=created_datetime,
                event_type=EntryHistoryEventType.HISTORY_EVENT_INSERT,
                event_description=f"H εγγραφή '{covid19entry}' καταχωρήθηκε"
            )

            messages.success(self.request, f'To κενό COVID-19 \'{covid19entry}\' καταχωρήθηκε με επιτυχία')

            return super().form_valid(form)


class Covid19EntryDeleteView(LoginRequiredMixin, UserIsAssociatedWithASchoolTestMixin, DeleteView):

    model = Covid19Entry

    def get_queryset(self):
        base_qs = super(Covid19EntryDeleteView, self).get_queryset()
        return base_qs.filter(school=self.request.user.profile.school, deleted_on__isnull=True)

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


class Covid19EntryUpdateView(LoginRequiredMixin, UserIsAssociatedWithASchoolTestMixin, UpdateView):
    model = Covid19Entry
    form_class = Covid19EntryUpdateForm
    context_object_name = 'entry'
    template_name_suffix = '_update_form'

    success_url = reverse_lazy('covid19:covid19_entries')

    def get_queryset(self):
        base_qs = super(Covid19EntryUpdateView, self).get_queryset()
        return base_qs.filter(school=self.request.user.profile.school, deleted_on__isnull=True)

    def form_valid(self, form):

        original_data = self.get_object()
        updated_data = form.instance

        self.request.user.profile.status = False
        self.request.user.profile.status_time = None
        self.request.user.profile.save()

        updated_datetime = timezone.now()

        Covid19EntryEventHistory.objects.create(
            covid_entry=original_data,
            created_by=self.request.user,
            event_datetime=updated_datetime,
            event_type=EntryHistoryEventType.HISTORY_EVENT_UPDATE,
            event_description=f"H εγγραφή '{original_data}' τροποποιήθηκε σε '{updated_data}'"
        )

        messages.success(self.request, "Η ενημέρωση του κενού COVID-19 ήταν επιτυχής")

        return super().form_valid(form)



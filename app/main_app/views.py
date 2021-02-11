from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Specialty, Entry
from .forms import EntryCreateForm, EntryUpdateForm
from history.models import HistoryEntry


class SpecialtiesListView(ListView):
    model = Specialty
    template_name = 'main_app/specialties.html'
    context_object_name = 'specialties'
    paginate_by = 10

    def get_queryset(self):
        return Specialty.objects.all().order_by('code')


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry

    success_url = '/user_entries/'

    def delete(self, *args, **kwargs):
        original_data = self.get_object()
        self.request.user.profile.status = False
        self.request.user.profile.save()
        HistoryEntry.objects.create(specialty=original_data.specialty, owner=original_data.owner,
                                    hours=original_data.hours, date_time=original_data.date_time,
                                    type=original_data.type,
                                    description=original_data.description, variant=original_data.variant)

        return super(EntryDeleteView, self).delete(*args, **kwargs)

    def test_func(self):
        entry = self.get_object()

        if self.request.user == entry.owner:
            return True

        return False


class EntriesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Entry
    template_name = 'main_app/entries.html'
    context_object_name = 'entries'
    ordering = ['specialty', 'owner']
    paginate_by = 10

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class EntriesVacanciesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Entry
    template_name = 'main_app/entries_vacancies.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(type='Κενό', hours__gt=0).order_by('specialty', 'owner')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class EntriesSurplusListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Entry
    template_name = 'main_app/entries_surplus.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(type='Πλεόνασμα', hours__gt=0).order_by('specialty', 'owner')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class UserEntriesListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'main_app/user_entries.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user).order_by('specialty')


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryCreateForm

    success_url = '/user_entries/'

    def get_form_kwargs(self):
        kwargs = super(EntryCreateView, self).get_form_kwargs()
        # https://stackoverflow.com/questions/32260785/django-validating-unique-together-constraints-in-a-modelform-with-excluded-fiel
        kwargs['instance'] = Entry(owner=self.request.user)
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        # Setting form.instance.user in form_valid is too late, because the 
        # form has already been validated by then.
        #form.instance.owner = self.request.user
        self.request.user.profile.status = False
        self.request.user.profile.save()

        return super().form_valid(form)

class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    form_class = EntryUpdateForm
    template_name = 'main_app/entry_update.html'
    context_object_name = 'entry'

    success_url = '/user_entries/'

    def form_valid(self, form):
        original_data = self.get_object()
        self.request.user.profile.status = False
        self.request.user.profile.save()
        HistoryEntry.objects.create(specialty=original_data.specialty, owner=original_data.owner,
                                    hours=original_data.hours, date_time=original_data.date_time,
                                    type=original_data.type,
                                    description=original_data.description, variant=original_data.variant)

        return super().form_valid(form)

    def test_func(self):
        entry = self.get_object()

        if self.request.user == entry.owner:
            return True

        return False


def about(request):
    return render(request, 'main_app/about.html', {'title': 'Σχετικά'})


def home(request):
    return render(request, 'main_app/home.html', {'title': 'Αρχική'})

def help(request):
    return render(request, 'main_app/help.html', {'title': 'Εγχειρίδιο Χρήσης'})

def clear_entries(request):
    if request.method == 'POST':
        Entry.objects.all().delete()
        return redirect('main_app:entries')
    else:
        if request.user.is_superuser:
            return render(request, 'main_app/clear_entries.html')
        else:
            return render(request, 'main_app/error.html')

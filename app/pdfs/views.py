from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from main_app.models import Entry
from django_xhtml2pdf.views import PdfMixin
from history.models import HistoryEntry
from users.models import Profile


class PdfUserEntries(PdfMixin, LoginRequiredMixin, ListView):
    template_name = 'pdfs/pdf_user_entries.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user).order_by('specialty')


class PdfEntries(PdfMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'pdfs/pdf_entries.html'
    context_object_name = 'entries'

    def get_queryset(self):
        entries = list()
        for p in Profile.objects.filter(verified=True):
            ue = Entry.objects.filter(owner=p.user)

            entries.append([p, ue])

        return entries

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        return False


class PdfHistory(PdfMixin, LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'pdfs/pdf_history.html'
    context_object_name = 'history'

    def get_queryset(self):
        history = list()
        for p in Profile.objects.filter(verified=True):
            uh = HistoryEntry.objects.filter(owner=p.user)

            history.append([p, uh])

        return history

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        return False


class PdfUserHistory(PdfMixin, LoginRequiredMixin, ListView):
    template_name = 'pdfs/pdf_user_history.html'
    context_object_name = 'history'

    def get_queryset(self):
        return HistoryEntry.objects.filter(owner=self.request.user).order_by('owner')

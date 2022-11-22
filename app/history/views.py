from .models import HistoryEntry
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect


class HistoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = HistoryEntry
    template_name = 'history/history.html'
    context_object_name = 'history'
    ordering = ['owner', 'specialty']
    paginate_by = 10

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        return False


class UserHistoryListView(LoginRequiredMixin, ListView):
    model = HistoryEntry
    template_name = 'history/user_history.html'
    context_object_name = 'history'
    paginate_by = 10

    def get_queryset(self):
        return HistoryEntry.objects.filter(owner=self.request.user).order_by('date_time')


def clear_history(request):
    if request.method == 'POST':
        HistoryEntry.objects.all().delete()

        return redirect('history:history')
    else:
        if request.user.is_superuser:
            return render(request, 'history/clear_history.html')
        else:
            return render(request, 'main_app/error.html')

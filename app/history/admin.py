from django.contrib import admin
from .models import HistoryEntry


@admin.register(HistoryEntry)
class HistoryEntryAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'owner', 'hours', 'type', 'description', 'date_time')
    list_filter = ('specialty', 'owner', 'hours', 'type')
    ordering = ('type', 'specialty', 'owner')


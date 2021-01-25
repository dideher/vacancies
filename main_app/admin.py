from django.contrib import admin
from .models import Specialty, Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'owner', 'hours', 'type', 'priority', 'description', 'date_time')
    list_filter = ('specialty', 'owner', 'hours', 'type', 'priority')
    ordering = ('type', 'specialty', 'owner')


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('code', 'lectic')
    search_fields = ('code', 'lectic')
    ordering = ('code', )

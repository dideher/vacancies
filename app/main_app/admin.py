from django.contrib import admin
from .models import Specialty, Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'owner', 'hours', 'type', 'description', 'date_time')
    list_filter = ('specialty', 'owner', 'hours', 'type')
    ordering = ('type', 'specialty', 'owner')


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('ordering', 'code', 'lectic', 'label', 'active')
    search_fields = ('code', 'lectic', 'label')
    ordering = ('ordering', )

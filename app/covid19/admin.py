from django.contrib import admin
from .models import Covid19Entry, Covid19EntryEventHistory


@admin.register(Covid19Entry)
class Covid19EntryAdmin(admin.ModelAdmin):
    list_display = ('teacher_registry', 'teacher_surname', 'teacher_name', 'specialty', 'hours', 'created_on', 'deleted_on')
    # list_filter = ('managed_by', 'school_group')
    # ordering = ('school_group', 'managed_by', 'name')


@admin.register(Covid19EntryEventHistory)
class Covid19EntryEventHistoryAdmin(admin.ModelAdmin):
    #list_display = ('name', )
    pass

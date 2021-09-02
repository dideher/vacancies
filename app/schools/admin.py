from django.contrib import admin
from .models import School, SchoolGroup


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('school_group', 'name', 'email', 'managed_by')
    list_filter = ('managed_by', 'school_group')
    ordering = ('school_group', 'managed_by', 'name')


@admin.register(SchoolGroup)
class SchoolGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )

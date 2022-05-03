from django.contrib import admin
from .models import School, SchoolGroup


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('ministry_code', 'name', 'school_group', 'sibling_school', 'email', 'school_type', 'managed_by')
    list_filter = ('managed_by', 'school_group', 'school_type')
    ordering = ('school_group', 'managed_by', 'name')


@admin.register(SchoolGroup)
class SchoolGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'neighboring_tag', 'ordering')
    ordering = ('ordering', )

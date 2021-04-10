from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'managed_by')
    list_filter = ('managed_by', )
    ordering = ('managed_by', 'name')

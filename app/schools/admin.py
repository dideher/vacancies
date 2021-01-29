from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'connected_to_user')
    list_filter = ('connected_to_user', )
    ordering = ('connected_to_user', 'name')

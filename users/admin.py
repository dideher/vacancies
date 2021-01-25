from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'verified', 'status', 'status_time')
    list_filter = ('verified', 'status')
    ordering = ('verified', 'status')

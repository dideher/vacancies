from django import forms
from .models import Entry
from main_app.models import Specialty


class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['specialty', 'type', 'hours', 'priority', 'description']
        widgets = {
            'type': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EntryCreateForm, self).__init__(*args, **kwargs)
        user_entries_specialties = Entry.objects.filter(owner=user).only('specialty')
        self.fields['specialty'].queryset = Specialty.objects.all().exclude(
            pk__in=[e.specialty.pk for e in user_entries_specialties])


class EntryUpdateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['type', 'hours', 'priority', 'description']
        widgets = {
            'type': forms.RadioSelect,
        }

from django import forms
from .models import Entry
from main_app.models import Specialty


class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['specialty', 'type', 'variant', 'hours', 'priority', 'description']
        widgets = {
            'type': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EntryCreateForm, self).__init__(*args, **kwargs)

    # def full_clean(self):
    #     super().full_clean()
    #     try:
    #         self.instance.validate_unique()
    #     except forms.ValidationError as e:
    #         self._update_errors(e)

class EntryUpdateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['type', 'variant', 'hours', 'priority', 'description']
        widgets = {
            'type': forms.RadioSelect,
        }

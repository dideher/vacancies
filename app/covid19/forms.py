from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Covid19Entry
from main_app.models import Specialty
from vacancies.utils.form import SpecialtyModelChoiceField
from vacancies.utils import  is_empty

class Covid19EntryCreateForm(forms.ModelForm):
    # check https://stackoverflow.com/questions/52920107/how-to-populate-fill-choicefield-with-custom-values-in-django-forms

    specialty = SpecialtyModelChoiceField(
        label=_('Ειδικότητα'),
        queryset=Specialty.objects.filter(active=True).order_by('ordering')
    )

    class Meta:
        model = Covid19Entry
        fields = ['teacher_registry', 'teacher_surname', 'teacher_name', 'specialty', 'hours', 'illness_started',
                  'illness_end_estimation', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(Covid19EntryCreateForm, self).__init__(*args, **kwargs)

        # populate the variant field based on the "current user"
        #self.fields['variant'].choices = get_variant_choices(current_user=user)

    def clean(self):
        """
        Validates the leave's date_from and date_until
        """

        cleaned_data = super().clean()

        teacher_registry = cleaned_data.get("teacher_registry")
        teacher_name = cleaned_data.get("teacher_name")
        teacher_surname = cleaned_data.get("teacher_surname")
        illness_started = cleaned_data.get("illness_started")
        illness_end_estimation = cleaned_data.get("illness_end_estimation")

        if not is_empty(teacher_registry):
            print(type(teacher_registry))
            try:
                teacher_registry = int(teacher_registry)
            except ValueError:
                self.add_error('teacher_registry', _('Ο αριθμός μητρώου που δηλώσατε δεν είναι αποδεκτός'))

            if teacher_registry <= 0 or teacher_registry > 999999:
                self.add_error('teacher_registry', _('Ο αριθμός μητρώου που δηλώσατε δεν είναι αποδεκτός'))

        if is_empty(teacher_name) and is_empty(teacher_surname) and teacher_registry is None:
            self.add_error(None, _('Πρέπει να δηλώσετε ΑΜ ή το πλήρες ονοματεπώνυμο του εκπαιδευτικού'))

        if not is_empty(teacher_name) and is_empty(teacher_surname):
            self.add_error('teacher_surname', _('Αφού δηλώσατε όνομα, τότε πρέπει να δηλώσετε ΚΑΙ το επώνυμο του εκπαιδευτικού' ))

        if is_empty(teacher_name) and not is_empty(teacher_surname):
            self.add_error('teacher_name', _('Αφού δηλώσατε επώνυμο, τότε πρέπει να δηλώσετε ΚΑΙ το όνομα του εκπαιδευτικού'))

        if illness_started and illness_end_estimation and illness_started >= illness_end_estimation:
            self.add_error('illness_end_estimation', _('Η ημ/νία πιθανής επιστροφής είναι προγενέστερη ή ίση της ημ/νιας νόσησης'))

        return cleaned_data


class Covid19EntryUpdateForm(forms.ModelForm):

    # variant = forms.ChoiceField(
    #     label=_('Τύπος Κενού / Πλεονάσματος'),
    #     help_text=_('Επιλέξετε το είδος του κενού'),
    # )

    class Meta:
        model = Covid19Entry
        fields = ['hours' ]
        # widgets = {
        #     'type': forms.RadioSelect,
        #     'description': forms.Textarea(attrs={'rows': 3}),
        # }


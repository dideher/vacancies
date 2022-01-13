from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Covid19Entry


class Covid19EntryCreateForm(forms.ModelForm):
    # check https://stackoverflow.com/questions/52920107/how-to-populate-fill-choicefield-with-custom-values-in-django-forms
    # variant = forms.ChoiceField(
    #     label=_('Τύπος Κενού / Πλεονάσματος'),
    #     help_text=_('Επιλέξετε το είδος του κενού'),
    # )

    # specialty = SpecialtyModelChoiceField(
    #     label=_('Ειδικότητα'),
    #     queryset=Specialty.objects.filter(active=True).order_by('ordering')
    # )

    class Meta:
        model = Covid19Entry
        fields = ['hours']
        # widgets = {
        #     'type': forms.RadioSelect,
        #     'description': forms.Textarea(attrs={'rows': 3}),
        # }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(Covid19EntryCreateForm, self).__init__(*args, **kwargs)

        # populate the variant field based on the "current user"
        #self.fields['variant'].choices = get_variant_choices(current_user=user)

    # def full_clean(self):
    #     super().full_clean()
    #     try:
    #         self.instance.validate_unique()
    #     except forms.ValidationError as e:
    #         self._update_errors(e)


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


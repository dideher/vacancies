from django import forms
from .models import SchoolClassesInfo

class SchoolClassesInfoUpdateForm(forms.ModelForm):

    # variant = forms.ChoiceField(
    #     label=_('Τύπος Κενού / Πλεονάσματος'),
    #     help_text=_('Επιλέξετε το είδος του κενού'),
    # )

    class Meta:
        model = SchoolClassesInfo
        fields = [
            'a_grade_classes',
            'a_grade_classes_over_21',
            'a_grade_classes_french',
            'a_grade_classes_german',
            'b_grade_classes',
            'b_grade_classes_over_21',
            'b_grade_classes_french',
            'b_grade_classes_german',
            'b_grace_classes_prosanatolismou',
            'b_grace_classes_anthropistikon',
            'c_grade_classes',
            'c_grade_classes_over_21',
            'c_grade_classes_french',
            'c_grade_classes_german',
            'c_grade_classes_prosanatolismou',
            'c_grade_classes_anthropistikon',
            'c_grade_classes_thetikon',
            'c_grade_classes_pliroforikis',
        ]
        exclude = [ 'school', ]
        # widgets = {
        #     'type': forms.RadioSelect,
        #     'description': forms.Textarea(attrs={'rows': 3}),
        # }
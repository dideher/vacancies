from django import forms

from main_app.models import Specialty


class SpecialtyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        """
        Convert objects into strings and generate the labels for the choices
        presented by this object. Subclasses can override this method to
        customize the display of the choices.
        """
        if isinstance(obj, Specialty):
            sp: Specialty = obj
            return f'{sp.code} - {sp.lectic}'
        else:
            return str(obj)
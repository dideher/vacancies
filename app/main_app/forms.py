from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Entry, EntryVariantType, Specialty


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



VALID_ENTRY_VARIANTS_DEFAULT = (
    EntryVariantType.GENERAL_EDUCATION ,
    EntryVariantType.GENERAL_EDUCATION_WITH_EXAMS ,
    EntryVariantType.SPECIFIC_NEEDS_SMEAE,
    EntryVariantType.SPECIFIC_NEEDS_INTEGRATION_CLASS,
    EntryVariantType.SPECIFIC_NEEDS_INTEGRATION_CLASS_DEAF,
    EntryVariantType.SPECIFIC_NEEDS_INTEGRATION_CLASS_BLIND,
    EntryVariantType.SPECIFIC_NEEDS_PARALLEL_SUPPORT,
    EntryVariantType.SPECIFIC_NEEDS_PARALLEL_SUPPORT_DEAF,
    EntryVariantType.SPECIFIC_NEEDS_PARALLEL_SUPPORT_BLIND,
    EntryVariantType.VULNERABLE_GROUP,
    EntryVariantType.BY_RESIGNATION,
    EntryVariantType.RECEPTION_CLASSES,
    EntryVariantType.A_NEW_START,
)

VALID_ENTRY_VARIANTS_MUSIC_SCHOOL = (
    EntryVariantType.MUSICAL_AKORTEON,
    EntryVariantType.MUSICAL_BIOLA,
    EntryVariantType.MUSICAL_BIOLI,
    EntryVariantType.MUSICAL_BIOLI_TRADITIONAL,
    EntryVariantType.MUSICAL_BIOLOTSELO,
    EntryVariantType.MUSICAL_GAINDA,
    EntryVariantType.MUSICAL_DIEYTH_ORXISTRAS,
    EntryVariantType.MUSICAL_DIEYTH_XORODIAS,
    EntryVariantType.MUSICAL_ZOURNAS,
    EntryVariantType.MUSICAL_THEORHTIKA_BYZ_MOUSIKHS,
    EntryVariantType.MUSICAL_THEORHTIKA_EYR_MOUSIKHS,
    EntryVariantType.MUSICAL_KANONAKI,
    EntryVariantType.MUSICAL_KITHARA_HLEKTRIKI,
    EntryVariantType.MUSICAL_KITHARA_KLASIKI,
    EntryVariantType.MUSICAL_KLARINETO,
    EntryVariantType.MUSICAL_KLARINO_PARADOSIAKO,
    EntryVariantType.MUSICAL_KONTRAMPASO,
    EntryVariantType.MUSICAL_KORNO,
    EntryVariantType.MUSICAL_KROUSTA_EYR,
    EntryVariantType.MUSICAL_KROUSTA_PARADOSIAKA,
    EntryVariantType.MUSICAL_LAOUTO,
    EntryVariantType.MUSICAL_LYRA_DODEKANHSOU,
    EntryVariantType.MUSICAL_LYRA_KRHTIKH,
    EntryVariantType.MUSICAL_LYRA_MAKEDONIAS,
    EntryVariantType.MUSICAL_LYRA_POLITIKH,
    EntryVariantType.MUSICAL_LYRA_PONTIAKH,
    EntryVariantType.MUSICAL_MANTOLINO,
    EntryVariantType.MUSICAL_MOUSIKHS_TEXNLOGIAS,
    EntryVariantType.MUSICAL_MPASO_HLEKTRIKO,
    EntryVariantType.MUSICAL_MPOUZOUKI_TRIXORDO,
    EntryVariantType.MUSICAL_NEI_KABALI_PAR_AYLOI,
    EntryVariantType.MUSICAL_OMPOE,
    EntryVariantType.MUSICAL_OUTI,
    EntryVariantType.MUSICAL_PIANO,
    EntryVariantType.MUSICAL_SANTOURI,
    EntryVariantType.MUSICAL_SAXOFONO,
    EntryVariantType.MUSICAL_TAMPOURA,
    EntryVariantType.MUSICAL_TOUMPA,
    EntryVariantType.MUSICAL_TROMPETA,
    EntryVariantType.MUSICAL_TROMPONI,
    EntryVariantType.MUSICAL_FAGOTO,
    EntryVariantType.MUSICAL_FLAOUTO,
)


def get_variant_choices(**kwargs):
    """
    Returns valid EntryVariantType choices based on the current user
    or other criteria
    """
    valid_choices = list()
    current_user = kwargs.get('current_user')
    if current_user is None:
        # current user is None, so return all variants
        return EntryVariantType.choices
    
    # until user is properly connected with the school entity,
    # match against the user last name
    if current_user.last_name == 'ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ - ΓΥΜΝΑΣΙΟ':
        valid_entry_variants = VALID_ENTRY_VARIANTS_MUSIC_SCHOOL
    else:
        # go with the default list
        valid_entry_variants = VALID_ENTRY_VARIANTS_DEFAULT
    
    for k, v in EntryVariantType.choices:
        if k in valid_entry_variants:
            valid_choices.append((k, v))
        
    return valid_choices


class EntryCreateForm(forms.ModelForm):
    # check https://stackoverflow.com/questions/52920107/how-to-populate-fill-choicefield-with-custom-values-in-django-forms
    variant = forms.ChoiceField(
        label=_('Τύπος Κενού / Πλεονάσματος'), 
        help_text=_('Επιλέξετε το είδος του κενού'), 
    )

    specialty = SpecialtyModelChoiceField(
        label=_('Ειδικότητα'),
        queryset=Specialty.objects.all()
    )

    class Meta:
        model = Entry
        fields = ['specialty', 'type', 'variant', 'hours', 'description']
        widgets = {
            'type': forms.RadioSelect,
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EntryCreateForm, self).__init__(*args, **kwargs)

        # populate the variant field based on the "current user"
        self.fields['variant'].choices = get_variant_choices(current_user=user)

    # def full_clean(self):
    #     super().full_clean()
    #     try:
    #         self.instance.validate_unique()
    #     except forms.ValidationError as e:
    #         self._update_errors(e)


class EntryUpdateForm(forms.ModelForm):

    # variant = forms.ChoiceField(
    #     label=_('Τύπος Κενού / Πλεονάσματος'),
    #     help_text=_('Επιλέξετε το είδος του κενού'),
    # )

    class Meta:
        model = Entry
        fields = ['type', 'variant', 'hours', 'description']
        widgets = {
            'type': forms.RadioSelect,
            'description': forms.Textarea(attrs={'rows': 3}),
        }


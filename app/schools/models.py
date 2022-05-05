from django.db import models
from django.utils.translation import gettext_lazy as _


class SchoolType(models.TextChoices):
    GYMNASIO = 'GYMNASIO', _('Γυμνάσια')
    GYMNASIO_LYKEIO = 'GYMNASIO_LYKEIO', _('Γυμνάσιο Με Λυκειακές Τάξεις')
    LYKEIO = 'LYKEIO', _('Λύκεια')
    EPAL = 'EPAL', _('Επαγγελματικά Λύκεια'),
    EEEEK = 'EEEEK', _('Ειδικής Επαγγελματικής Εκπαίδευσης και Κατάρτισης')


class SchoolVariant(models.TextChoices):
    HMERISIO_GYM = 'HMERISIO_GYM', _('Ημερήσιο Γυμνάσιο')
    HMERISIO_LYK = 'HMERISIO_LYK', _('Ημερήσιο Γενικό Λύκειο')
    EIDIKIS_AGOGIS_GYM = 'EIDIKIS_AGOGIS_GYM', _('Γυμνάσιο Ειδικής Αγωγής')
    ΕΕΕΕΚ = 'ΕΕΕΕΚ', _('ΕΕΕΕΚ')
    ENIAIO_EIDIKO_GYM_LYK = 'ENIAIO_EIDIKO_GYM_LYK', _('Ενιαίο Ειδικό Επαγγελματικό Γυμνάσιο - Λύκειο')
    ESPERINO_LYK = 'ESPERINO_LYK', _('Εσπερινό Γενικό Λύκειο')
    ESPERINO_GYM = 'ESPERINO_GYM', _('Εσπερινό Γυμνάσιο')
    ESPERINO_GYM_LYK_TAKSEIS = 'ESPERINO_GYM_LYK_TAKSEIS', _('Εσπερινό Γυμνάσιο με Λυκειακές Τάξεις')
    ESPERINO_EPAL = 'ESPERINO_EPAL', _('Εσπερινό ΕΠΑΛ')
    HMERISIO_EPAL = 'HMERISIO_EPAL', _('Ημερήσιο ΕΠΑΛ')
    KALITEXNIKO_GYM_LYK_TAKSEIS = 'KALITEXNIKO_GYM_LYK_TAKSEIS', _('Καλλιτεχνικό Γυμνάσιο με Λυκειακές Τάξεις')
    MOYSIKO_GYM_LYK_TAKSEIS = 'MOYSIKO_GYM_LYK_TAKSEIS', _('Μουσικό Γυμνάσιο με Μουσικές Λυκειακές Τάξεις')
    PROTYPO_GYM = 'PROTYPO_GYM', _('Πρότυπο Γυμνάσιο')
    PROTYPO_LYK = 'PROTYPO_LYK', _('Πρότυπο Λύκειο')


class School(models.Model):
    email = models.EmailField(unique=True, null=False, verbose_name='Email Σχολείου')
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Όνομα Σχολείου')
    myschool_name = models.CharField(max_length=100, null=True, verbose_name='Όνομα Σχολείου MySchool')
    ministry_code = models.CharField(max_length=18, null=True, verbose_name='Κωδικός Υπουργείου')
    principal = models.CharField(max_length=100, null=True, verbose_name='Διευθυντής Σχολείου')
    phone = models.CharField(max_length=15, null=True, verbose_name='Τηλέφωνο Σχολείου')
    address = models.CharField(max_length=100, null=True, verbose_name='Διεύθυνση Σχολείου')
    sibling_school = models.ForeignKey('self', null=True, on_delete=models.SET_NULL,
                                       verbose_name='Συστεγαζόμενο Σχολείο')
    school_type = models.CharField(
        max_length=64,
        verbose_name=_('Έιδος Σχολείου'),
        help_text=_('Επιλέξετε τον τύπο της σχολική μονάδας (Γυμνάσιο/Λύκειο/...)'),
        choices=SchoolType.choices,
        default=SchoolType.LYKEIO,
        null=False
    )
    school_variant = models.CharField(
        max_length=58,
        verbose_name=_('Κατηγορία'),
        help_text=_('Επιλέξετε την κατηγορία της σχολικής μονάδας'),
        choices=SchoolVariant.choices,
        default=SchoolVariant.HMERISIO_LYK,
        null=False
    )
    school_group = models.ForeignKey('SchoolGroup',
                                     verbose_name=_('Σχολική Ομάδα'),
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='schools')

    def __str__(self):
        return f'{self.name}'


class SchoolGroup(models.Model):
    """
    Models a school group
    """
    name = models.CharField(max_length=100, null=False, verbose_name='Ομάδα', unique=True)
    ordering = models.PositiveSmallIntegerField(null=True, verbose_name='Σειρά')
    neighboring_tag = models.CharField(max_length=5, null=True, verbose_name='Όμορη Όμαδα', db_index=True)

    def __str__(self):
        return str(self.name)



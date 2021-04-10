from django.db import models
from django.utils.translation import gettext_lazy as _


class SchoolType(models.TextChoices):
    GYMNASIO = 'GYMNASIO', _('Γυμνάσιο')
    GYMNASIO_LYKEIO = 'GYMNASIO_LYKEIO', _('Γυμνάσιο Με Λυκειακές Τάξεις')
    LYKEIO = 'LYKEIO', _('Λύκειο')
    EPAL = 'EPAL', _('ΕΠΑΛ'),


class SchoolTimetable(models.TextChoices):
    ESPERINO = 'ESPERINO', _('Εσπερινό')
    HMERISIO = 'HMERISIO', _('Ημερήσιο')


class SchoolVariant(models.TextChoices):
    GENERAL = 'GENERAL', _('Γενικής Παιδείας')
    MUSIC = 'MUSIC', _('Μουσικό')
    ART = 'ART', _('Καλλιτεχνικό')
    PEIRAMATIKO = 'PEIRAMATIKO', _('Πειραματικό')
    EIDIKO = 'EIDIKO', _('Ειδικό')


class School(models.Model):
    email = models.EmailField(unique=True, null=True, verbose_name='Email Σχολείου')
    name = models.CharField(max_length=100, null=True, verbose_name='Όνομα Σχολείου')
    principal = models.CharField(max_length=100, null=True, verbose_name='Διευθυντής Σχολείου')
    phone = models.CharField(max_length=15, null=True, verbose_name='Τηλέφωνο Σχολείου')
    address = models.CharField(max_length=100, null=True, verbose_name='Διεύθυνση Σχολείου')
    school_type = models.CharField(
        max_length=16,
        verbose_name=_('Έιδος Σχολείου'),
        help_text=_('Επιλέξετε τον τύπο της σχολική μονάδας (Γυμνάσιο/Λύκειο/...)'),
        choices=SchoolType.choices,
        default=SchoolType.LYKEIO,
        null=False
    )
    school_timetable = models.CharField(
        max_length=16,
        verbose_name=_('Ωράριο Λειτουργίας'),
        help_text=_('Επιλέξετε τον το ωράριο λειτουργίας της σχολικής μονάδας'),
        choices=SchoolTimetable.choices,
        default=SchoolTimetable.HMERISIO,
        null=False
    )
    school_variant = models.CharField(
        max_length=16,
        verbose_name=_('Κατηγορία'),
        help_text=_('Επιλέξετε την κατηγορία της σχολικής μονάδας'),
        choices=SchoolVariant.choices,
        default=SchoolVariant.GENERAL,
        null=False
    )

    def __str__(self):
        return f'{self.name}'

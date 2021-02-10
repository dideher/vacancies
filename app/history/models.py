from django.db import models
from django.contrib.auth.models import User
from main_app.models import Specialty
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from main_app.models import EntryVariantType

class HistoryEntry(models.Model):
    ENTRY_CHOICES = (
        ('Κενό', 'Κενό'),
        ('Πλεόνασμα', 'Πλεόνασμα')
    )

    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='Ειδικότητα', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.IntegerField(default=0)
    date_time = models.DateTimeField(default=now, verbose_name='Χρονική σήμανση')
    type = models.CharField(default='Κενό', choices=ENTRY_CHOICES, max_length=9, verbose_name='Κενό / Πλεόνασμα')
    description = models.TextField(verbose_name='Παρατηρήσεις', blank=True)
    variant = models.CharField(
        max_length=64, 
        verbose_name=_('Τύπος Κενού / Πλεονάσματος'), 
        help_text=_('Επιλέξετε το είδος του κενού'), 
        choices=EntryVariantType.choices,
        default=EntryVariantType.GENERAL_EDUCATION,
        null=False
    )

    def __str__(self):
        return f'{self.specialty} | {self.owner} | {self.hours} | {self.type} | {self.description}'
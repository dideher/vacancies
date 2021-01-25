from django.db import models
from django.contrib.auth.models import User
from main_app.models import Specialty
from django.utils.timezone import now


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
    priority = models.BooleanField(default=False, verbose_name='Προτεραιότητα')
    description = models.CharField(max_length=128, verbose_name='Παρατηρήσεις', null=True, blank=True)

    def __str__(self):
        return f'{self.specialty} | {self.owner} | {self.hours} | {self.type} | {self.priority} | {self.description}'
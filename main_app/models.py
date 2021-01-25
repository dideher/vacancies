from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator


class Specialty(models.Model):
    code = models.CharField(unique=True, max_length=10, verbose_name='Ειδικότητα')
    lectic = models.CharField(max_length=100, verbose_name='Λεκτικό')

    def __str__(self):
        return self.code


class Entry(models.Model):
    ENTRY_CHOICES = (
        ('Κενό', 'Κενό'),
        ('Πλεόνασμα', 'Πλεόνασμα')
    )

    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='Ειδικότητα', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.IntegerField(default=0, validators=[MinValueValidator(1)],
                                error_messages={'min_value': "Η τιμή πρέπει να είναι μεγαλύτερη του 0."},
                                help_text="Η τιμή πρέπει να είναι μεγαλύτερη του 0.",
                                verbose_name='Ώρες')
    date_time = models.DateTimeField(auto_now=True, verbose_name='Χρονική σήμανση')
    type = models.CharField(default='Κενό', choices=ENTRY_CHOICES, max_length=9, verbose_name='Κενό / Πλεόνασμα')
    priority = models.BooleanField(default=False, verbose_name='Προτεραιότητα')
    description = models.CharField(max_length=128, verbose_name='Παρατηρήσεις', null=True, blank=True)

    class Meta:
        unique_together = (('specialty', 'owner'),)

    def __str__(self):
        return f'{self.specialty} | {self.owner} | {self.hours} | {self.type} | {self.priority} | {self.description}'

    def get_absolute_url(self):
        return reverse('main_app:entry_detail', kwargs={'pk': self.pk})

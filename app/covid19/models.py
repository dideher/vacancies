from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from vacancies.commons import EntryHistoryEventType


class Covid19Entry(models.Model):
    teacher_name = models.CharField(blank=True, max_length=32, default='', verbose_name='Όνομα Εκπ/ου', help_text="")
    teacher_surname = models.CharField(blank=True, max_length=32, default='', verbose_name='Επώνυμο Εκπ/ου', help_text="")
    teacher_registry = models.IntegerField(blank=True, null=True, default=None, verbose_name='Α.Μ.')
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='covid19_entries', null=True, default=None)

    specialty = models.ForeignKey('main_app.Specialty', on_delete=models.CASCADE, verbose_name='Ειδικότητα', null=True)
    hours = models.IntegerField(default=0, validators=[MinValueValidator(1)],
                                error_messages={'min_value': "Η τιμή πρέπει να είναι μεγαλύτερη του 0."},
                                help_text="Η τιμή πρέπει να είναι μεγαλύτερη του 0.",
                                verbose_name='Ώρες')
    illness_started = models.DateField(auto_now=True, verbose_name='Ημ/νια Νόσησης', null=False)
    illness_end_estimation = models.DateField(auto_now=False, verbose_name='Ημ/νια Πιθανής Επιστροφής', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_on = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted_on = models.DateTimeField(auto_now=False, null=True, blank=True)
    comments = models.TextField(verbose_name='Παρατηρήσεις', blank=True,
                                help_text='Καταχωρίστε τυχόν παρατηρήσεις που μπορεί να έχετε για το συγεκριμένο προσωρινό COVID-19 κενό',
                                default='')

    class Meta:
        indexes = [
            models.Index(fields=['school', 'specialty']),
            models.Index(fields=['created_on']),
        ]


class Covid19EntryEventHistory(models.Model):
    covid_entry = models.ForeignKey(Covid19Entry,  on_delete=models.CASCADE, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    event_datetime = models.DateTimeField(auto_now=True, null=False, blank=False)
    event_type = models.CharField(default=EntryHistoryEventType.HISTORY_EVENT_INSERT,
                                  choices=EntryHistoryEventType.choices, max_length=15)
    event_description = models.TextField(blank=True, default='')

    class Meta:
        indexes = [
            models.Index(fields=['covid_entry']),
            models.Index(fields=['event_datetime']),
        ]

from django.db import models
from django.utils.translation import gettext_lazy as _


class EntryHistoryEventType(models.TextChoices):
    HISTORY_EVENT_INSERT = 'INSERT', _('Καταχώριση Εγγραφής')
    HISTORY_EVENT_UPDATE = 'UPDATE', _('Τροποποίηση Εγγραφής')
    HISTORY_EVENT_DELETE = 'DELETE', _('Διαγραφή Εγγραφής')
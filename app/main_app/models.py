from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Specialty(models.Model):
    code = models.CharField(unique=True, max_length=10, verbose_name='Ειδικότητα')
    lectic = models.CharField(max_length=100, verbose_name='Λεκτικό')

    def __str__(self):
        return self.code

class EntryVariantType(models.TextChoices):
    
    GENERAL_EDUCATION = 'GENERAL_EDUCATION', _('Γενικής Παιδείας για μη Πανελλαδικώς Εξεταζόμενα Μαθήματα')
    GENERAL_EDUCATION_WITH_EXAMS = 'GENERAL_EDUCATION_WITH_EXAMS', _('Γενικής Παιδείας για Πανελλαδικώς Εξεταζόμενο Μάθημα')
    SPECIFIC_NEEDS_SMEAE = 'SPECIFIC_NEEDS_SMEAE', _('Ειδικής Αγωγής - ΣΜΕΑΕ')
    SPECIFIC_NEEDS_INTEGRATION_CLASS = 'SPECIFIC_NEEDS_INTEGRATION_CLASS', _('Ειδικής Αγωγής - Τμήμα Ένταξης')
    SPECIFIC_NEEDS_INTEGRATION_CLASS_DEAF = 'SPECIFIC_NEEDS_INTEGRATION_CLASS_DEAF', _('Ειδικής Αγωγής - Τμήμα Ένταξης Κωφών')
    SPECIFIC_NEEDS_INTEGRATION_CLASS_BLIND = 'SPECIFIC_NEEDS_INTEGRATION_CLASS_BLIND', _('Ειδικής Αγωγής - Τμήμα Ένταξης Τυφλών')
    SPECIFIC_NEEDS_PARALLEL_SUPPORT = 'SPECIFIC_NEEDS_PARALLEL_SUPPORT', _('Ειδικής Αγωγής - Παράλληλης Στήριξης')
    SPECIFIC_NEEDS_PARALLEL_SUPPORT_DEAF = 'SPECIFIC_NEEDS_PARALLEL_SUPPORT_DEAF', _('Ειδικής Αγωγής - Παράλληλης Στήριξης Κωφών')
    SPECIFIC_NEEDS_PARALLEL_SUPPORT_BLIND = 'SPECIFIC_NEEDS_PARALLEL_SUPPORT_BLIND', _('Ειδικής Αγωγής - Παράλληλης Στήριξης Τυφλών')
    VULNERABLE_GROUP = 'VULNERABLE_GROUP', _('Ευπαθών Ομάδων')
    BY_RESIGNATION = 'BY_RESIGNATION', _('Από παραίτηση')


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
    description = models.TextField(verbose_name='Παρατηρήσεις', blank=True, default='')
    variant = models.CharField(
        max_length=64, 
        verbose_name=_('Τύπος Κενού / Πλεονάσματος'), 
        help_text=_('Επιλέξετε το είδος του κενού'), 
        choices=EntryVariantType.choices,
        default=EntryVariantType.GENERAL_EDUCATION,
        null=False
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'specialty', 'variant'], name='unique_variant_entry')
        ]
        
    def validate_unique(self, exclude=None):
        qs = self.__class__.objects.filter(specialty=self.specialty, variant=self.variant)
        if self.pk is None:
            # we are not updating, so go ahead
            if qs.filter(owner=self.owner).exists():
                raise ValidationError({'variant': 
                                    _(f'Υπάρχει ήδη καταχωρημένο κενό/πλεόνοσμα με αυτόν τον τύπο για την ειδικότητα {self.specialty}')})
            
        
    
    def __str__(self):
        return f'{self.specialty} ({self.variant}) | {self.owner} | {self.hours} | {self.type} | {self.description}'

    def get_absolute_url(self):
        return reverse('main_app:entry_detail', kwargs={'pk': self.pk})

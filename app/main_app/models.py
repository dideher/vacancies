from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from schools.models import School


class Specialty(models.Model):
    code = models.CharField(unique=True, max_length=10, verbose_name='Ειδικότητα')
    lectic = models.CharField(max_length=100, verbose_name='Λεκτικό')

    def __str__(self):
        return self.code


class EntryVariantType(models.TextChoices):
    
    GENERAL_EDUCATION = 'GENERAL_EDUCATION', _('Γενικής Αγωγής - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα')
    GENERAL_EDUCATION_WITH_EXAMS = 'GENERAL_EDUCATION_WITH_EXAMS', _('Γενικής Αγωγής - Πανελλαδικώς '
                                                                     'Εξεταζόμενα Μαθήματα')
    SPECIFIC_NEEDS_SMEAE = 'SPECIFIC_NEEDS_SMEAE', _('Ειδικής Αγωγής - ΣΜΕΑΕ')
    SPECIFIC_NEEDS_INTEGRATION_CLASS = 'SPECIFIC_NEEDS_INTEGRATION_CLASS', _('Ειδικής Αγωγής - Τμήμα Ένταξης')
    SPECIFIC_NEEDS_INTEGRATION_CLASS_DEAF = 'SPECIFIC_NEEDS_INTEGRATION_CLASS_DEAF', _('Ειδικής Αγωγής - '
                                                                                       'Τμήμα Ένταξης Κωφών')
    SPECIFIC_NEEDS_INTEGRATION_CLASS_BLIND = 'SPECIFIC_NEEDS_INTEGRATION_CLASS_BLIND', _('Ειδικής Αγωγής - Τμήμα '
                                                                                         'Ένταξης Τυφλών')
    SPECIFIC_NEEDS_PARALLEL_SUPPORT = 'SPECIFIC_NEEDS_PARALLEL_SUPPORT', _('Ειδικής Αγωγής - Παράλληλης Στήριξης')
    SPECIFIC_NEEDS_PARALLEL_SUPPORT_DEAF = 'SPECIFIC_NEEDS_PARALLEL_SUPPORT_DEAF', _('Ειδικής Αγωγής - Παράλληλης '
                                                                                     'Στήριξης Κωφών')
    SPECIFIC_NEEDS_PARALLEL_SUPPORT_BLIND = 'SPECIFIC_NEEDS_PARALLEL_SUPPORT_BLIND', _('Ειδικής Αγωγής - Παράλληλης '
                                                                                       'Στήριξης Τυφλών')
    VULNERABLE_GROUP = 'VULNERABLE_GROUP', _('Ευπαθών Ομάδων')
    BY_RESIGNATION = 'BY_RESIGNATION', _('Από παραίτηση')
    RECEPTION_CLASSES = 'RECEPTION_CLASSES', _('Τάξεις Υποδοχής')
    A_NEW_START = 'A_NEW_START', _('Μ.Ν.Α.Ε.'),
    MUSICAL_AKORTEON = 'MUSICAL_AKORTEON', _('Ακορντεόν')
    MUSICAL_BIOLA = 'MUSICAL_BIOLA', _('Βιόλα')
    MUSICAL_BIOLI = 'MUSICAL_BIOLI', _('Βιολί')
    MUSICAL_BIOLI_TRADITIONAL = 'MUSICAL_BIOLI_TRADITIONAL', _('Βιολί (Παραδοσιακό)')
    MUSICAL_BIOLOTSELO = 'MUSICAL_BIOLOTSELO', _('Βιολοντσέλο')
    MUSICAL_GAINDA = 'MUSICAL_GAINDA', _('Γκάιντα')
    MUSICAL_DIEYTH_ORXISTRAS = 'MUSICAL_DIEYTH_ORXISTRAS', _('Διεύθυνση Ορχήστρας')
    MUSICAL_DIEYTH_XORODIAS = 'MUSICAL_DIEYTH_XORODIAS', _('Διεύθυνση Χορωδίας')
    MUSICAL_ZOURNAS = 'MUSICAL_ZOURNAS',  _('Ζουρνάς')
    MUSICAL_THEORHTIKA_BYZ_MOUSIKHS = 'MUSICAL_THEORHTIKA_BYZ_MOUSIKHS', _('Θεωρητικά Βυζαντινής Μουσικής')
    MUSICAL_THEORHTIKA_EYR_MOUSIKHS = 'MUSICAL_THEORHTIKA_EYR_MOUSIKHS', _('Θεωρητικά Ευρωπαϊκής Μουσικής')
    MUSICAL_KANONAKI = 'MUSICAL_KANONAKI', _('Κανονάκι')
    MUSICAL_KITHARA_HLEKTRIKI = 'MUSICAL_KITHARA_HLEKTRIKI', _('Κιθάρα ηλεκτρική')
    MUSICAL_KITHARA_KLASIKI = 'MUSICAL_KITHARA_KLASIKI', _('Κιθάρα κλασική')
    MUSICAL_KLARINETO = 'MUSICAL_KLARINETO',  _('Κλαρινέτο')
    MUSICAL_KLARINO_PARADOSIAKO = 'MUSICAL_KLARINO_PARADOSIAKO', _('Κλαρίνο (Παραδοσιακό)')
    MUSICAL_KONTRAMPASO = 'MUSICAL_KONTRAMPASO', _('Κοντραμπάσο')
    MUSICAL_KORNO = 'MUSICAL_KORNO', _('Κόρνο')
    MUSICAL_KROUSTA_EYR = 'MUSICAL_KROUSTA_EYR', _('Κρουστά Ευρωπαϊκά (Κλασικά - Σύγχρονα)')
    MUSICAL_KROUSTA_PARADOSIAKA = 'MUSICAL_KROUSTA_PARADOSIAKA', _('Κρουστά παραδοσιακά')
    MUSICAL_LAOUTO = 'MUSICAL_LAOUTO', _('Λαούτο')
    MUSICAL_LYRA_DODEKANHSOU = 'MUSICAL_LYRA_DODEKANHSOU', _('Λύρα Δωδεκανήσου')
    MUSICAL_LYRA_KRHTIKH = 'MUSICAL_LYRA_KRHTIKH', _('Λύρα Κρητική')
    MUSICAL_LYRA_MAKEDONIAS = 'MUSICAL_LYRA_MAKEDONIAS', _('Λύρα Μακεδονίας')
    MUSICAL_LYRA_POLITIKH = 'MUSICAL_LYRA_POLITIKH', _('Λύρα Πολίτικη')
    MUSICAL_LYRA_PONTIAKH = 'MUSICAL_LYRA_PONTIAKH', _('Λύρα Ποντιακή')
    MUSICAL_MANTOLINO = 'MUSICAL_MANTOLINO', _('Μαντολίνο')
    MUSICAL_MOUSIKHS_TEXNLOGIAS = 'MUSICAL_MOUSIKHS_TEXNLOGIAS', _('Μουσικής Τεχνολογίας (Εφαρμογές Η/Υ)')
    MUSICAL_MPASO_HLEKTRIKO = 'MUSICAL_MPASO_HLEKTRIKO', _('Μπάσο ηλεκτρικό')
    MUSICAL_MPOUZOUKI_TRIXORDO = 'MUSICAL_MPOUZOUKI_TRIXORDO', _('Μπουζούκι (Τρίχορδο)')
    MUSICAL_NEI_KABALI_PAR_AYLOI = 'MUSICAL_NEI_KABALI_PAR_AYLOI', _('Νέι-Καβάλι-Παραδοσιακοί Αυλοί')
    MUSICAL_OMPOE = 'MUSICAL_OMPOE', _('Όμποε')
    MUSICAL_OUTI = 'MUSICAL_OUTI', _('Ούτι')
    MUSICAL_PIANO = 'MUSICAL_PIANO',  _('Πιάνο')
    MUSICAL_SANTOURI = 'MUSICAL_SANTOURI', _('Σαντούρι')
    MUSICAL_SAXOFONO = 'MUSICAL_SAXOFONO', _('Σαξόφωνο (Άλτο - Βαρύτονο - Τενόρο)')
    MUSICAL_TAMPOURA = 'MUSICAL_TAMPOURA', _('Ταμπουράς')
    MUSICAL_TOUMPA = 'MUSICAL_TOUMPA', _('Τούμπα')
    MUSICAL_TROMPETA = 'MUSICAL_TROMPETA', _('Τρομπέτα')
    MUSICAL_TROMPONI = 'MUSICAL_TROMPONI', _('Τρομπόνι')
    MUSICAL_FAGOTO = 'MUSICAL_FAGOTO', _('Φαγκότο')
    MUSICAL_FLAOUTO = 'MUSICAL_FLAOUTO', _('Φλάουτο')


class Entry(models.Model):
    ENTRY_CHOICES = (
        ('Κενό', 'Κενό'),
        ('Πλεόνασμα', 'Πλεόνασμα')
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='entries', null=True, default=None)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='Ειδικότητα', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hours = models.IntegerField(default=0, validators=[MinValueValidator(1)],
                                error_messages={'min_value': "Η τιμή πρέπει να είναι μεγαλύτερη του 0."},
                                help_text="Η τιμή πρέπει να είναι μεγαλύτερη του 0.",
                                verbose_name='Ώρες')
    date_time = models.DateTimeField(auto_now=True, verbose_name='Χρονική σήμανση')
    type = models.CharField(default='Κενό', choices=ENTRY_CHOICES, 
                            max_length=9, verbose_name='Κενό / Πλεόνασμα')
    description = models.TextField(verbose_name='Παρατηρήσεις', blank=True,
                                   help_text='Καταχωρίστε τυχόν παρατηρήσεις που μπορεί να έχετε για το '
                                             'συγεκριμένο κενό/πλεόνασμα',
                                   default='')
    variant = models.CharField(
        max_length=64, 
        verbose_name=_('Τύπος Κενού / Πλεονάσματος'), 
        help_text=_('Επιλέξετε το είδος του κενού'), 
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
                                    _(f'Υπάρχει ήδη καταχωρισμένο κενό/πλεόνοσμα με αυτόν τον τύπο για '
                                      f'την ειδικότητα {self.specialty}')})
    
    def __str__(self):
        return f'{self.specialty} ({self.variant}) | {self.owner} | {self.hours} | {self.type} | {self.description}'

    def get_absolute_url(self):
        return reverse('main_app:entry_detail', kwargs={'pk': self.pk})

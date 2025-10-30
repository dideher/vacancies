from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

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
    myschool_name = models.CharField(max_length=100, null=True, verbose_name='Όνομα Σχολείου MySchool',
                                     blank=True)
    ministry_code = models.CharField(max_length=18, null=True, verbose_name='Κωδικός Υπουργείου', blank=True)
    principal = models.CharField(max_length=100, null=True, verbose_name='Διευθυντής Σχολείου', blank=True)
    phone = models.CharField(max_length=15, null=True, verbose_name='Τηλέφωνο Σχολείου', blank=True)
    address = models.CharField(max_length=100, null=True, verbose_name='Διεύθυνση Σχολείου', blank=True)
    sibling_school = models.ForeignKey('self', null=True, on_delete=models.SET_NULL,
                                       verbose_name='Συστεγαζόμενο Σχολείο', blank=True)
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

    def get_school_variant_label(self):
        try:
            return SchoolVariant(self.school_variant).label if self.school_variant else None
        except Exception:
            return None

    def get_school_type_label(self):
        try:
            return SchoolType(self.school_type).label if self.school_type else None
        except Exception:
            return None


    def requires_class_info(self):
        """
        Returns True if the school requires class info
        :return:
        """
        return True if self.school_type in [SchoolType.LYKEIO, SchoolType.GYMNASIO] else False

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


# GYMNASIO
# A" GENIKIS -> ek twn opoion posa einai gallika, germanika, (to idio gia b kai g) (n+1)

# LYKEIO :
# A: posa ek twn genikis paidiais, posa einai galika kai posa germanika (n+1)
# B: posa einai galika kai germanika kai prosanatolismou thetikwn kai an8rwpistikwn (auta ta dyo xwris elenxo sum)
# G: posa apo auta einai prosnataolimso anr8rwpistiwn, thetikwn, ygeias & pliforikis ((auta ta 4 xwris elenxo sum))

class SchoolClassesInfo(models.Model):

    school = models.OneToOneField(School, null=False, on_delete=models.CASCADE, verbose_name='Σχολείο', blank=False, related_name='classes_info')

    a_grade_classes = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γενικής Α' Τάξης",
        help_text="Συνολικά Τμήματα Γενικής Α' Τάξης",
        null=False,
        default=0,

    )
    a_grade_classes_over_21 = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γενικής Α' Τάξης (πάνω από 21 μαθητές)",
        null=False,
        default=0,
        help_text="Τμήματα Γενικής Α' Τάξης με πάνω απο 21 μαθητές",
    )
    a_grade_classes_french = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γαλλικών Α' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Γαλλικών Α' Τάξης",
    )
    a_grade_classes_german = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γερμανικών Α' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Γερμανικών Α' Τάξης",
    )

    b_grade_classes = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γενικής Β' Τάξης",
        null=False,
        default=0,
        help_text="Συνολικά Τμήματα Γενικής Β' Τάξης",
    )
    b_grade_classes_over_21 = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γενικής Β' Τάξης (πάνω από 21 μαθητές)",
        null=False,
        default=0,
        help_text="Τμήματα Γενικής Β' Τάξης με πάνω απο 21 μαθητές",
    )
    b_grade_classes_french = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γαλλικών Β' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Γαλλικών Β' Τάξης",
    )
    b_grade_classes_german = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γερμανικών Β' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Γερμανικών Β' Τάξης",
    )
    # only for LYKEIO
    b_grace_classes_prosanatolismou = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Προσανατολισμού Β' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Προσανατολισμού Β' Τάξης",
    )
    b_grace_classes_anthropistikon = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Ανθρωπιστικών Β' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Ανθρωπιστικών Β' Τάξης",
    )

    c_grade_classes = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γενικής Γ' Τάξης",
        null=False,
        default=0,
        help_text="Συνολικά Τμήματα Γενικής Γ' Τάξης",
    )
    c_grade_classes_over_21 = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γενικής Γ' Τάξης (πάνω από 21 μαθητές)",
        null=False,
        default=0,
        help_text="Τμήματα Γενικής Γ' Τάξης με πάνω απο 21 μαθητές",
    )
    c_grade_classes_german = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γερμανικών Γ' Τάξης",
        null=False,
        default=0,
        help_text="Συνολικά Τμήματα Γενικής Γ' Τάξης",
    )
    c_grade_classes_french = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Γαλλικών Γ' Τάξης",
        null=False,
        default=0,
        help_text="Συνολικά Τμήματα Γενικής Γ' Τάξης",
    )

    # only for LYKEIO

    c_grade_classes_prosanatolismou = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Προσανατολισμού Γ' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Προσανατολισμού Γ' Τάξης",
    )

    c_grade_classes_anthropistikon = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Ανθρωπιστικών Γ' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Ανθρωπιστικών Γ' Τάξης",
    )

    c_grade_classes_thetikon = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Θετικών Επιστημών Γ' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Θετικών Επιστημών Γ' Τάξης",
    )

    c_grade_classes_pliroforikis = models.PositiveSmallIntegerField(
        verbose_name="Τμήματα Πληροφορικής & Υγείας Γ' Τάξης",
        null=False,
        default=0,
        help_text="Τμήματα Πληροφορικής & Υγείας Γ' Τάξης",
    )

    # Automatically updated to the current timestamp whenever the object is saved
    last_updated = models.DateTimeField(
        verbose_name="Τελευταία ενημέρωση",
        auto_now=True,
    )


    def clean(self):
        if self.a_grade_classes_over_21 > self.a_grade_classes:
            raise ValidationError({"a_grade_classes_over_21": "Ο αριθμός των τμημάτων Α' με πάνω απο 21 μαθητές δεν "
                                                              "μπορεί να είναι μεγαλύτερος απο τον συνολικό αριθμό "
                                                              "τμημάτων της Α'"})
        if self.b_grade_classes_over_21 > self.b_grade_classes:
            raise ValidationError({"b_grade_classes_over_21": "Ο αριθμός των τμημάτων Β' με πάνω απο 21 μαθητές δεν "
                                                              "μπορεί να είναι μεγαλύτερος απο τον συνολικό αριθμό "
                                                              "τμημάτων της Β'"})
        if self.c_grade_classes_over_21 > self.c_grade_classes:
            raise ValidationError({"c_grade_classes_over_21": "Ο αριθμός των τμημάτων Γ' με πάνω απο 21 μαθητές δεν "
                                                              "μπορεί να είναι μεγαλύτερος απο τον συνολικό αριθμό "
                                                              "τμημάτων της Γ'"})
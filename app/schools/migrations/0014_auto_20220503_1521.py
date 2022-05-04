# Generated by Django 3.1.12 on 2022-05-03 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0013_school_myschool_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Σχολείου'),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Όνομα Σχολείου'),
        ),
        migrations.AlterField(
            model_name='school',
            name='school_type',
            field=models.CharField(choices=[('GYMNASIO', 'Γυμνάσια'), ('GYMNASIO_LYKEIO', 'Γυμνάσιο Με Λυκειακές Τάξεις'), ('LYKEIO', 'Λύκεια'), ('EPAL', 'Επαγγελματικά Λύκεια'), ('EEEEK', 'Ειδικής Επαγγελματικής Εκπαίδευσης και Κατάρτισης')], default='LYKEIO', help_text='Επιλέξετε τον τύπο της σχολική μονάδας (Γυμνάσιο/Λύκειο/...)', max_length=16, verbose_name='Έιδος Σχολείου'),
        ),
        migrations.AlterField(
            model_name='school',
            name='school_variant',
            field=models.CharField(choices=[('HMERISIO_GYM', 'Ημερήσιο Γυμνάσιο'), ('HMERISIO_LYK', 'Ημερήσιο Γενικό Λύκειο'), ('EIDIKIS_AGOGIS_GYM', 'Γυμνάσιο Ειδικής Αγωγής'), ('ΕΕΕΕΚ', 'ΕΕΕΕΚ'), ('ENIAIO_EIDIKO_GYM_LYK', 'Ενιαίο Ειδικό Επαγγελματικό Γυμνάσιο - Λύκειο'), ('ESPERINO_LYK', 'Εσπερινό Γενικό Λύκειο'), ('ESPERINO_GYM', 'Εσπερινό Γυμνάσιο'), ('ESPERINO_GYM_LYK_TAKSEIS', 'Εσπερινό Γυμνάσιο με Λυκειακές Τάξεις'), ('ESPERINO_EPAL', 'Εσπερινό ΕΠΑΛ'), ('HMERISIO_EPAL', 'Ημερήσιο ΕΠΑΛ'), ('KALITEXNIKO_GYM_LYK_TAKSEIS', 'Καλλιτεχνικό Γυμνάσιο με Λυκειακές Τάξεις'), ('MOYSIKO_GYM_LYK_TAKSEIS', 'Μουσικό Γυμνάσιο με Μουσικές Λυκειακές Τάξεις'), ('PROTYPO_GYM', 'Πρότυπο Γυμνάσιο'), ('PROTYPO_LYK', 'Πρότυπο Λύκειο')], default='HMERISIO_LYK', help_text='Επιλέξετε την κατηγορία της σχολικής μονάδας', max_length=28, verbose_name='Κατηγορία'),
        ),
        migrations.AlterField(
            model_name='school',
            name='sibling_school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='schools.school', verbose_name='Συστεγαζόμενο Σχολείο'),
        ),
    ]
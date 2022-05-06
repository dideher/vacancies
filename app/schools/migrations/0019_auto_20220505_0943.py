# Generated by Django 3.1.12 on 2022-05-05 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0018_auto_20220505_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='school_type',
            field=models.CharField(choices=[('GYMNASIO', 'Γυμνάσια'), ('GYMNASIO_LYKEIO', 'Γυμνάσιο Με Λυκειακές Τάξεις'), ('LYKEIO', 'Λύκεια'), ('EPAL', 'Επαγγελματικά Λύκεια'), ('EEEEK', 'Ειδικής Επαγγελματικής Εκπαίδευσης και Κατάρτισης')], default='LYKEIO', help_text='Επιλέξετε τον τύπο της σχολική μονάδας (Γυμνάσιο/Λύκειο/...)', max_length=32, verbose_name='Έιδος Σχολείου'),
        ),
    ]
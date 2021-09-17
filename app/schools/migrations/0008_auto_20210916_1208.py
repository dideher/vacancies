# Generated by Django 3.1.4 on 2021-09-16 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0007_auto_20210913_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='school_variant',
            field=models.CharField(choices=[('GENERAL', 'Γενικής Αγωγής'), ('MUSIC', 'Μουσικό'), ('ART', 'Καλλιτεχνικό'), ('PEIRAMATIKO', 'Πειραματικό'), ('EIDIKO', 'Ειδικό')], default='GENERAL', help_text='Επιλέξετε την κατηγορία της σχολικής μονάδας', max_length=16, verbose_name='Κατηγορία'),
        ),
    ]

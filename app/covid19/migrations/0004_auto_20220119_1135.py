# Generated by Django 3.1.12 on 2022-01-19 09:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0020_auto_20211004_1041'),
        ('covid19', '0003_auto_20220114_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='covid19entry',
            name='updated_on',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='deleted_on',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='hours',
            field=models.IntegerField(default=0, error_messages={'min_value': 'Η τιμή πρέπει να είναι μεγαλύτερη του 0.'}, help_text='Δηλώστε τις ώρες διδασκαλίας του νοσούντα στην μονάδα σας (μην δηλώσετε το υποχρεωτικό ωράριο του εκπαιδευτικού)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)], verbose_name='Ώρες Διδασκαλίας'),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='illness_end_estimation',
            field=models.DateField(blank=True, help_text='Καταχωρήστε την πιθανή (αν την γνωρίζετε) ημερομηνία επιστροφής του εκπαιδευτικού στην μονάδα', null=True, verbose_name='Ημερομηνία Πιθανής Επιστροφής'),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='illness_started',
            field=models.DateField(help_text='Καταχωρήστε την ημερομηνία νόσησης του εκπαιδευτικού', verbose_name='Ημερομηνία Νόσησης'),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='specialty',
            field=models.ForeignKey(help_text='Συμπληρώστε την ειδικότητα του νοσούντα', null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.specialty', verbose_name='Ειδικότητα'),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='teacher_name',
            field=models.CharField(blank=True, default='', help_text='Συμπληρώστε το όνομα του νοσούντα. Εναλλακτικά, μπορείτε να δηλώστε μόνο το Α.Μ.', max_length=32, verbose_name='Όνομα Εκπαιδευτικού'),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='teacher_registry',
            field=models.IntegerField(blank=True, default=None, help_text='Δηλώστε το Α.Μ. του νοσούντα εκπαιδευτικού. Αν δηλώσετε Α.Μ. τότε ΔΕΝ χρειάζεται να δηλώσετε και το πλήρες ονοματεπώνυμο του νοσούντα', null=True, verbose_name='Α.Μ.'),
        ),
        migrations.AlterField(
            model_name='covid19entry',
            name='teacher_surname',
            field=models.CharField(blank=True, default='', help_text='Συμπληρώστε το επώνυμο του νοσούντα. Εναλλακτικά, μπορείτε να δηλώστε μόνο το Α.Μ.', max_length=32, verbose_name='Επώνυμο Εκπαιδευτικού'),
        ),
        migrations.AlterField(
            model_name='covid19entryeventhistory',
            name='event_type',
            field=models.CharField(choices=[('INSERT', 'Καταχώριση Εγγραφής'), ('UPDATE', 'Τροποποίηση Εγγραφής'), ('DELETE', 'Διαγραφή Εγγραφής')], default='INSERT', max_length=15),
        ),
    ]

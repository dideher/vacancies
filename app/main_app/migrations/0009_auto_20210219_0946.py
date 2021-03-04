# Generated by Django 3.1.4 on 2021-02-19 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_auto_20210210_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Καταχωρήστε τυχόν παρατηρήσεις που μπορεί να έχετε για το συγεκριμένο κενό/πλαιόνασμα', verbose_name='Παρατηρήσεις'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='variant',
            field=models.CharField(choices=[('GENERAL_EDUCATION', 'Γενικής Παιδείας - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα'), ('GENERAL_EDUCATION_WITH_EXAMS', 'Γενικής Παιδείας - Πανελλαδικώς Εξεταζόμενα Μαθήματα'), ('SPECIFIC_NEEDS_SMEAE', 'Ειδικής Αγωγής - ΣΜΕΑΕ'), ('SPECIFIC_NEEDS_INTEGRATION_CLASS', 'Ειδικής Αγωγής - Τμήμα Ένταξης'), ('SPECIFIC_NEEDS_INTEGRATION_CLASS_DEAF', 'Ειδικής Αγωγής - Τμήμα Ένταξης Κωφών'), ('SPECIFIC_NEEDS_INTEGRATION_CLASS_BLIND', 'Ειδικής Αγωγής - Τμήμα Ένταξης Τυφλών'), ('SPECIFIC_NEEDS_PARALLEL_SUPPORT', 'Ειδικής Αγωγής - Παράλληλης Στήριξης'), ('SPECIFIC_NEEDS_PARALLEL_SUPPORT_DEAF', 'Ειδικής Αγωγής - Παράλληλης Στήριξης Κωφών'), ('SPECIFIC_NEEDS_PARALLEL_SUPPORT_BLIND', 'Ειδικής Αγωγής - Παράλληλης Στήριξης Τυφλών'), ('VULNERABLE_GROUP', 'Ευπαθών Ομάδων'), ('BY_RESIGNATION', 'Από παραίτηση'), ('RECEPTION_CLASSES', 'Τάξεις Υποδοχής'), ('A_NEW_START', 'Μ.Ν.Α.Ε.')], default='GENERAL_EDUCATION', help_text='Επιλέξετε το είδος του κενού', max_length=64, verbose_name='Τύπος Κενού / Πλεονάσματος'),
        ),
    ]
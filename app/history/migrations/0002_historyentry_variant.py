# Generated by Django 3.1.4 on 2021-02-08 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyentry',
            name='variant',
            field=models.CharField(choices=[('GENERAL_EDUCATION', 'Γενικής Παιδείας για μη Πανελλαδικώς Εξεταζόμενα Μαθήματα'), ('GENERAL_EDUCATION_WITH_EXAMS', 'Γενικής Παιδείας για Πανελλαδικώς Εξεταζόμενο Μάθημα'), ('SPECIFIC_NEEDS_SMEAE', 'Ειδικής Αγωγής - ΣΜΕΑΕ'), ('SPECIFIC_NEEDS_INTEGRATION_CLASS', 'Ειδικής Αγωγής - Τμήμα Ένταξης'), ('SPECIFIC_NEEDS_INTEGRATION_CLASS_DEAF', 'Ειδικής Αγωγής - Τμήμα Ένταξης Κωφών'), ('SPECIFIC_NEEDS_INTEGRATION_CLASS_BLIND', 'Ειδικής Αγωγής - Τμήμα Ένταξης Τυφλών'), ('SPECIFIC_NEEDS_PARALLEL_SUPPORT', 'Ειδικής Αγωγής - Παράλληλης Στήριξης'), ('SPECIFIC_NEEDS_PARALLEL_SUPPORT_DEAF', 'Ειδικής Αγωγής - Παράλληλης Στήριξης Κωφών'), ('SPECIFIC_NEEDS_PARALLEL_SUPPORT_BLIND', 'Ειδικής Αγωγής - Παράλληλης Στήριξης Τυφλών'), ('VULNERABLE_GROUP', 'Ευπαθών Ομάδων'), ('BY_RESIGNATION', 'Από παραίτηση')], default='GENERAL_EDUCATION', help_text='Επιλέξετε το είδος του κενού', max_length=64, verbose_name='Τύπος Κενού / Πλεονάσματος'),
        ),
    ]

# Generated by Django 3.1.4 on 2021-03-15 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_auto_20210228_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Καταχωρίστε τυχόν παρατηρήσεις που μπορεί να έχετε για το συγεκριμένο κενό/πλεόνασμα', verbose_name='Παρατηρήσεις'),
        ),
    ]
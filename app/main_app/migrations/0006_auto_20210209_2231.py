# Generated by Django 3.1.4 on 2021-02-09 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20210209_2222'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='entry',
            name='owner_specialty_variant',
        ),
        migrations.AddConstraint(
            model_name='entry',
            constraint=models.UniqueConstraint(fields=('owner', 'specialty', 'variant'), name='unique_entry'),
        ),
    ]

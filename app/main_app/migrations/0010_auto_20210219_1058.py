# Generated by Django 3.1.4 on 2021-02-19 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_auto_20210219_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'permissions': [('can_clear_all_entries', 'Can clear all entries')]},
        ),
    ]

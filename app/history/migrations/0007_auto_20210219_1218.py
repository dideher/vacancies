# Generated by Django 3.1.4 on 2021-02-19 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0006_auto_20210219_1057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historyentry',
            options={'permissions': [('can_clear_all_history_entries', 'Can clear all history entries'), ('can_view_all_history_entries', 'Can view all history entries')]},
        ),
    ]

# Generated by Django 3.1.4 on 2021-02-09 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_historyentry_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historyentry',
            name='priority',
        ),
    ]

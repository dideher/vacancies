# Generated by Django 3.1.4 on 2021-02-19 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': [('clear_profiles_status', 'Can clear profile statuses'), ('check_profiles_status', 'Can check profile statutes')]},
        ),
    ]

# Generated by Django 3.1.4 on 2021-02-23 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='school',
            options={'permissions': [('can_view_all_schools', 'Can view all schools')]},
        ),
    ]

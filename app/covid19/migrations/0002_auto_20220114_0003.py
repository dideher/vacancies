# Generated by Django 3.1.12 on 2022-01-13 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='covid19entry',
            name='deleted_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

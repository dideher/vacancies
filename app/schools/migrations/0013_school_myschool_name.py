# Generated by Django 3.1.12 on 2022-05-03 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0012_school_neighboring_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='myschool_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Όνομα Σχολείου MySchool'),
        ),
    ]
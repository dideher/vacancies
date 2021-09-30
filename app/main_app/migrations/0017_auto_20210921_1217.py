# Generated by Django 3.1.4 on 2021-09-21 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_auto_20210831_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialty',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Διαθέσιμο'),
        ),
        migrations.AddField(
            model_name='specialty',
            name='label',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='specialty',
            name='ordering',
            field=models.SmallIntegerField(null=True, verbose_name='Σειρά'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='lectic',
            field=models.CharField(blank=True, max_length=100, verbose_name='Λεκτικό'),
        ),
    ]

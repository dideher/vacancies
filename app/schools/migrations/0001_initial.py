# Generated by Django 3.1.4 on 2021-01-25 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='Email Σχολείου')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Σχολείο')),
                ('principal', models.CharField(max_length=100, null=True, verbose_name='Διευθυντής Σχολείου')),
                ('phone', models.CharField(max_length=15, null=True, verbose_name='Τηλέφωνο Σχολείου')),
                ('address', models.CharField(max_length=100, null=True, verbose_name='Τηλέφωνο Σχολείου')),
                ('connected_to_user', models.BooleanField(default=False, verbose_name='Σύνδεση με χρήστη')),
            ],
        ),
    ]
from django.db import models


class School(models.Model):
    email = models.EmailField(unique=True, null=True, verbose_name='Email Σχολείου')
    name = models.CharField(max_length=100, null=True, verbose_name='Σχολείο')
    principal = models.CharField(max_length=100, null=True, verbose_name='Διευθυντής Σχολείου')
    phone = models.CharField(max_length=15, null=True, verbose_name='Τηλέφωνο Σχολείου')
    address = models.CharField(max_length=100, null=True, verbose_name='Τηλέφωνο Σχολείου')
    connected_to_user = models.BooleanField(default=False, verbose_name='Σύνδεση με χρήστη')

    def __str__(self):
        return f'{self.name}'

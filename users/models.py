from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from main_app.models import Specialty
from schools.models import School


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False, verbose_name='Επαληθεύτηκε από τη ΔΔΕ')
    status = models.BooleanField(default=False, verbose_name='Έκανε επικαιροποίηση')
    status_time = models.DateTimeField(auto_now=True, verbose_name='Χρονική σήμανση επικαιροποίησης')

    def __str__(self):
        return f'{self.user.username} Profile'


def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        school = School.objects.filter(email=instance.email).first()

        if school != None:
            instance.last_name = school.name
            instance.save()
            instance.profile.verified = True
            school.connected_to_user = True
            school.save()

post_save.connect(create_profile, sender=User)

def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()

post_save.connect(save_profile, sender=User)


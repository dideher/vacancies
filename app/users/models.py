from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from schools.models import School


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.OneToOneField(
        School,
        default=None,
        related_name='managed_by',
        on_delete=models.SET_NULL,
        null=True
    )
    verified = models.BooleanField(default=False, verbose_name='Επαληθεύτηκε από τη ΔΔΕ')
    status = models.BooleanField(default=False, verbose_name='Έκανε επικαιροποίηση')
    status_time = models.DateTimeField(auto_now=True, verbose_name='Χρονική σήμανση επικαιροποίησης')

    def __str__(self):
        return f'{self.user.username} Profile'


def create_profile(sender, instance, created, *args, **kwargs):
    """
    Create a new profile and associate it with a school based on the
    name of the user
    
    :param sender:
    :param instance:
    :type instance: User
    :param created:
    :param args:
    :param kwargs:
    :return:
    """
    if created:
        new_profile = Profile.objects.create(user=instance)  # type: Profile

        school = School.objects.filter(email=instance.email).first()  # type: School

        if school is not None:
            instance.last_name = school.name
            instance.save()

            new_profile.school = school
            new_profile.verified = True
            new_profile.save()


post_save.connect(create_profile, sender=User)


def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()


post_save.connect(save_profile, sender=User)


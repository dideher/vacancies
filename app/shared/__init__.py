from django.contrib.auth.models import User
from users.models import Profile


def check_user_is_school(user: User) -> bool:
    """
    Check if user "represents" a school
    :param user:
    :return:
    """
    user_profile: Profile = user.profile
    return user_profile.school is not None


def check_user_is_superuser(user: User) -> bool:
    """
    Check if the user is a superuser
    """
    return user.is_superuser

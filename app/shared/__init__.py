from django.contrib.auth.models import User


def check_user_is_superuser(user: User) -> bool:
    """
    Check if the user is a superuser
    """
    return user.is_superuser

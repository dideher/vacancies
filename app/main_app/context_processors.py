from django.contrib.auth.models import User
from users.models import Profile
from schools.models import School, SchoolType

def school_user_global_vars(request):
    user: User = request.user

    if user.is_staff or user.is_anonymous:
        # user is staff, don't bother
        return {}

    user_profile: Profile = user.profile
    school: School = user_profile.school

    if school is None:
        # user has no school, don't bother'
        return {}

    return {
        "site_name": "My Website",
        "school": school,
        "school_requires_class_info": school.requires_class_info(),
        "school_has_class_info": True if hasattr(school, 'classes_info') else False,
        "school_class_info": getattr(school, 'classes_info') if hasattr(school, 'classes_info') else None
    }

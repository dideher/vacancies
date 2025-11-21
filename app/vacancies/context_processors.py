from constance import config
from vacancies.commons import school_updates_disallowed
def global_context(request):

    user = request.user

    return {
        "user_ip": request.META.get("REMOTE_ADDR"),
        "config": config,
        "school_updates_disallowed": school_updates_disallowed(request),
        "is_school": user.is_authenticated and not user.is_superuser,
    }
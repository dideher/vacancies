
from django.contrib.auth.mixins import UserPassesTestMixin
from vacancies.utils.permissions import check_user_is_school


class UserIsAssociatedWithASchoolTestMixin(UserPassesTestMixin):
    """
    Deny a request with a permission error if the current user is not a "school"
    False.
    """

    def test_func(self):
        return check_user_is_school(self.request.user)

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from schools.models import School
from users.models import Profile
from main_app.models import Entry, Specialty
from .serializers import SchoolSerializer, EntrySerializer, SpecialtySerializer


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retrieving specialties
    """
    queryset = Specialty.objects.all().order_by('code')
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticated]


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retrieving schools.
    """
    queryset = School.objects.all().order_by('name')
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    TODO: Add docstring
    """
    queryset = Entry.objects.all().order_by('specialty')
    serializer_class = EntrySerializer


class SchoolEntryList(viewsets.ViewSetMixin, generics.ListAPIView):

    queryset = Entry.objects.all().order_by('specialty')
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_pk = self.kwargs['pk']
        return Entry.objects.filter(school=school_pk).order_by('specialty')


def reconnect_users_to_schools(user=None):
    # type: (User) -> List[Profile]
    if user is None:
        # we are working for all users
        profiles = Profile.objects.all()  # type: list[Profile]
    else:
        profiles = [user.profile, ]  # type: list[Profile]

    # store the associated (actually processed) users/profile in a list
    associated_users = list()

    for profile in profiles:
        try:
            school = School.objects.get(email=profile.user.email)  # type: School

            profile.user.last_name = school.name
            profile.user.save()

            profile.verified = True
            profile.school = school
            profile.save()

            associated_users.append(profile)
        except School.DoesNotExist:
            pass

    return associated_users
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from schools.models import School
from users.models import Profile
from main_app.models import Entry, Specialty
from api.serializers import SchoolSerializer, EntrySerializer, SpecialtySerializer


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


class SchoolPendingList(viewsets.ViewSetMixin, generics.ListAPIView):
    """
    Returns the list of school that are still pending (not finalized their entries)
    """
    queryset = School.objects.filter(managed_by__status=False).order_by('name')
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]

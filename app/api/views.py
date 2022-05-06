from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from schools.models import School
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from main_app.models import Entry, Specialty
from api.serializers import SchoolSerializer, EntrySerializer, SpecialtySerializer, SchoolDetailSerializer


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retrieving specialties
    """
    queryset = Specialty.objects.all().order_by('code')
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticated]


class SchoolViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving schools.
    """

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = School.objects.all().order_by('name')
        serializer = SchoolSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = School.objects.all()
        user = get_object_or_404(queryset, ministry_code=pk)
        serializer = SchoolDetailSerializer(user)
        return Response(serializer.data)


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


class EntryList(viewsets.ViewSetMixin, generics.ListAPIView):
    """
    Returns a list of all entries (on schools that have finalized their data)
    """
    queryset = Entry.objects.filter(school__managed_by__status=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['variant', 'type', 'specialty']
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]


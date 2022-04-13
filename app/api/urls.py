from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import SchoolViewSet, EntryViewSet, SpecialtyViewSet, SchoolEntryList, SchoolPendingList

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'entries', EntryViewSet)
router.register(r'specialties', SpecialtyViewSet)
router.register(r'schools/(?P<pk>\d+)/entries', SchoolEntryList, basename='foooo/')
router.register(r'pending_schools', SchoolPendingList)

urlpatterns = [
    path('', include(router.urls)),
]
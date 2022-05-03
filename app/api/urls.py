from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import EntryList, SpecialtyViewSet, SchoolEntryList, SchoolPendingList, SchoolViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'entries', EntryList)
router.register(r'specialties', SpecialtyViewSet)
router.register(r'schools/(?P<pk>\d+)/entries', SchoolEntryList, basename='foooo/')
router.register(r'pending_schools', SchoolPendingList, basename='pending_schools')

urlpatterns = [
    path('', include(router.urls)),
]
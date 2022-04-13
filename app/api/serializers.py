from rest_framework import serializers
from schools.models import School
from main_app.models import Entry, Specialty


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):

    # If the profile associated with the school has "validated" all entries
    is_finalized = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = School
        fields = ['id', 'email', 'principal', 'phone', 'address', 'name', 'school_type', 'school_timetable',
                  'school_variant', 'is_finalized']

    def get_is_finalized(self, obj):
        # type: (SchoolSerializer, School) -> bool
        try:
            return obj.managed_by.status
        except School.managed_by.RelatedObjectDoesNotExist:
            return False


class EntrySerializer(serializers.ModelSerializer):

    specialty_code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Entry
        fields = ['id', 'specialty', 'hours', 'specialty_code']

    def get_specialty_code(self, obj):
        # type: (EntrySerializer, Entry) -> str
        return obj.specialty.code

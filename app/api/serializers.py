import re
from typing import Union, List
from rest_framework import serializers
from django.db.models import Q
from schools.models import School, SchoolGroup
from main_app.models import Entry, Specialty


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):

    # If the profile associated with the school has "validated" all entries
    is_finalized = serializers.SerializerMethodField(read_only=True)
    finalized_on = serializers.SerializerMethodField(read_only=True)
    sibling_school = serializers.SerializerMethodField(read_only=True)
    sibling_school_name = serializers.SerializerMethodField(read_only=True)
    school_group = serializers.SerializerMethodField(read_only=True)
    neighboring_groups = serializers.SerializerMethodField(read_only=True)
    neighboring_groups_label = serializers.SerializerMethodField(read_only=True)
    school_type_label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = School
        fields = [
            'ministry_code',
            'email',
            'name',
            'school_group',
            'neighboring_groups',
            'neighboring_groups_label',
            'sibling_school',
            'sibling_school_name',
            'principal',
            'phone',
            'address',
            'school_type',
            'school_type_label',
            'is_finalized',
            'finalized_on'
        ]

    @staticmethod
    def get_school_group_id_from_name(school_group_name: str) -> Union[int, None]:
        if school_group_name is not None:
            m = re.match(r"(\d+)", school_group_name)
            if m is not None:
                return int(m.group(1))
        return None

    def get_sibling_school(self, obj: School) -> Union[str, None]:
        try:
            sibling_school: School = obj.sibling_school
            if sibling_school is not None:
                return sibling_school.ministry_code
            return None
        except School.managed_by.RelatedObjectDoesNotExist:
            return None

    def get_sibling_school_name(self, obj: School) -> Union[str, None]:
        try:
            sibling_school: School = obj.sibling_school
            if sibling_school is not None:
                return sibling_school.name
            return None
        except School.managed_by.RelatedObjectDoesNotExist:
            return None

    def get_school_group(self, obj: School) -> Union[int, None]:

        school_group: SchoolGroup = obj.school_group
        return SchoolSerializer.get_school_group_id_from_name(school_group.name) if school_group else None

    def get_neighboring_groups(self, obj: School) -> Union[List[int], None]:
        school_group: SchoolGroup = obj.school_group

        if school_group and school_group.neighboring_tag:
            neighboring_groups = SchoolGroup.objects.filter(Q(neighboring_tag=school_group.neighboring_tag)
                                                            & ~Q(name=school_group.name)).order_by('name')
            return [SchoolSerializer.get_school_group_id_from_name(neighboring_group.name)
                    for neighboring_group in neighboring_groups]

        return None

    def get_neighboring_groups_label(self, obj: School) -> Union[str, None]:

        neighboring_groups = self.get_neighboring_groups(obj)

        if neighboring_groups:
            return ','.join(map(str, neighboring_groups))

        return None

    def get_is_finalized(self, obj: School):
        try:
            return obj.managed_by.status
        except School.managed_by.RelatedObjectDoesNotExist:
            return False

    def get_finalized_on(self, obj: School) -> str:
        try:
            return obj.managed_by.status_time
        except School.managed_by.RelatedObjectDoesNotExist:
            return None

    def get_school_type_label(self, obj: School) -> str:
        return obj.get_school_type_label()


class SchoolDetailSerializer(SchoolSerializer):

    school_variant_label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = School
        fields = [
            'ministry_code',
            'email',
            'name',
            'myschool_name',
            'school_group',
            'neighboring_groups',
            'sibling_school',
            'principal',
            'phone',
            'address',
            'school_type',
            'school_type_label',
            'school_variant',
            'school_variant_label',
            'is_finalized',
            'finalized_on'
        ]

    def get_school_variant_label(self, obj: School) -> str:
        return obj.get_school_variant_label()


class EntrySerializer(serializers.ModelSerializer):

    specialty_code = serializers.SerializerMethodField(read_only=True)
    specialty_text = serializers.SerializerMethodField(read_only=True)
    school = serializers.SerializerMethodField(read_only=True)
    school_name = serializers.SerializerMethodField(read_only=True)
    variant_label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Entry
        fields = ['id',  'school', 'school_name', 'hours', 'specialty_code', 'specialty_text', 'type', 'variant',
                  'variant_label']

    def get_school(self, obj: Entry) -> str:
        return obj.school.ministry_code

    def get_school_name(self, obj: Entry) -> str:
        return obj.school.name

    def get_specialty_code(self, obj):
        # type: (EntrySerializer, Entry) -> str
        return obj.specialty.code

    def get_specialty_text(self, obj: Entry) -> str:

        specialty_text = obj.specialty.label

        if specialty_text is None:
            specialty_text = obj.specialty.lectic

        return specialty_text

    def get_variant_label(self, obj: Entry):
        return obj.get_variant_label()


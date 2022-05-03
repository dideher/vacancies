from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction

from schools.models import School, SchoolGroup


class Command(BaseCommand):

    def handle(self, *args, **options):
        def create_school_group(name: str, ordering: int) -> SchoolGroup:
            """
            Creates a school group
            :param name:
            :param ordering:
            :return:
            """
            sg: SchoolGroup = SchoolGroup.objects.create(name=name, ordering=ordering)
            return sg

        with transaction.atomic():
            # reset all school groups

            # remove all groups
            deleted_school_groups = SchoolGroup.objects.all().delete()

            # 1η ομάδα
            create_school_group(name="1η ομάδα", ordering=1)

            # 2η ομάδα
            create_school_group(name="2η ομάδα", ordering=2)

            # 3η ομάδα
            create_school_group(name="3η ομάδα", ordering=4)

            # 4η ομάδα
            create_school_group(name="4η ομάδα", ordering=None)

            # 5η ομάδα
            create_school_group(name="5η ομάδα", ordering=6)

            # 6η ομάδα
            create_school_group(name="6η ομάδα", ordering=8)

            # 7η ομάδα
            create_school_group(name="7η ομάδα", ordering=5)

            # 8η ομάδα
            create_school_group(name="8η ομάδα", ordering=7)

            # 9η ομάδα
            create_school_group(name="9η ομάδα", ordering=3)

            # 10η ομάδα
            create_school_group(name="10η ομάδα", ordering=None)

            # 11η ομάδα
            create_school_group(name="11η ομάδα", ordering=None)

            # 12η ομάδα
            create_school_group(name="12η ομάδα", ordering=9)

            # 13η ομάδα
            create_school_group(name="13η ομάδα", ordering=10)

            # 14η ομάδα
            create_school_group(name="14η ομάδα", ordering=11)

            # 15η ομάδα
            create_school_group(name="15η ομάδα", ordering=12)

            # 16η ομάδα
            create_school_group(name="16η ομάδα", ordering=13)

            # 17η ομάδα
            create_school_group(name="17η ομάδα", ordering=14)

            # 18η ομάδα

            create_school_group(name="18η ομάδα", ordering=15)

            # 19η ομάδα
            create_school_group(name="19η ομάδα", ordering=16)

            # 20η ομάδα
            create_school_group(name="20η ομάδα", ordering=17)

            # 21η ομάδα
            create_school_group(name="21η ομάδα", ordering=18)
            # 22η ομάδα

            create_school_group(name="22η ομάδα", ordering=20)
            # 23η ομάδα

            create_school_group(name="23η ομάδα", ordering=21)
            # 24η ομάδα

            create_school_group(name="24η ομάδα", ordering=22)
            # 25η ομάδα
            create_school_group(name="25η ομάδα", ordering=23)
            create_school_group(name="26η ομάδα", ordering=24)
            create_school_group(name="27η ομάδα", ordering=25)
            create_school_group(name="28η ομάδα", ordering=26)
            create_school_group(name="29η ομάδα", ordering=27)
            create_school_group(name="30η ομάδα", ordering=29)
            create_school_group(name="31η ομάδα", ordering=30)
            create_school_group(name="32η ομάδα", ordering=31)
            create_school_group(name="33η ομάδα", ordering=32)
            create_school_group(name="34η ομάδα", ordering=33)
            create_school_group(name="35η ομάδα", ordering=34)
            create_school_group(name="36η ομάδα", ordering=28)
            create_school_group(name="37η ομάδα", ordering=19)
            create_school_group(name="38η ομάδα", ordering=None)

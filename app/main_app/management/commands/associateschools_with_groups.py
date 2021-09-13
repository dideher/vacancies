from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction

from schools.models import School, SchoolGroup


class Command(BaseCommand):

    def handle(self, *args, **options):
        def create_school_group(name: str, ordering: int, school_names: List[str]) -> SchoolGroup:
            """
            Creates a school group and associates the specified schools with the group
            :param name:
            :param ordering:
            :param school_names:
            :return:
            """
            sg: SchoolGroup = SchoolGroup.objects.create(name=name, ordering=ordering)
            for school_name in school_names:
                school: School = School.objects.get(name=school_name)
                school.school_group = sg
                school.save()
            return sg

        with transaction.atomic():
            # reset all school groups
            updated_schools = School.objects.filter(school_group__isnull=False).update(school_group=None)
            self.stdout.write(
                self.style.SUCCESS('[*] removed "%s" school(s) from their school group' % updated_schools))

            # remove all groups
            deleted_school_groups = SchoolGroup.objects.all().delete()

            # 1η ομάδα
            create_school_group(name="1η ομάδα", ordering=1, school_names=[
                '1ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '6ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                'ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '1ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                '3ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
            ])

            # 2η ομάδα
            create_school_group(name="2η ομάδα", ordering=2, school_names=[
                '3ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '5ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                '4ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ (ΕΣΠΕΡΙΝΟ)',
            ])

            # 3η ομάδα
            create_school_group(name="3η ομάδα", ordering=4, school_names=[
                '2ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '4ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '2ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                '4ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
            ])

            # 4η ομάδα
            create_school_group(name="4η ομάδα", ordering=None, school_names=[
                'ΠΡΟΤΥΠΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                'ΠΡΟΤΥΠΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
            ])

            # 5η ομάδα
            create_school_group(name="5η ομάδα", ordering=6, school_names=[
                '5ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '7ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '11ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                '2ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ',
            ])

            # 6η ομάδα
            create_school_group(name="6η ομάδα", ordering=8, school_names=[
                '12ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '6ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
            ])

            # 7η ομάδα
            create_school_group(name="7η ομάδα", ordering=5, school_names=[
                '8ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '9ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '10ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '11ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '7ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                '10ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                '13ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                '5ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ',
            ])

            # 8η ομάδα
            create_school_group(name="8η ομάδα", ordering=7, school_names=[
                '13ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                '8ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
                'ΕΣΠΕΡΙΝΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ',
            ])

            # 9η ομάδα
            create_school_group(name="9η ομάδα", ordering=3, school_names=[
                '1ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ',
                '6ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ',
            ])

            # 10η ομάδα
            create_school_group(name="10η ομάδα", ordering=None, school_names=[
                'ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ - ΓΥΜΝΑΣΙΟ',
                'ΚΑΛΛΙΤΕΧΝΙΚΟ ΓΥΜΝΑΣΙΟ',
            ])

            # 11η ομάδα
            create_school_group(name="11η ομάδα", ordering=None, school_names=[
                'ΕΙΔΙΚΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ',
                'ΕΕΕΕΚ ΗΡΑΚΛΕΙΟΥ',
                'ΕΠΑΛ ΕΙΔΙΚΗΣ ΑΓΩΓΗΣ',
            ])

            # 12η ομάδα
            create_school_group(name="12η ομάδα", ordering=9, school_names=[
                'ΓΥΜΝΑΣΙΟ Ν. ΑΛΙΚΑΡΝΑΣΣΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ Ν.ΑΛΙΚΑΡΝΑΣΣΟΥ',
                '3ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ',
            ])

            # 13η ομάδα
            create_school_group(name="13η ομάδα", ordering=10, school_names=[
                'ΓΥΜΝΑΣΙΟ ΑΡΧΑΝΩΝ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΧΑΝΩΝ',
            ])

            # 14η ομάδα
            create_school_group(name="14η ομάδα", ordering=11, school_names=[
                'ΓΥΜΝΑΣΙΟ ΜΕΛΕΣΩΝ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΕΛΕΣΩΝ',
            ])

            # 15η ομάδα
            create_school_group(name="15η ομάδα", ordering=12, school_names=[
                'ΓΥΜΝΑΣΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΡΚΑΛΟΧΩΡΙΟΥ',
                '1ο ΕΠΑ.Λ. ΑΡΚΑΛΟΧΩΡΙΟΥ',
            ])

            # 16η ομάδα
            create_school_group(name="16η ομάδα", ordering=13, school_names=[
                'ΓΥΜΝΑΣΙΟ ΒΙΑΝΝΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΒΙΑΝΝΟΥ',
            ])

            # 17η ομάδα
            create_school_group(name="17η ομάδα", ordering=14, school_names=[
                'ΓΥΜΝΑΣΙΟ ΚΑΣΤΕΛΛΙΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΑΣΤΕΛΙΟΥ',
            ])

            # 18η ομάδα

            create_school_group(name="18η ομάδα", ordering=15, school_names=[
                'ΓΥΜΝΑΣΙΟ ΘΡΑΨΑΝΟΥ',
            ])

            # 19η ομάδα
            create_school_group(name="19η ομάδα", ordering=16, school_names=[
                'ΓΥΜΝΑΣΙΟ ΜΟΧΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΧΟΥ',
            ])

            # 20η ομάδα
            create_school_group(name="20η ομάδα", ordering=17, school_names=[
                'ΓΥΜΝΑΣΙΟ ΜΑΛΙΩΝ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΑΛΙΩΝ',
                'ΓΥΜΝΑΣΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ Λ. ΧΕΡΣΟΝΗΣΟΥ',
            ])

            # 21η ομάδα
            create_school_group(name="21η ομάδα", ordering=18, school_names=[
                'ΓΥΜΝΑΣΙΟ ΕΠΙΣΚΟΠΗΣ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΕΠΙΣΚΟΠΗΣ',
            ])
            # 22η ομάδα

            create_school_group(name="22η ομάδα", ordering=20, school_names=[
                'ΓΥΜΝΑΣΙΟ ΤΕΦΕΛΙΟΥ',
            ])
            # 23η ομάδα

            create_school_group(name="23η ομάδα", ordering=21, school_names=[
                # 'ΕΠΑΣ ΑΣΤΕΡΟΥΣΙΩΝ',
                'ΓΥΜΝΑΣΙΟ ΠΥΡΓΟΥ',
            ])
            # 24η ομάδα

            create_school_group(name="24η ομάδα", ordering=22, school_names=[
                'ΓΥΜΝΑΣΙΟ ΧΑΡΑΚΑ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΧΑΡΑΚΑ',
            ])
            # 25η ομάδα
            create_school_group(name="25η ομάδα", ordering=23, school_names=[
                'ΓΥΜΝΑΣΙΟ ΑΣΗΜΙΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΣΗΜΙΟΥ'
            ])
            create_school_group(name="26η ομάδα", ordering=24, school_names=[
                'ΓΥΜΝΑΣΙΟ ΠΡΟΦΗΤΗ ΗΛΙΑ',
            ])
            create_school_group(name="27η ομάδα", ordering=25, school_names=[
                'ΓΥΜΝΑΣΙΟ ΤΥΛΙΣΟΥ',
            ])
            create_school_group(name="28η ομάδα", ordering=26, school_names=[
                'ΓΥΜΝΑΣΙΟ ΚΡΟΥΣΩΝΑ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΚΡΟΥΣΩΝΑ'
            ])
            create_school_group(name="29η ομάδα", ordering=27, school_names=[
                'ΓΥΜΝΑΣΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΟΥ ΜΥΡΩΝΑ'
            ])
            create_school_group(name="30η ομάδα", ordering=29, school_names=[
                'ΓΥΜΝΑΣΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ',
                'ΓΥΜΝΑΣΙΟ ΒΕΝΕΡΑΤΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΑΣ ΒΑΡΒΑΡΑΣ'
            ])
            create_school_group(name="31η ομάδα", ordering=30, school_names=[
                'ΓΥΜΝΑΣΙΟ ΖΑΡΟΥ',
                'ΓΥΜΝΑΣΙΟ ΓΕΡΓΕΡΗΣ',
            ])
            create_school_group(name="32η ομάδα", ordering=31, school_names=[
                'ΓΥΜΝΑΣΙΟ ΒΑΓΙΟΝΙΑΣ',
            ])
            create_school_group(name="33η ομάδα", ordering=32, school_names=[
                'ΓΥΜΝΑΣΙΟ ΜΟΙΡΩΝ',
                'ΓΥΜΝΑΣΙΟ ΑΓΙΩΝ ΔΕΚΑ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΜΟΙΡΩΝ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΓΙΩΝ ΔΕΚΑ',
                '1ο ΕΠΑ.Λ. ΜΟΙΡΩΝ',
            ])
            create_school_group(name="34η ομάδα", ordering=33, school_names=[
                'ΓΥΜΝΑΣΙΟ ΠΟΜΠΙΑΣ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΠΟΜΠΙΑΣ',
            ])
            create_school_group(name="35η ομάδα", ordering=34, school_names=[
                'ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΤΥΜΠΑΚΙΟΥ',
                'ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΤΥΜΠΑΚΙΟΥ'
            ])
            create_school_group(name="36η ομάδα", ordering=28, school_names=[
                'ΓΥΜΝΑΣΙΟ ΓΑΖΙΟΥ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΑΖΙΟΥ',
            ])

            create_school_group(name="37η ομάδα", ordering=19, school_names=[
                'ΓΥΜΝΑΣΙΟ ΓΟΥΒΩΝ',
                'ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΓΟΥΒΩΝ',
            ])
            create_school_group(name="38η ομάδα", ordering=None, school_names=[
                'ΕΕΕΕΚ ΤΥΜΠΑΚΙΟΥ',
            ])

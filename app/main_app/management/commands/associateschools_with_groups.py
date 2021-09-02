from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from users.models import User, Profile
from main_app.models import Entry
from schools.models import School, SchoolGroup


class Command(BaseCommand):

    def handle(self, *args, **options):

        with transaction.atomic():

            # reset all school groups
            updated_schools = School.objects.filter(school_group__isnull=False).update(school_group=None)
            self.stdout.write(self.style.SUCCESS('[*] removed "%s" school(s) from their school group' % updated_schools))

            # remove all groups
            deleted_school_groups = SchoolGroup.objects.all().delete()

            # 1η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="1η ομάδα")
            s: School = School.objects.get(name='1ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='6ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='ΕΣΠΕΡΙΝΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='1ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='3ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 2η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="2η ομάδα")

            s: School = School.objects.get(name='3ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='5ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='4ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ (ΕΣΠΕΡΙΝΟ)')
            s.school_group = sg
            s.save()

            # 3η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="3η ομάδα")

            s: School = School.objects.get(name='2ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='4ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='2ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='4ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 4η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="4η ομάδα")

            s: School = School.objects.get(name='ΠΡΟΤΥΠΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='ΠΡΟΤΥΠΟ ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 5η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="5η ομάδα")

            s: School = School.objects.get(name='5ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='7ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='11ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='2ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 6η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="6η ομάδα")

            s: School = School.objects.get(name='12ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='6ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 7η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="7η ομάδα")

            s: School = School.objects.get(name='8ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='9ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='10ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='11ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='7ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='10ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='13ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='5ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 8η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="8η ομάδα")

            s: School = School.objects.get(name='13ο ΓΥΜΝΑΣΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='8ο ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='ΕΣΠΕΡΙΝΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 9η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="9η ομάδα")

            s: School = School.objects.get(name='1ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='6ο ΕΠΑ.Λ. ΗΡΑΚΛΕΙΟΥ')
            s.school_group = sg
            s.save()

            # 10η ομάδα
            sg: SchoolGroup = SchoolGroup.objects.create(name="10η ομάδα")

            s: School = School.objects.get(name='ΜΟΥΣΙΚΟ ΣΧΟΛΕΙΟ - ΓΥΜΝΑΣΙΟ')
            s.school_group = sg
            s.save()

            s: School = School.objects.get(name='ΚΑΛΛΙΤΕΧΝΙΚΟ ΓΥΜΝΑΣΙΟ')
            s.school_group = sg
            s.save()











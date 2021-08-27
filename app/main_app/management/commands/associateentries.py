from django.core.management.base import BaseCommand, CommandError
from users.models import User, Profile
from main_app.models import Entry, School


def connect_entries_to_schools(school):
    # type: (School) -> List[Entry]
    if school is None:
        # we are working for all users
        users = User.objects.all()  # type: list[User]
    else:
        users = [school.managed_by.user, ]  # type: list[User]

    # store the associated (actually processed) users/profile in a list
    associated_entries = list()

    for user in users:
        entries = Entry.objects.filter(owner=user)
        for entry in entries:
            if entry.school is None:
                entry.school = user.profile.school
                entry.save()

                associated_entries.append(entry)

    return associated_entries


class Command(BaseCommand):
    """
    Associate Entries with the corresponding school
    """

    help = 'Associate blind entries with their corresponding school'

    def add_arguments(self, parser):
        parser.add_argument('--school_email', type=str, help="The school to associate")

    def handle(self, *args, **options):
        
        school_email = options.get('school_email', None)
        if school_email is not None:
            # user email specified, so we are running in a "single-user" mode
            try:
                school = School.objects.get(email=school_email)
                self.stdout.write(self.style.SUCCESS('[*] school "%s" found in database' % school_email))
            except School.DoesNotExist:
                raise CommandError('School "%s" does not exist' % school_email)
        else:
            # no user email specified, go ahead and process the whole database
            self.stdout.write(self.style.SUCCESS('[*] No school specified, scanning/processing whole database.'))
            school = None
                
        processed_entries = connect_entries_to_schools(school=school)

        if len(processed_entries) > 0:
            self.stdout.write()
            for entry in processed_entries:
                self.stdout.write('[=] associated school "{email}" with entry "{entry}"'.format(
                    email=entry.school.email,
                    entry=entry,
                    )
                )   
            self.stdout.write()
            self.stdout.write(self.style.SUCCESS('[*] Successfully updated {sum} entrie(s)'.format(sum=len(processed_entries))))
        else:
            # command did not update any entry
            self.stdout.write(self.style.WARNING('[*] No entry found that need updating.'))


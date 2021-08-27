from django.core.management.base import BaseCommand, CommandError
from excels.views import reconnect_users_to_schools
from users.models import User


class Command(BaseCommand):
    """
    Associate User (profile) with the corresponding school
    """

    help = 'Associate blind users (or a specific user) with their corresponding school'

    def add_arguments(self, parser):
        parser.add_argument('--user_email', type=str, help="The user to associate")

    def handle(self, *args, **options):
        
        user_email = options.get('user_email', None)
        if user_email is not None:
            # user email specified, so we are running in a "single-user" mode
            try:
                user = User.objects.get(email=user_email)
                self.stdout.write(self.style.SUCCESS('[*] User "%s" found in database' % user_email))
            except User.DoesNotExist:
                raise CommandError('User "%s" does not exist' % user_email)
        else:
            # no user email specified, go ahead and process the whole database
            self.stdout.write(self.style.SUCCESS('[*] No user specified, scanning/processing whole database.'))
            user = None
                
        processed_profiles = reconnect_users_to_schools(user=user)

        if len(processed_profiles) > 0:
            self.stdout.write()
            for profile in processed_profiles:
                self.stdout.write('[=] associated profile "{email}" with school "{school}"'.format(
                    email=profile.user.email,
                    school=profile.school.name,
                    )
                )   
            self.stdout.write()
            self.stdout.write(self.style.SUCCESS('[*] Successfully updated {sum} user profile(s)'.format(sum=len(processed_profiles))))
        else:
            # command did not update any profile
            self.stdout.write(self.style.WARNING('[*] No user profiles found that need updating.'))


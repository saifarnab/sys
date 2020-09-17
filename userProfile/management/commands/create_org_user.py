from django.core.management.base import BaseCommand
from userProfile.models import OrgProfile, User


class Command(BaseCommand):
    help = 'Create demo org user'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.create_user(username='demo@demo.com', email='demo@demo.com', password='123456', role='Org')
            if user:
                org = OrgProfile.objects.create(
                    user=user,
                    name='DIIT',
                    contact_number='017136',
                    email='demo@demo.com',
                    address='Dhanmondi 27',

                )
            return 'user created'
        except Exception as e:
            print(e)

from django.core.management.base import BaseCommand
from userProfile.models import OrgProfile, User, TrainerProfile


class Command(BaseCommand):
    help = 'Create demo trainer user'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.create_user(username='trainer@demo.com', email='trainer@demo.com', password='123456', role='Trainer')
            if user:
                org = TrainerProfile.objects.create(
                    user=user,
                    name='Saif',
                    contact_number='017136',
                    email='demo@demo.com',
                    address='Dhanmondi 27',
                )
            return 'user created'
        except Exception as e:
            print(e)

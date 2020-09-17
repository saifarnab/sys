from userProfile.models import User, OrgProfile


class CreateUser(object):

    def org_user(self):
        user = User.objects.create_user(username='demo@demo.com', email='demo@demo.com', password='123', role='Org')
        if user:
            org = OrgProfile.objects.create(
                user=user,
                name='DIIT',
                contact_number='017136',
                email='demo@demo.com',
                address='Dhanmondi 27',

            )
        return 'user created'


if __name__ == "__main__":
    create_user = CreateUser()
    print(create_user.org_user())


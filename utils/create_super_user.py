from django.contrib.auth.models import User

from kindergarten.models import UserAdditionInfo

user = User.objects.create_user(
    username='root',
    password='root',
)
UserAdditionInfo(
    user=user,
    surname='surname',
    name='name',
    patronymic='patronymic',
    phone='phone',
    comments='comments'
).save()
user.is_superuser = True
user.is_staff = True
user.save()

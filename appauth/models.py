
from datetime import datetime

from django.db.models import Model, Manager
from django.db.models import (CharField, EmailField, IntegerField,
                              BooleanField, FileField, DateTimeField)
from django.db.models import UUIDField, OneToOneField, CASCADE

from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    # TODO クラス名考える
    username = CharField(max_length=150)
    email = EmailField(max_length=150, unique=True)
    age = IntegerField(null=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    picture = FileField(null=True, upload_to='puture/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    class Meta:
        default_permissions = ()
        permissions = [
            ('pl', 'プロジェクトリーダー'),
            ('pm', 'プロジェクトマネージャー'),
        ]

    def get_absolute_url(self):
        return reverse_lazy('appauth:home')


class UserActivateTokensManager(Manager):

    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()
            # expired_at__gte=timezone.localtime()  # local
        ).first()
        user = user_activate_token.user
        user.is_active = True
        # print('■' + str(user.id))
        user.save()


class UserActivateTokens(Model):
    token = UUIDField(db_index=True)
    expired_at = DateTimeField()
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    objects = UserActivateTokensManager()

    class Meta:
        db_table = 'user_activate_tokens'

# @receiver(post_save, sender=AppUser)
# def publish_token(sender, instance, **kwargs):
#     user_activate_token = UserActivateTokens.objects.create(
#         user=instance, token=str(uuid4()), expired_at= datetime.now()+timedelta(days=1)
#     )

#     print(f'http://127.0.0.1:8000/appauth/activate_user/{user_activate_token.token}')

# def create_token(user):
#     user_activate_token = UserActivateTokens.objects.create(
#         user=user, token=str(uuid4()), expired_at= datetime.now()+timedelta(days=1)
#     )
#     print('■ここも来たよ')

#     print(f'http://127.0.0.1:8000/appauth/activate_user/{user_activate_token.token}')

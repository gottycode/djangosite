
from datetime import datetime,timedelta
from uuid import uuid4
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
            username = username,
            email = email
        )
        user.set_passwor(password)
        user.save(using=self._db)
        print('■来たよ')
        # create_token(user)

        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    # TODO クラス名考える
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    age = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='puture/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('account:home')

class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user
        user.is_active = True
        # print('■' + str(user.id))
        user.save()

class UserActivateTokens(models.Model):
    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = UserActivateTokensManager()

    class Meta:
        db_table = 'user_activate_tokens'

# @receiver(post_save, sender=AppUser)
# def publish_token(sender, instance, **kwargs):
#     user_activate_token = UserActivateTokens.objects.create(
#         user=instance, token=str(uuid4()), expired_at= datetime.now()+timedelta(days=1)
#     )

#     print(f'http://127.0.0.1:8000/account/activate_user/{user_activate_token.token}')

def create_token(user):
    user_activate_token = UserActivateTokens.objects.create(
        user=user, token=str(uuid4()), expired_at= datetime.now()+timedelta(days=1)
    )
    print('■ここも来たよ')

    print(f'http://127.0.0.1:8000/account/activate_user/{user_activate_token.token}')
 
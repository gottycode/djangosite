
from datetime import datetime

from django.db.models import Model, Manager
from django.db.models import (CharField, EmailField, DateTimeField,
                              BooleanField, FileField)
from django.db.models import UUIDField, OneToOneField, CASCADE
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db.models.fields import DateField


class UserManager(BaseUserManager):
    """Userクラスの操作を行う"""

    def create_user(self, username, email, password=None):
        """ユーザー登録"""

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
        # ハッシュ値にしてパスワード登録
        user.set_password(password)

        # 権限登録
        user.is_staff = True
        user.is_superuser = True

        # DB登録
        user.save(using=self._db)

        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    """ユーザークラス"""

    username = CharField('ユーザー名', max_length=150)
    email = EmailField('メール', max_length=150, unique=True)
    birthday = DateField('誕生日', null=True)
    is_active = BooleanField('有効フラグ', default=True)
    is_staff = BooleanField('', default=False)
    is_superuser = BooleanField('管理者フラグ', default=False)  # TODO 管理画面が見れる、初回のユーザ登録に
    picture = FileField('写真', null=True, upload_to='puture/', blank=True)  # TODO 未使用

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    class Meta:
        default_permissions = ()  # Djangoデフォルトの権限を無効
        permissions = [
            ('mb', 'メンバー'),
            ('tl', 'チームリーダー'),
            ('pl', 'プロジェクトリーダー'),
            ('pm', 'プロジェクトマネージャー'),
            ('po', '顧客'),
        ]


class UserActivateTokensManager(Manager):
    """ユーザートークン操作クラス"""

    def activate_user_by_token(self, token):

        # 取得したトークンからユーザーモデルを取得
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user

        # ステータスを有効にして保存
        user.is_active = True
        user.save()


class UserActivateTokens(Model):
    """ユーザートークン"""

    token = UUIDField('仮登録トークン', db_index=True)
    expired_at = DateTimeField('有効期限')
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    objects = UserActivateTokensManager()

    class Meta:
        default_permissions = ()
        db_table = 'user_activate_tokens'

# @receiver(post_save, sender=AppUser)
# def publish_token(sender, instance, **kwargs):
#     user_activate_token = UserActivateTokens.objects.create(
#         user=instance, token=str(uuid4()), expired_at= datetime.now()+timedelta(days=1)
#     )

#     print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')

# def create_token(user):
#     user_activate_token = UserActivateTokens.objects.create(
#         user=user, token=str(uuid4()), expired_at= datetime.now()+timedelta(days=1)
#     )
#     print('■ここも来たよ')

#     print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')

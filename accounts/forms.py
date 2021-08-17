from django.forms import (BooleanField, CharField, DateField,
                          EmailField, PasswordInput, ValidationError,
                          ChoiceField, RadioSelect,)
from django import forms  # 仮
from django.forms import ModelForm, DateInput
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from accounts.models import AppUser


class RegistForm(ModelForm):
    username = CharField(label='名前')
    birthday = DateField(label='誕生日', widget=DateInput(attrs={"type": "date"}), required=False)
    email = EmailField(label='メールアドレス')
    password = CharField(label='パスワード', widget=PasswordInput())
    confirm_password = CharField(label='パスワード再入力', widget=PasswordInput())

    class Meta:
        model = AppUser
        fields = ['username', 'birthday', 'email', 'password', 'confirm_password']

    def clean(self):
        """項目間の入力チェック"""

        # パスワードとパスワード再入力の一致確認
        cleaned_data = super(RegistForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)

    def save(self, commit=False):

        # パスワードをハッシュ値で登録
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class RegistForm2(ModelForm):

    # 仮登録
    username = CharField(label='名前')
    birthday = DateField(label='誕生日', widget=DateInput(attrs={"type": "date"}), required=False)
    email = EmailField(label='メールアドレス')

    class Meta:
        model = AppUser
        fields = ['username', 'email', 'birthday']


class CompleteRegistrationForm(ModelForm):
    """本登録"""

    password = CharField(label='パスワード', widget=PasswordInput())
    confirm_password = CharField(label='パスワード再入力', widget=PasswordInput())

    class Meta:
        model = AppUser
        fields = ['password', 'confirm_password']

    def clean(self):
        """項目間のバリデーション"""

        # パスワードとパスワード再入力の一致を確認
        cleaned_data = super(CompleteRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)

    def save(self, commit=False):

        # パスワードをハッシュ値にして登録
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UpdateUserForm(ModelForm):
    """ユーザー情報更新"""

    CHOICE = {
        ('0', 'なし'),
        ('1', 'あり'),
    }

    username = CharField(label='名前')
    birthday = DateField(label='誕生日', widget=DateInput(attrs={"type": "date"}), required=False)
    email = EmailField(label='メールアドレス')
    password = CharField(label='パスワード', widget=PasswordInput(), required=False)
    confirm_password = CharField(label='パスワード再入力', widget=PasswordInput(), required=False)
    print('♪')
    typing = ContentType(app_label='accounts', model='appuser')
    print(typing.values('id'))
    perms = forms.ModelMultipleChoiceField(
        label='権限',
        queryset=Permission.objects.filter(content_type_id=8).all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = AppUser
        fields = ['username', 'birthday', 'email', 'password', 'confirm_password']

    def clean(self):

        cleaned_data = super(UpdateUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        print('★')
        perms = self.cleaned_data['perms']
        for perm in perms:
            print(perm)
            user.user_permissions.add(perm)
        user.save()
        # self.save_m2m()

        return user


class UserLoginForm(AuthenticationForm):
    """ログイン"""

    username = EmailField(label='メールアドレス')
    password = CharField(label='パスワード')
    remember = BooleanField(label='ログイン情報保持', required=False)

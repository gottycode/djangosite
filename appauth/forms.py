from django.forms import (BooleanField, CharField, IntegerField,
                          EmailField, PasswordInput, ValidationError)
from django.forms import ModelForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

from appauth.models import AppUser


class RegistForm(ModelForm):
    username = CharField(label='名前')
    age = IntegerField(label='年齢', min_value=0)
    email = EmailField(label='メールアドレス')
    password = CharField(label='パスワード', widget=PasswordInput())
    confirm_password = CharField(label='パスワード再入力', widget=PasswordInput())

    class Meta:
        model = AppUser
        fields = ['username', 'age', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(RegistForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        print('regist1')
        return user


class RegistForm2(ModelForm):
    username = CharField(label='名前')
    age = IntegerField(label='年齢', min_value=0)
    email = EmailField(label='メールアドレス')

    class Meta:
        model = AppUser
        fields = ['username', 'email', 'age']

    # def save(self, commit=False):
    #     user = super().save(commit=False)

    #     print('regist2')
    #     return user


class CompleteRegistrationForm(ModelForm):

    password = CharField(label='パスワード', widget=PasswordInput())
    confirm_password = CharField(label='パスワード再入力', widget=PasswordInput())

    class Meta:
        model = AppUser
        fields = ['password', 'confirm_password']

    def clean(self):
        cleaned_data = super(CompleteRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = EmailField(label='メールアドレス')
    password = CharField(label='パスワード')
    remember = BooleanField(label='ログイン情報保持', required=False)


class UpdateUserForm(ModelForm):

    username = CharField(label='名前')
    age = IntegerField(label='年齢', min_value=0)
    email = EmailField(label='メールアドレス')
    password = CharField(label='パスワード', widget=PasswordInput(), required=False)
    confirm_password = CharField(label='パスワード再入力', widget=PasswordInput(), required=False)

    class Meta:
        model = AppUser
        fields = ['username', 'age', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(CompleteRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

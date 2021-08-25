from datetime import datetime, timedelta
import os
from uuid import uuid4
import logging

from django.shortcuts import redirect, render, get_object_or_404
from django.forms import ChoiceField, RadioSelect
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from accounts.forms import (RegistForm, RegistForm2,
                            UserLoginForm, CompleteRegistrationForm,
                            UpdateUserForm)
from accounts.models import AppUser, UserActivateTokens

# ロガー
application_logger = logging.getLogger('application-logger')
error_logger = logging.getLogger('error-logger')


class HomeView(TemplateView):
    """ホーム画面"""

    template_name = os.path.join('auth', 'home.html')


class RegistUserView(CreateView):
    """本登録"""

    template_name = os.path.join('auth', 'regist.html')
    form_class = RegistForm

    def get_success_url(self):
        return reverse_lazy('accounts:home')


class RegistUser2View(CreateView):
    """仮登録"""

    template_name = os.path.join('auth', 'regist2.html')
    form_class = RegistForm2
    model = AppUser

    def form_valid(self, form):
        application_logger.info('仮登録に来た')

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        user_activate_token = UserActivateTokens.objects.create(
            user=user, token=str(uuid4()), expired_at=datetime.now()+timedelta(days=1)
        )

        # print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')
        print('このURLをメールで送る')
        print(f'http://127.0.0.1:8000/accounts/complete_registration/{user_activate_token.token}')

        # return redirect('accounts:home')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:home')


class UserLoginView(LoginView):
    template_name = os.path.join('auth', 'login.html')
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(12000)
        print('呼ばれた')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('auth', 'user.html')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CompleteRegistrationView(View):
    template_name = os.path.join('auth', 'complete_registration.html')
    form_class = CompleteRegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        token = kwargs['token']
        print(token)
        # return render(request, self.template_name, {'form': form, "first": first_name})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # TODO ユーザーのパスワードを保存して
            # is_activeを更新する
            form.save()
        else:
            return render(request, self.template_name, {'form': form})  # エラーメッセージを含んだフォームをセットして再表示

        return redirect("accounts:home")


class UserListView(View, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = os.path.join('auth', 'user_list.html')

    def get(self, request, *args, **kwargs):
        users = AppUser.objects.all()
        for user in users:
            perms = user.user_permissions
            for perm in perms.all():
                # print(dir(perm))
                print(perm.name)

        return render(request, self.template_name, {'users': users})


class UpdateUserView(PermissionRequiredMixin, View):

    permission_required = ('accounts.pm',)

    template_name = os.path.join('auth', 'update_user.html')
    form_class = UpdateUserForm

    def get(self, request, *args, **kwargs):

        # print('★')
        # print(super().has_permission())
        # print(super().get_permission_required())

        # print(dir(request))
        # print(kwargs)
        app_user = get_object_or_404(AppUser, id=kwargs['id'])
        perms = app_user.user_permissions
        print('--------------------------------')
        # print(perms.values('id',))
        perm_list = [k['id'] for k in perms.values('id',)]
        # print(AppUser.Meta.permissions)
        form = UpdateUserForm(request.GET or None, instance=app_user)

        # for perm in perms:
        #     form.fields[perm] = ChoiceField(label='属性', widget=RadioSelect, choices=CHOICE, initial=0)
        print('*******************************************')
        print(form.fields['perms'].initial)
        form.fields['perms'].initial = perm_list

        print(form.fields['perms'].initial)

        return render(request, self.template_name, {'form': form, 'permittions': perms.all()})

    def post(self, request, *args, **kwargs):

        id = kwargs['id']
        user = get_object_or_404(AppUser, pk=id)
        form = UpdateUserForm(request.POST or None, instance=user)  # TODO modelformではなくformの場合はinitial=listで
        if form.is_valid():
            form.save()
            # form.save_m2m()
            return redirect('accounts:user_list')

        else:
            message = '再入力してください'
            context = {
                'form': form,
                'message': message
            }
            return render(request, self.template_name, context)


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'auth/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        print('ここここ')
        return context


class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'auth/password_change_done.html'

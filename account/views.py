from datetime import datetime, timedelta
from uuid import uuid4
import logging
from django.forms import forms

from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import RegistForm, RegistForm2, UserLoginForm, CompleteRegistrationForm
from .models import AppUser, UserActivateTokens

application_logger = logging.getLogger('application-logger')
error_logger = logging.getLogger('error-logger')


class HomeView(TemplateView):
    template_name = 'home.html'


class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm


class RegistUser2View(CreateView):
    template_name = 'regist2.html'
    form_class = RegistForm2
    model = AppUser

    def form_valid(self, form):
        application_logger.warning('仮登録に来た')

        user = form.save(commit=False)
        user.is_active = False
        user.save()
        print(user)

        user_activate_token = UserActivateTokens.objects.create(
            user=user, token=str(uuid4()), expired_at=datetime.now()+timedelta(days=1)
        )

        print(f'http://127.0.0.1:8000/account/activate_user/{user_activate_token.token}')
        print(f'http://127.0.0.1:8000/account/complete_registration/{user_activate_token.token}')

        # return redirect('account:home')

        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'
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
    template_name = 'user.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


"""
class ActivateView(TemplateView):
    template_name = 'activate_user.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = self.kwargs.get('token')
        print(token)
        user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)

        return self.render_to_response(context)
"""


class CompleteRegistrationView(View):
    template_name = "complete_registration.html"
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

        return redirect("account:home")

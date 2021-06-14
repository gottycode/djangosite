from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import RegistForm,RegistForm2, UserLoginForm
from .models import UserActivateTokens
class HomeView(TemplateView):
    template_name = 'home.html'

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

class RegistUser2View(CreateView):
    template_name = 'regist2.html'
    form_class = RegistForm2


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

class ActivateView(TemplateView):
    template_name = 'activate_user.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = self.kwargs.get ('token')
        print(token)
        user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)

        return self.render_to_response(context)
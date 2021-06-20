from django.urls import path
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserView, RegistUser2View,  # ActivateView,
    CompleteRegistrationView
)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import reverse_lazy
app_name = 'account'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('regist2/', RegistUser2View.as_view(), name='regist2'),
    # path('activate_user/<uuid:token>', ActivateView.as_view(), name='activate'),
    path('complete_registration/<uuid:token>', CompleteRegistrationView.as_view(), name='complete_registration'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('change_password/', PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('user/', UserView.as_view(), name='user'),

]

from django.urls import path

from accounts.views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserView, RegistUser2View, PasswordChangeView,
    CompleteRegistrationView, UserListView, UpdateUserView,
    PasswordChangeDoneView
)
app_name = 'accounts'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('regist2/', RegistUser2View.as_view(), name='regist2'),
    # path('activate_user/<uuid:token>', ActivateView.as_view(), name='activate'),
    path('complete_registration/<uuid:token>', CompleteRegistrationView.as_view(), name='complete_registration'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('user/', UserView.as_view(), name='user'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('update_user/<int:id>', UpdateUserView.as_view(), name='update_user'),
]

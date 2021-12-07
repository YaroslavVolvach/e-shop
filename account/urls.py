from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm, CustomPasswordResetForm, CustomSetPasswordForm
from .api.urls import urlpatters as api_urls

app_name = 'account'

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(
         authentication_form=LoginForm,
         template_name='account/user_login.html',
         redirect_authenticated_user='/'
         ), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
         template_name='account/password_reset.html',
         email_template_name='account/password_reset_email.html',
         form_class=CustomPasswordResetForm,
         success_url=reverse_lazy('account:password_reset_done')
         ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name='account/password_reset_done.html',
         ), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='account/password_reset_confirm.html',
         form_class=CustomSetPasswordForm,
         success_url=reverse_lazy('account:password_reset_complete')
         ), name='password_reset_confirm'),

    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='account/password_reset_complete.html',
         ), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>', views.profile, name='profile_for_staff'),
    path('profile/change/<int:id>/', views.UpdateProfile.as_view(), name='change_profile'),
    path('profile/change_image/', views.change_image, name='change_image'),
    path('profile/remove_image/', views.remove_image, name='remove_image'),
    path('profile/change_password/', views.PasswordChange.as_view(), name='change_password'),
    path('profile/change_email/<int:id>', views.EmailChange.as_view(), name='change_email'),
    path('users/<category>/', views.UserList.as_view(), name='users'),
    path('blacklist/<int:user_id>/<category>/', views.blacklist, name='blacklist'),
    path('permissions/<int:user_id>/<category>/', views.permissions, name='permissions'),
    path('api/', include(api_urls))
]

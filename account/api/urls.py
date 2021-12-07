from django.urls import path, include
from account.api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatters = [
    path('', views.UserListApiView.as_view(), name='api-list'),
    path('user-detail/<int:id>', views.UserDetailAPIView.as_view(), name='api-detail'),
    path('user-update/<int:id>', views.UserUpdateAPIView.as_view(), name='api-update'),
    path('user-ban/<int:id>', views.UserBanOrUnbanAPIView.as_view(), name='api-ban'),
    path('user-permission/<int:id>', views.ChangePermissionAPIView.as_view(), name='api-permission'),
    path('registration/', views.RegistrAPIVIEW.as_view(), name='api-registration'),
    path('login/', obtain_auth_token, name='api-login'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset'))
]

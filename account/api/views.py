from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from account.api import serializers, permission
from account.models import CustomUser


class RegistrAPIVIEW(CreateAPIView):
    serializer_class = serializers.RegistrationAPISerialazer
    queryset = CustomUser.objects.all()


class UserListApiView(ListAPIView):
    serializer_class = serializers.UserAPISerialazer
    queryset = CustomUser.objects.all()


class UserDetailAPIView(RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = serializers.UserAPISerialazer
    queryset = CustomUser.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [permission.IsOwnerOrReadOnly]
    lookup_field = 'id'
    serializer_class = serializers.UserAPISerialazer
    queryset = CustomUser.objects.all()


class UserBanOrUnbanAPIView(UpdateAPIView):
    permission_classes = [permission.ChangePermission]
    lookup_field = 'id'
    serializer_class = serializers.UserBanOrUnbanAPISerialazer
    queryset = CustomUser.objects.all()


class ChangePermissionAPIView(UpdateAPIView):
    permission_classes = [permission.ChangePermission]
    lookup_field = 'id'
    serializer_class = serializers.ChangePermissionAPISerialazer
    queryset = CustomUser.objects.all()

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import get_objects_for_user
from rest_framework import permissions, serializers, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from apps.accounts import defaults
from apps.api.v1.permissions import ObjectPermissions
from apps.api.v1.serializers import BadRequestResponseSerializer
from apps.api.v1.serializers.accounts import (
    UserFullSerializer, UserRegistrationSerializer, UserChangePasswordSerializer,
    UserRestorePasswordSerializer, UploadUserPhotoSerializer
)
from apps.api.v1.tokens import EmailVerifyTokenGenerator
from apps.api.v1.viewsets import ExtendedModelViewSet

User = get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class UserViewSet(ExtendedModelViewSet):
    """
    Добавление нового пользователя

    :return 201

    retrieve:
    Возвращает данные пользователя

    :param ID пользователя
    :return 200

    list:
    Выводит список всех пользователей

    :return 200

    update:
    Изменение данных пользователя

    :param ID пользователя
    :return 200

    partial_update:
    Частичное обновление пользовательских данных

    :param ID пользователя
    :return 200

    delete:
    Удаление пользователя

    :param ID пользователя
    :return 204
    """

    queryset = User.objects.exclude(username='AnonymousUser')
    serializer_class = UserFullSerializer
    serializer_class_map = {
        'registration': UserRegistrationSerializer,
        'change_password': UserChangePasswordSerializer,
        'restore_password': UserRestorePasswordSerializer,
        'upload_photo': UploadUserPhotoSerializer,
    }
    permission_classes = (ObjectPermissions,)
    permission_map = {
        'registration': permissions.AllowAny,
        'verify_email': permissions.AllowAny,
        'restore_password': permissions.AllowAny,
    }
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = (
        'id', 'username', 'email', 'phone', 'gender', 'first_name', 'middle_name', 'last_name', 'birthday',
        'last_login', 'date_joined'
    )
    search_fields = ('$username', '$first_name', '$middle_name', '$last_name', '$email', '$phone')
    ordering = ('id',)

    def get_queryset(self):
        users = get_objects_for_user(self.request.user, 'accounts.view_user', accept_global_perms=False)
        return users.exclude(username='AnonymousUser')

    @swagger_auto_schema(responses={200: serializers.Serializer, 400: BadRequestResponseSerializer})
    @action(methods=['get'], detail=False)
    def me(self, request, pk=None, **kwargs):
        """
        Возвращает данные пользователя

        :param request: auth user
        :return 200
        """
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: UserChangePasswordSerializer,
            400: BadRequestResponseSerializer,
            410: BadRequestResponseSerializer,
        }
    )
    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        """
        Смена пароля пользователя

        :param request: password, password1, password2
        :return: 200
        """
        serializer = self.get_serializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = UserFullSerializer(instance=request.user).data
            return Response(data)

    @swagger_auto_schema(responses={200: serializers.Serializer, 400: BadRequestResponseSerializer})
    @action(methods=['patch'], detail=True, url_path='upload-photo')
    def upload_photo(self, request, pk=None, **kwargs):
        """
        Загрузка фотографии пользователя base64.

        :return 200
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            photo = serializer.save()
            if photo is None:
                user.delete_photo()
            else:
                user.photo.save(photo.name, photo)
                user.save()
            return Response()

    @swagger_auto_schema(responses={201: UserRegistrationSerializer, 400: BadRequestResponseSerializer})
    @action(methods=['post'], detail=False)
    def registration(self, request):
        """
        Регистрация пользователя через форму регистрации, с отправкой email уведомления

        :param: username, first_name, last_name, email, phone, password, passworddup.
        :return 201
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            data = UserFullSerializer(instance=user).data
            return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={200: serializers.Serializer, 400: BadRequestResponseSerializer})
    @action(methods=['get'], detail=True, url_path=r'verify-email/(?P<key>[^/.]+)')
    def verify_email(self, request, pk=None, key=None, **kwargs):
        """
        Подтверждение адреса электронной почты

        :param: id-идентификатор пользователя, key - Уникальный ключ
        :return 200
        """
        user = get_object_or_404(User, pk=pk)
        is_valid_token = EmailVerifyTokenGenerator().check_token(user, key)
        if is_valid_token:
            user.is_active = True
            user.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'token': _('Not valid email token')}}, status=status.HTTP_400_BAD_REQUEST)

    def _gender(self):
        genders = [{"value": k, "text": v} for k, v in defaults.GENDER_CHOICES]
        return genders

    @swagger_auto_schema(responses={200: serializers.Serializer, 404: BadRequestResponseSerializer})
    @action(methods=['post'], detail=False, url_path=r'restore-password')
    def restore_password(self, request, pk=None, **kwargs):
        """
        Востановление пароля, небезопасный метод, пользователю приходит в письме его новый пароль

        :return 200
        """
        user = get_object_or_404(User, username=request.data['username'])
        serializer = self.get_serializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)

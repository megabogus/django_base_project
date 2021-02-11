import base64
import imghdr
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError

User = get_user_model()


class UserFullSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False, validators=[UniqueValidator(User.objects.all())])
    email = serializers.EmailField(required=False, validators=[UniqueValidator(User.objects.all())])
    full_name = serializers.SerializerMethodField()
    change_password = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_change_password(self, obj):
        return obj.get_change_password()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'full_name', 'first_name', 'middle_name', 'last_name', 'gender', 'phone', 'email',
            'photo', 'change_password', 'birthday', 'last_login', 'date_joined',
        )
        read_only_fields = (
            'id', 'full_name', 'photo', 'last_login', 'date_joined'
        )


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[MaxLengthValidator(150), UniqueValidator(User.objects.all())])
    first_name = serializers.CharField(validators=[MaxLengthValidator(30)])
    middle_name = serializers.CharField(validators=[MaxLengthValidator(30)], required=False)
    last_name = serializers.CharField(validators=[MaxLengthValidator(150)])
    email = serializers.EmailField(validators=[UniqueValidator(User.objects.all())])
    phone = PhoneNumberField(validators=[UniqueValidator(User.objects.all())])

    password = serializers.CharField()
    passworddup = serializers.CharField()

    def validate_passworddup(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['passworddup']:
            raise ValidationError(detail=_('Пароли не совпадают'))
        return super().validate(attrs)

    def create(self, validated_data):
        username = validated_data.get('username')
        user = User.objects.create(
            username=username,
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            birthday=validated_data.get('birthday'),
            phone=validated_data.get('phone'),
            is_active=False,
        )
        user.set_password(validated_data.get('passworddup'))
        user.save()
        user.send_verify_email()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password2'])
        instance.change_password = timezone.now()
        instance.save()
        return self.instance

    def validate_password(self, value):
        if not self.instance.check_password(value):
            raise ValidationError(detail=_('Введенный пароль некорректен'))
        return value

    def validate_password1(self, value):
        validate_password(value)
        return value

    def validate_password2(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError(detail=_('Пароли не совпадают'))
        return super().validate(attrs)


class UserRestorePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

    def update(self, instance, validated_data):
        instance.change_password = None
        instance.save()
        instance.send_change_password_email()
        return self.instance


class UploadUserPhotoSerializer(serializers.Serializer):
    photo = serializers.CharField(allow_null=True)

    def validate_photo(self, value):
        if value is None:
            return None
        try:
            header, data = value.split(';base64,')
            decoded = base64.b64decode(data)
        except Exception as e:
            raise ValidationError(f"Произошла ошибка {e}")
        else:
            return decoded

    def create(self, validated_data):
        photo = validated_data['photo']
        if photo is None:
            return None

        file_name = str(uuid.uuid4())
        file_extension = imghdr.what(file_name, photo)
        file_extension = 'jpg' if file_extension == 'jpeg' else file_extension
        complete_file_name = f'{file_name}.{file_extension}'
        return ContentFile(photo, name=complete_file_name)

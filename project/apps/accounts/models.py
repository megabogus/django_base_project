import datetime
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import CreatedDeletedModel, CreatedModel, UUIDModel
from apps.api.v1.tokens import EmailVerifyTokenGenerator
from . import defaults
from .tasks import send_templated_email


class User(CreatedDeletedModel, auth_models.AbstractUser):
    first_name = models.CharField(_('Имя'), max_length=255)
    middle_name = models.CharField(_('Отчество'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('Фамилия'), max_length=255)
    birthday = models.DateField(_('Дата рождения'), null=True, blank=True)
    gender = models.PositiveSmallIntegerField(
        _('Пол'),
        choices=defaults.GENDER_CHOICES,
        default=defaults.NOT_DEFINED
    )
    phone = PhoneNumberField(_('Телефон'), null=True, blank=False, unique=False, help_text=_("например +41524204242"))
    email = models.EmailField(_('email адрес'), null=True, blank=False, unique=True, db_index=True)
    photo = models.ImageField(_('Фотография пользователя'), upload_to='user_photos', null=True, blank=True)
    change_password = models.DateField(_("Дата смены пароля"), blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.username)

    def get_full_name(self):
        if self.middle_name:
            return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)
        else:
            return "{} {}".format(self.last_name, self.first_name)

    def get_change_password(self):
        if self.change_password is None:
            return True
        elif datetime.date.today() > self.change_password + datetime.timedelta(days=defaults.DELTA_DAYS):
            return True
        else:
            return False

    def send_verify_email(self):
        key = EmailVerifyTokenGenerator().make_token(self)
        url = settings.REG_VERIFY_URL.format(self.pk, key)
        return send_templated_email.delay(
            _('Подтвердите Ваш электронный адрес'),
            self.email,
            'accounts/verify_email.txt',
            'accounts/verify_email.html',
            url=url, email=self.username, site_name=settings.REG_SITE_NAME
        )

    def send_change_password_email(self):
        password = User.objects.make_random_password()
        self.set_password(password)
        self.save()
        return send_templated_email.delay(
            _('Сброс пароля'),
            self.email,
            'accounts/change_password.txt',
            'accounts/change_password.html',
            password=password, email=self.username, site_name=settings.REG_SITE_NAME
        )

    def delete_photo(self):
        if self.photo:
            self.photo.delete(save=True)

    class Meta(auth_models.AbstractUser.Meta):
        ordering = ('-created_at', 'pk')
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('пользователя')
        verbose_name_plural = _('Пользователи')
        indexes = (models.Index(fields=('username', 'phone', 'email',)),)

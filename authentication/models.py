from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework_jwt.settings import api_settings

from system.models import BaseModel, SoftDeleteModel


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(email=self.normalize_email(email), name=name,)

        user.set_password(password)
        user.save(using=self._db)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user

    def create_superuser(self, email, name, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(email=email, password=password, name=name,)

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel, SoftDeleteModel):
    email = models.EmailField(
        verbose_name=_('Email address'), max_length=255, unique=True,
    )
    name = models.CharField(verbose_name=_('name'), max_length=30)
    is_active = models.BooleanField(verbose_name=_('Is active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
    ]

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.name

    @property
    def is_staff(self):
        'Is the user a member of staff?'
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

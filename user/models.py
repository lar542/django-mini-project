from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager
from django.core.mail import send_mail
from conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('아이디', max_length=10, unique=True)
    password = models.CharField('비밀번호', max_length=10)
    email = models.EmailField('이메일', unique=True)
    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용여부', default=False)
    created_at = models.DateTimeField('가입일', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username' # 아이디를 사용자 식별자로 설정
    REQUIRED_FIELDS = ['email'] # 필수입력값

    def email_user(self, subject, message, html_message):
        return send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email],
            html_message=html_message)
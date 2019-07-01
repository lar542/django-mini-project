from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('아이디', max_length=10, unique=True)
    password = models.CharField('비밀번호', max_length=10)
    email = models.EmailField('이메일', unique=True)
    is_staff = models.BooleanField('스태프 권한', default=False)
    is_active = models.BooleanField('사용여부', default=True)
    created_at = models.DateTimeField('가입일', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username' # 아이디를 사용자 식별자로 설정
    REQUIRED_FIELDS = ['email'] # 필수입력값
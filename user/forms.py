from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . validators import RegisteredEmailValidator


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model() # 프로젝트 폴더의 settings.py의 AUTH_USER_MODEL이 참조하는 모델을 찾아주는 함수
        fields = ['email', 'username']
        # 정의된 모델에서 폼에 보여줄 필드를 정의, password는 UserCreationForm에서 자동 생성


class VerificationEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True}),
        validators=(forms.EmailField.default_validators + [RegisteredEmailValidator()])
    )
    # 이미 인증된 이메일이나 가입된 적이 있는 이메일인 경우 에러를 발생시키는 유효성 검증 필터 추가
    # 에러 메시지는 필드에 표시하기 위해 view가 아니라 필드에서 유효성을 검증하도록 함
    # 이 유효성 검증필터를 EmailField의 기본 필터에 추가하기 위해 RegisteredEmailValidator() 인스턴스를 추가함
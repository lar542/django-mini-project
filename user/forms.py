from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model() # 프로젝트 폴더의 settings.py의 AUTH_USER_MODEL이 참조하는 모델을 찾아주는 함수
        fields = ['email', 'username']
        # 정의된 모델에서 폼에 보여줄 필드를 정의, password는 UserCreationForm에서 자동 생성
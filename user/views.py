from django.views.generic import CreateView, FormView
from user.forms import UserRegisterForm, VerificationEmailForm
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.views.generic.base import TemplateView
from django.shortcuts import redirect, render


# 인증 이메일 발송
class VerifyEmailMixin:
    email_template_name = 'user/verify.html'
    token_generator = default_token_generator  # 사용자 데이터를 가지고 해시데이터를 만들어주는 객체

    def send_verification_email(self, user):
        token = self.token_generator.make_token(user) # 사용자 고유의 토큰을 생성
        url = self.build_verification_link(user, token)
        subject = '[가입 인증] 환영합니다!'
        message = '다음 주소로 이동하셔서 인증해주세요. {}'.format(url)
        html_message = render(self.request, self.email_template_name, {'url': url}).content.decode('utf-8')
        user.email_user(subject, message, html_message=html_message) # 이메일 발송
        messages.info(self.request, '환영합니다! 가입하신 이메일주소로 인증메일을 발송했으니 확인 후 인증해주세요!')

    def build_verification_link(self, user, token):
        return '{}/user/{}/verify/{}'.format(self.request.META.get('HTTP_ORIGIN'), user.pk, token)


# 회원가입
class UserRegister(VerifyEmailMixin, CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    template_name = 'user/join.html'
    success_url = '/user/login/'
    verify_url = '/user/verify/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if form.instance:
            self.send_verification_email(form.instance)
        return response


# 인증 이메일 재발송
class ResendVerifyEmail(VerifyEmailMixin, FormView):
    model = get_user_model()
    form_class = VerificationEmailForm
    template_name = 'user/resend_verify_email.html'
    success_url = '/user/login/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            messages.error(self.request, '알 수 없는 사용자 입니다.')
        else:
            self.send_verification_email(user)
        return super().form_valid(form)


# 인증페이지
class UserVerification(TemplateView):
    model = get_user_model()
    token_generator = default_token_generator

    def get(self, request, *args, **kwargs):
        if self.is_valid_token(kwargs=kwargs):
            messages.info(request, '인증이 완료되었습니다.')
        else:
            messages.error(request, '인증이 실패하였습니다.')
        return redirect('user:login')

    def is_valid_token(self, **kwargs):
        pk = kwargs.get('kwargs').get('pk')
        token = kwargs.get('kwargs').get('token')
        user = self.model.objects.get(pk=pk)
        is_valid = self.token_generator.check_token(user, token)
        if is_valid:
            user.is_active = True
            user.save()
        return is_valid


# 로그인
class UserLogin(LoginView):
    template_name = 'user/login.html'

    # 유효성 검증에 실패한 경우 form_invalid 메소드를 오버라이딩해서 에러 메시지를 출력
    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다.', extra_tags='danger')
        return super().form_invalid(form)
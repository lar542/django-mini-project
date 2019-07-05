from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('join/', views.UserRegister.as_view(), name="join"),
    path('login/', views.UserLogin.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('<pk>/verify/<token>', views.UserVerification.as_view(), name="verify"),
    path('resend_verify_email/', views.ResendVerifyEmail.as_view(), name="resend")
]
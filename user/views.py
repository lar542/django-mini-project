from django.shortcuts import render
from . models import User
from django.views import generic
from user.forms import UserRegisterForm
from django.contrib.auth import get_user_model


class UserRegister(generic.CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    template_name = 'user/join.html'
    success_url = '/board/'


#class UserLogin(generic.View):



#class UserLogout(generic.View):

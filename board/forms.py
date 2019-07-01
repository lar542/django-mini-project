from django.forms import ModelForm
from django import forms
from . models import Board, Comment
from django.utils.translation import gettext_lazy as _


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content', 'username']
        labels = {
            'title': _('제목'),
            'content': _('내용'),
        }
        help_text = {
            'title': _('제목을 입력해주세요.'),
            'content': _('내용을 입력해주세요.'),
        }
        error_message = {
            'title': {
                'max_length': _('제목은 200자 이하로 작성해주세요.')
            },
            'content': {
                'max_length': _('내용은 1000자 이하로 작성해주세요.')
            },
            'username': _('사용자 아이디는 필수 값 입니다.')
        }
        widgets = {
            'username': forms.HiddenInput()
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['board', 'content', 'username']
        labels = {
            'content': _('내용')
        }
        help_text = {
            'content': _('내용을 입력해주세요.')
        }
        widgets = {
            'board': forms.HiddenInput(),
            'username': forms.HiddenInput()
        }
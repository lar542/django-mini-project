from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('write/', views.WriteView.as_view(), name="write"),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('comment/write/', views.CommentWrite.as_view(), name="comment-write"),
]
from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('write/', views.WriteView.as_view(), name="write"),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:pk>/update', views.UpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name="delete"),

    path('comment/<int:board_id>/write', views.comment_write, name="comment-write"),
    path('comment/<int:board_id>/<int:comment_id>/delete', views.comment_delete, name="comment-delete"),
]
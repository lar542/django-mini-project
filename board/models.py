from django.db import models


class Board(models.Model):
    username = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BoardLikePoint(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    username = models.CharField(max_length=10)
    like_point = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    username = models.CharField(max_length=10)
    content = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentLikeCnt(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    username = models.CharField(max_length=10)
    like_cnt = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
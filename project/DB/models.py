from django.db import models
from django.contrib.auth.models import User

# Create your models here.

"""
사용자 정보는 Django 내장 인증 모델을 사용, admin 페이지에서 확인
class User(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
"""        

class Dictionary(models.Model):
    word = models.CharField(max_length=20)
    meaning = models.CharField(max_length=200)
    creationDate = models.DateField(auto_now_add=True)
    learned = models.BooleanField(default=False)
    userid = models.ForeignKey(User, verbose_name='custom word',on_delete=models.CASCADE)

    def __str__(self):
        return self.word
    
    class Meta:
        verbose_name = '사용자 사전'
        # db_table =  # 미지정시 기본 이름 : <앱>_<클래스> -> db_user (전체 소문자)
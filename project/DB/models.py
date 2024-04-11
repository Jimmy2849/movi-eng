from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Dictionary(models.Model):
    word = models.CharField(max_length=20)
    meaning = models.CharField(max_length=200)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.word
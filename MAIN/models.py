from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    abstract = models.CharField(max_length=300)
    content = models.TextField()
    userKey = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
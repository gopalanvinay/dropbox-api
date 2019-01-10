from django.db import models

class UserDetail(models.Model):
    user_name = models.CharField(max_length=60)
    user_email = models.CharField(max_length=60, default="user@example.com")
    access_token = models.CharField(max_length=200)
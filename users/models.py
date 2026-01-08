from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_project_manager = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'     
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.username
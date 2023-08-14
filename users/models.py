from django.contrib.auth.models import AbstractUser, Group,Permission
from django.db import models

class User(AbstractUser):

    USERNAME_FIELD = 'username'
    username = models.CharField(max_length=150, unique=True)
    is_teacher = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission,blank=True,related_name='custom_user_set')
    has_paid = models.BooleanField(default=False)

    has_resume = models.BooleanField(default=False)
    has_school = models.BooleanField(default=False)  

    created_at = models.DateTimeField(auto_now_add=True)
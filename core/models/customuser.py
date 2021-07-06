from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.EmailField(max_length=75)
    image = models.ImageField(upload_to="user/", default="user/avatar-default.png", blank=True) #Should  change to 'avatar' (upload_to="network/", default="network/sustainability-circle.png", blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name_prefix = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        # if (self.first_name and self.last_name):
        #     if self.last_name_prefix:
        #         return f"{self.first_name} {self.last_name_prefix} {self.last_name}"
        #     return f"{self.first_name} {self.last_name}"
        return self.username


''' 
- Should have Email as Login Field
'''
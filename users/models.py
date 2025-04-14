from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.





class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', null=True, blank=True)


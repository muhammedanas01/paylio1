from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
   

    def __str__(self):
        return self.username


# By defining the username field in this custom User model, you're essentially creating a custom field that overrides the default username field in Django's built-in User model.

# The purpose of this custom User model is to:

# 1. Use the email field as the username field for authentication purposes (by setting USERNAME_FIELD = 'email').
# 2. Include the username field as a required field when creating a new user (by setting REQUIRED_FIELDS = ['username']).
# 3. Add additional fields (is_staff and is_superuser) to the User model.

# By defining the username field in this custom User model, you're not relying on the default username field provided by Django's built-in User model. Instead, you're creating a custom field that you can use for your specific use case.

# So, in summary, the purpose of this code is to define a custom User model that overrides the default username field and adds additional fields, while still using the email field as the username field for authentication purposes.
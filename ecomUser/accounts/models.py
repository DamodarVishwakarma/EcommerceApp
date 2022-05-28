from re import U
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def _create_user(self, first_name, last_name, username, email, password,is_admin, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have email address')
        if not username:
            raise ValueError('User must have username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            is_staff=is_staff,
            is_active=True,
            is_admin=True,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    
    def create_user(self, first_name, last_name,  username, email, password, **extra_fields):
        return self._create_user(first_name, last_name,  username,email, password, False, False,False, **extra_fields)

    def create_superuser(self, first_name, last_name,  username, email, password, **extra_fields):
        user = self._create_user(first_name, last_name,  username,email, password, True, True,True, **extra_fields)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #required 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_lable):
        return True
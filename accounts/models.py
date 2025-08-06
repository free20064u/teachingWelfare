from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
class Region(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

class MaritalStatus(models.Model):
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=30, blank=True)
    short_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    serial_number = models.CharField(max_length=30, blank=True, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    home_town = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    marital_status = models.CharField(max_length=30, blank=True)
    house_number = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

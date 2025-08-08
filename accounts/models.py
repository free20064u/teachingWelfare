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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    CATEGORY = [
        (None,'Select Category'),
        ('chairperson','chairperson'),
        ('secretary','secretary'),
        ('finance','finance'),
        ('tresurer','tresurer'),
        ('member','member'),
    ]

    GENDER = [
        (None,'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female')
    ]

    MARITAL_STATUS = [
        (None, 'Marital Status'),
        ('M','Married'),
        ('S','Single'),
        ('D','Divorced')
    ]

    REGION = [
        (None, 'Select Region'),
        ('GA', 'Greater Accra'),
        ('AR', 'Ashante Region'),
        ('CR','Central Region'),
        ('WR','Western Region'),
        ('WN', 'Western North'),
        ('ER','Eastern Region'),
        ('VR','Volta Region'),
        ('BA', 'Ahafo Region'),
        ('BE', 'Bono East'),
        ('BR', 'Bono Region'),
        ('NR', 'Northern Region'),
        ('NE', 'North East'),
        ('SR', 'Savannah Region'),
        ('UE', 'Upper East'),
        ('UW', 'Upper West'),
        ('OR', 'Oti Region'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    home_town = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=2,choices=REGION, blank=True)
    gender = models.CharField(max_length=1,choices=GENDER, blank=True)
    marital_status = models.CharField(max_length=1,choices=MARITAL_STATUS, blank=True)
    house_number = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=15,choices=CATEGORY, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    house_number = models.CharField(max_length=30, blank=True)
    region = models.CharField(max_length=2,choices=REGION, blank=True)
    gender = models.CharField(max_length=1,choices=GENDER, blank=True)
    marital_status = models.CharField(max_length=1,choices=MARITAL_STATUS, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=15,choices=CATEGORY, blank=True)
    staff_id = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def save(self, *args, **kwargs):
        # We need to save the instance first to get a primary key (pk)
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # If it's a new instance and staff_id is not already set
        if is_new and not self.staff_id:
            # Format: TWA-{last_two_of_pk}-{last_two_of_join_year}
            # e.g., TWA-07-24 for pk=7, joined in 2024
            # e.g., TWA-23-24 for pk=123, joined in 2024
            last_two_pk = str(self.pk)[-2:].zfill(2)
            last_two_year = self.date_joined.strftime('%y')
            self.staff_id = f"TWA-{last_two_pk}-{last_two_year}"

            # Use .objects.filter().update() to save just this field and
            # avoid calling the save() method again, which would cause an infinite loop.
            CustomUser.objects.filter(pk=self.pk).update(staff_id=self.staff_id)

    def __str__(self):
        return self.email

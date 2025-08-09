from django.db import models

from accounts.models import CustomUser

# Create your models here.


class Benefit(models.Model):
    BENEFITS = {
        (None,'Select Benefit'),
        ('Marriage','Marriage'),
        ('Birth','Birth'),
        ('Funeral','Funeral'),
        ('Accident', 'Accident'),
        ('Ill-health', 'Ill-health'),
    }

    benefit_type = models.CharField(max_length=30,choices=BENEFITS, blank=True, null=True)
    detail = models.CharField(max_length=150, blank=True, null=True)
    supporting_document = models.FileField(upload_to='supporting_documents')
    member = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, default="Pending")
    reason = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return (self.member, self.benefit_type)


class Spouse(models.Model):
    first_name = models.CharField(max_length=30, blank=True)    
    middle_name = models.CharField(max_length=30, blank=True)    
    last_name = models.CharField(max_length=30, blank=True)
    house_number = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return (self.first_name, self.middle_name, self.last_name)


class Children(models.Model):
    first_name = models.CharField(max_length=30, blank=True)    
    middle_name = models.CharField(max_length=30, blank=True)    
    last_name = models.CharField(max_length=30, blank=True)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return (self.first_name, self.middle_name, self.last_name)


class NextOfKin(models.Model):
    first_name = models.CharField(max_length=30, blank=True)    
    middle_name = models.CharField(max_length=30, blank=True)    
    last_name = models.CharField(max_length=30, blank=True)
    house_number = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return (self.first_name, self.middle_name, self.last_name)
    

class Parent(models.Model):
    fathers_first_name = models.CharField(max_length=30, blank=True)    
    fathers_middle_name = models.CharField(max_length=30, blank=True)    
    fathers_last_name = models.CharField(max_length=30, blank=True)
    mothers_first_name = models.CharField(max_length=30, blank=True)    
    mothers_middle_name = models.CharField(max_length=30, blank=True)    
    mothers_last_name = models.CharField(max_length=30, blank=True)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    
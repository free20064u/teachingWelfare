from django.db import models

# Create your models here.
class BenefitType(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    
    def __str__(self):
        return(self.name)
    

class Benefit(models.Model):
    benefit_type = models.CharField(max_length=30, blank=True, null=True)
    detail = models.CharField(max_length=150, blank=True, null=True)
    supporting_document = models.FileField(upload_to='supporting_documents')
    member = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, default="Pending")
    reason = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return (self.member, self.benefit_type)

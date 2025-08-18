from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone

from accounts.models import CustomUser

# Create your models here.


class Benefit(models.Model):
    """
    Represents a benefit claim made by a member.
    """
    BENEFIT_CHOICES = (
        (None, 'Select a Benefit Type'),
        ('Marriage', 'Marriage'),
        ('Birth', 'Birth'),
        ('Funeral', 'Funeral'),
        ('Accident', 'Accident'),
        ('Ill-health', 'Ill-health'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    )

    # Define standard amounts for each benefit type
    BENEFIT_AMOUNTS = {
        'Marriage': Decimal('500.00'),
        'Birth': Decimal('300.00'),
        'Funeral': Decimal('1000.00'),
        'Accident': Decimal('700.00'),
        'Ill-health': Decimal('700.00'),
    }

    benefit_type = models.CharField(max_length=30, choices=BENEFIT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="The amount to be paid for this benefit.")
    detail = models.TextField()
    supporting_document = models.FileField(upload_to='supporting_documents', blank=True, null=True)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='benefits')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_submitted = models.DateTimeField(default=timezone.now)
    honoured = models.BooleanField(default=False)
    
    # Fields to track who processed the request and when
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_benefits'
    )
    processed_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"

    

    def __str__(self):
        """
        Returns a string representation of the benefit claim.
        """
        # Assumes CustomUser has a method to get the full name.
        # get_benefit_type_display() returns the human-readable value of the choice.
        return f"{self.member} - {self.get_benefit_type_display()}"


class Spouse(models.Model):
    """
    Represents the spouse of a member.
    A member can have only one spouse record.
    """
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    house_number = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    # A OneToOneField ensures that each member can have only one spouse.
    member = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='spouse')

    class Meta:
        verbose_name = "Spouse"
        verbose_name_plural = "Spouses"

    def __str__(self):
        """
        Returns the full name of the spouse.
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip().replace('  ', ' ')


class Children(models.Model):
    """
    Represents a child of a member.
    A member can have multiple children.
    """
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='children')

    class Meta:
        # Correctly pluralizes to "children" in the admin.
        verbose_name = "Child"
        verbose_name_plural = "Children"

    def __str__(self):
        """
        Returns the full name of the child.
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip().replace('  ', ' ')


class NextOfKin(models.Model):
    """
    Represents the next of kin for a member.
    A member can have only one next of kin record.
    """
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    house_number = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    # A OneToOneField ensures that each member can have only one next of kin.
    member = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='next_of_kin')

    class Meta:
        verbose_name = "Next of Kin"
        verbose_name_plural = "Next of Kin"

    def __str__(self):
        """
        Returns the full name of the next of kin.
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip().replace('  ', ' ')


class Parent(models.Model):
    """
    Represents the parents of a member.
    A member can have only one parent record.
    """
    fathers_first_name = models.CharField("Father's First Name", max_length=30, blank=True)
    fathers_middle_name = models.CharField("Father's Middle Name", max_length=30, blank=True)
    fathers_last_name = models.CharField("Father's Last Name", max_length=30, blank=True)
    mothers_first_name = models.CharField("Mother's First Name", max_length=30, blank=True)
    mothers_middle_name = models.CharField("Mother's Middle Name", max_length=30, blank=True)
    mothers_last_name = models.CharField("Mother's Last Name", max_length=30, blank=True)
    # A OneToOneField is appropriate here as a member has one set of parents.
    member = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parent')

    class Meta:
        verbose_name = "Parent"
        verbose_name_plural = "Parents"

    def __str__(self):
        """
        Returns a string representation for the member's parents.
        """
        return f"Parents of {self.member}"
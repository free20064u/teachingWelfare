import uuid
from django.db import models
from django.conf import settings


class Dues(models.Model):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dues'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    receipt_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Format: RCPT-YYYYMMDD-8CHAR_UUID
            date_str = self.payment_date.strftime('%Y%m%d')
            unique_id = str(uuid.uuid4()).split('-')[0].upper()
            self.receipt_number = f"RCPT-{date_str}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dues from {self.member.get_full_name()} on {self.payment_date}"

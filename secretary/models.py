from django.db import models
from django.conf import settings

# Create your models here.
class Announcement(models.Model):
    """
    Represents an announcement made by a secretary.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_announcements', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

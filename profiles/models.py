from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    read_key = models.CharField(max_length=255)
    write_key = models.CharField(max_length=255)

    def __str__(self):
        return f"UserProfile {self.user.username}"

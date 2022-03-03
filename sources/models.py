from django.db import models

class Source(models.Model):
    hostname = models.CharField(max_length=255)
    owner = models.OneToOneField(
        'users.User',
        primary_key=True,
        on_delete=models.CASCADE
    )
    REQUIRED_FILEDS = []
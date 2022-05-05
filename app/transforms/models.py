from django.db import models

class Transform(models.Model):
    owner = models.ForeignKey(
        'users.User',
        on_delete = models.CASCADE
    )
    uuid = models.CharField(max_length=255)
    REQUIRED_FILEDS = []
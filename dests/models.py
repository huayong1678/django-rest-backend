from django.db import models
from users.models import User

class Dest(models.Model):

    host = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    port = models.IntegerField()
    password = models.CharField(max_length=255)
    # hash_pwd = models.BinaryField()
    # hash_key = models.BinaryField()
    owner = models.ForeignKey(
        'users.User',
        on_delete = models.CASCADE
    )
    REQUIRED_FILEDS = []
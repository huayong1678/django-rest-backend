from django.db import models
from users.models import User
from sources.models import Source
from dests.models import Dest

class DatabaseSchema(models.Model):
    tag = models.CharField(max_length=255)
    dest = models.ForeignKey(
            'dests.Dest',
            on_delete = models.CASCADE
        )
    source = models.ForeignKey(
            'sources.Source',
            on_delete = models.CASCADE
        )
    owner = models.ForeignKey(
            'users.User',
            on_delete = models.CASCADE
        )
    REQUIRED_FIELD=[]
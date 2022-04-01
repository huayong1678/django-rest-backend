from django.db import models
from users.models import User

class Source(models.Model):
    host = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    database = models.CharField(max_length=255)
    tablename = models.CharField(max_length=255)

    POSTGRES = "PG"
    MYSQL = "MY"
    engine_choices = [
        (POSTGRES, "Postgres"),
        (MYSQL, "MySQL")
    ]
    engine = models.CharField(max_length=2, choices=engine_choices)

    port = models.IntegerField()
    password = models.CharField(max_length=255)
    owner = models.ForeignKey(
        'users.User',
        on_delete = models.CASCADE
    )
    REQUIRED_FILEDS = []
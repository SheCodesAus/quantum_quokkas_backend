from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    organisation = models.ForeignKey(
        'workshops.organisation',
        on_delete=models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'members'
    )

    def __str__(self):
        return self.username

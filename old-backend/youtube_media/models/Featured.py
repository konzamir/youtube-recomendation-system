from django.db import models
from django.contrib.auth.models import User
from .Links import Links


class Featured(models.Model):
    
    link = models.ForeignKey(
        to=Links, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f'{self.user.id} -> {self.link.title}'

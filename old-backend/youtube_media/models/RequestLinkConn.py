from django.db import models
from .Links import Links
from .RequestData import RequestData


class RequestLinkConn(models.Model):
    link = models.ForeignKey(
        to=Links, on_delete=models.CASCADE
    )
    request_data = models.ForeignKey(
        to=RequestData, on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f'{self.link.title} -> {self.request_data.data}'

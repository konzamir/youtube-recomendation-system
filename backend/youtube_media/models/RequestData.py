from django.db import models


class RequestData(models.Model):

    click_count = models.IntegerField(db_index=True, default=0)
    data = models.CharField(max_length=512)
    hash_data = models.CharField(max_length=64, db_index=True)
    full_url = models.CharField(max_length=512)
    region = models.CharField(max_length=16)
    etag = models.CharField(max_length=256)
    next_page = models.CharField(max_length=64, blank=True, null=True,)
    prev_page = models.CharField(max_length=64, blank=True, null=True)
    curr_page = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    updated_at = models.DateTimeField(db_index=True, auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    
    def __str__(self):
        return f'{self.data}'

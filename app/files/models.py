from django.db import models

class FileMetadata(models.Model):
    storage_key = models.CharField(max_length=255, unique=True)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    checksum = models.CharField(max_length=64)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

from django.db import models

# Create your models here.
class ChromaData(models.Model):
    text = models.TextField()
    embedding = models.JSONField()
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.text[:50]
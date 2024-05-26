from django.db import models


class History (models.Model):
    datetime = models.DateTimeField('date published')
    query = models.TextField()
    sim1 = models.FloatField()
    sim2 = models.FloatField()
    sim3 = models.FloatField()
    answer = models.TextField()

class ChromaData(models.Model):
    text = models.TextField()
    embedding = models.JSONField()
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.text[:50]
    

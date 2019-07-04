from django.db import models

# Create your models here.
class Movies(models.Model):
    prime_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    casts = models.TextField()
    rating = models.FloatField()
    
    objects = models.Manager()

    def __str__(self):
        return self.name
    

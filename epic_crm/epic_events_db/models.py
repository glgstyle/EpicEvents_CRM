from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=25)
    description = models.fields.CharField(max_length=255, blank=True)
    TYPE_CHOICES = (
        # first is displayed and second in database
        ('Sales', 'sales'),
        ('Support', 'support'),
        ('Management', 'management'),
    )
from django.db import models

# Create your models here.
class Task (models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')


    def __str__(self):
        return self.title
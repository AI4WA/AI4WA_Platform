from django.db import models

# Create your models here.


class Crime(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the crime")
    description = models.TextField()
    count = models.IntegerField(default=-1, blank=True, null=True, help_text="Number of crimes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
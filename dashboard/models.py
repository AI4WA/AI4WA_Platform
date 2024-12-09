from django.db import models


# Create your models here.
class PatientTracking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True, help_text="Description of the patient")
    count = models.IntegerField(default=0, help_text="Number of times the patient currently in the waiting room")

    def __str__(self):
        return f"PatientTracking: {self.id}, {self.count}, {self.description}"


class ImageData(models.Model):
    patient_tracking = models.ForeignKey(PatientTracking, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return f"ImageData: {self.id}, {self.image}"
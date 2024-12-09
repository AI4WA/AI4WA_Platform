from django.contrib import admin
from dashboard.models import PatientTracking, ImageData


# Register your models here.


@admin.register(PatientTracking)
class PatientTrackingaDmin(admin.ModelAdmin):
    pass


@admin.register(ImageData)
class ImageDataAdmin(admin.ModelAdmin):
    pass

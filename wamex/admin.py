from django.contrib import admin
from wamex.models import SpatialMetaData, Chat


# Register your models here.

@admin.register(SpatialMetaData)
class SpatialMetaDataAdmin(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass

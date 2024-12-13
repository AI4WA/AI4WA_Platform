from django.contrib.gis.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.
class SpatialMetaData(models.Model):
    file_name = models.CharField(max_length=255, help_text="Name of the file")
    metadata_json = models.JSONField(
        help_text="Metadata in JSON format",
        blank=True,
        null=True,
        default=dict
    )

    geometry = models.GeometryField(
        help_text="Geometry of the spatial data",
        blank=True,
        null=True,
        srid=4326
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Chat(models.Model):
    """
    Chat model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        db_index=True,
        db_column="chat_uuid",
        default=uuid.uuid4,
    )
    messages = models.JSONField(null=True, blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

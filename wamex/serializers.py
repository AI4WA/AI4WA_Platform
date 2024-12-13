from rest_framework import serializers
from wamex.models import SpatialMetaData


# create a serializer class for the model
class SpatialMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpatialMetaData
        fields = "__all__"

from rest_framework import serializers
from crime.models import Crime


class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = ['id', 'name', 'description', 'count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

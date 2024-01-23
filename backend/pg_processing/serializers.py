"""Responsible for serializers."""
from rest_framework.serializers import ModelSerializer
from .models import MainData


class MainDataSerializer(ModelSerializer):
    """Serialize data of MainData model."""

    class Meta:
        model = MainData
        fields = '__all__'



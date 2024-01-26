"""Responsible for serializers."""
from rest_framework import serializers
from .models import MainData


class MainDataSerializer(serializers.ModelSerializer):
    """Serialize data of MainData model."""

    class Meta:
        model = MainData
        fields = '__all__'


class KISDataSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    dept = serializers.CharField(required=False)
    channel = serializers.CharField(required=False)
    patient_type = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        clean_dict = {key: value for key, value in data.items() if value is not None}
        return clean_dict


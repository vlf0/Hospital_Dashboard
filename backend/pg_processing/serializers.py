"""Responsible for serializers."""
from rest_framework import serializers
from .models import MainData


class MainDataSerializer(serializers.ModelSerializer):
    """Serialize data of MainData model."""

    class Meta:
        model = MainData
        fields = '__all__'


class KISDataSerializer(serializers.Serializer):

    dept = serializers.CharField(required=False)
    channel = serializers.CharField(required=False)
    patient_type = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    pat_fio = serializers.CharField(required=False)
    ib_num = serializers.CharField(required=False)
    sex = serializers.CharField(required=False)
    ages = serializers.CharField(required=False)
    arriving_dt = serializers.DateTimeField(required=False)
    state = serializers.CharField(required=False)
    days = serializers.IntegerField(required=False)
    diag_arr = serializers.CharField(required=False)
    diag_dead = serializers.CharField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        clean_dict = {key: value for key, value in data.items() if value is not None}
        return clean_dict


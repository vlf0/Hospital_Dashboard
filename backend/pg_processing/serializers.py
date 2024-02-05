"""Responsible for serializers."""
from rest_framework import serializers
from .models import MainData



class MainDataSerializer(serializers.ModelSerializer):
    """Serialize data of MainData model."""

    class Meta:
        model = MainData
        fields = ['dates', 'arrived', 'hosp', 'refused', 'signout', 'deads', 'reanimation']


class KISDataSerializer(serializers.Serializer):

    ch103 = serializers.IntegerField(required=False, allow_null=True)
    clinic_only = serializers.IntegerField(required=False, allow_null=True)
    ch103_clinic = serializers.IntegerField(required=False, allow_null=True)
    singly = serializers.IntegerField(required=False, allow_null=True)
    ZL = serializers.CharField(required=False, allow_null=True)
    foreign = serializers.CharField(required=False, allow_null=True)
    moscow = serializers.CharField(required=False, allow_null=True)
    undefined = serializers.CharField(required=False, allow_null=True)
    dept = serializers.CharField(required=False, allow_null=True)
    amount = serializers.CharField(required=False, allow_null=True)

    therapy = serializers.CharField(required=False, allow_null=True)
    surgery = serializers.CharField(required=False, allow_null=True)
    cardiology = serializers.CharField(required=False, allow_null=True)
    urology = serializers.CharField(required=False, allow_null=True)
    neurology = serializers.CharField(required=False, allow_null=True)

    error = serializers.CharField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove all dict pairs with None values
        clean_dict = {key: value for key, value in data.items() if value is not None}
        return clean_dict

"""Responsible for serializers."""
from rest_framework import serializers
from .models import MainData


class MainDataSerializer(serializers.ModelSerializer):
    """Serialize data of MainData model."""

    class Meta:
        model = MainData
        fields = ['dates', 'arrived', 'hosp', 'refused', 'signout', 'deads', 'reanimation']


class KISDataSerializer(serializers.Serializer):
    """
    Serializer for non-model data getting from external DB.

    It contains all the required fields for all datasets
    since it serializes multiple separate datasets from the same DB.
    """
    # Fields of arrived patients.
    ch103 = serializers.IntegerField(required=False, allow_null=True)
    clinic_only = serializers.IntegerField(required=False, allow_null=True)
    ch103_clinic = serializers.IntegerField(required=False, allow_null=True)
    singly = serializers.IntegerField(required=False, allow_null=True)
    ZL = serializers.IntegerField(required=False, allow_null=True)
    foreign = serializers.IntegerField(required=False, allow_null=True)
    moscow = serializers.IntegerField(required=False, allow_null=True)
    undefined = serializers.IntegerField(required=False, allow_null=True)
    # Fields of hospitalized patients that counted by depts.
    therapy = serializers.IntegerField(required=False, allow_null=True)
    surgery = serializers.IntegerField(required=False, allow_null=True)
    cardiology = serializers.IntegerField(required=False, allow_null=True)
    urology = serializers.IntegerField(required=False, allow_null=True)
    neurology = serializers.IntegerField(required=False, allow_null=True)
    # Fields of deads and signout patients.
    deads = serializers.IntegerField(required=False, allow_null=True)
    moved = serializers.IntegerField(required=False, allow_null=True)
    signout = serializers.IntegerField(required=False, allow_null=True)
    cardio_d = serializers.IntegerField(required=False, allow_null=True)
    surgery_d = serializers.IntegerField(required=False, allow_null=True)
    therapy_d = serializers.IntegerField(required=False, allow_null=True)

    def to_representation(self, instance):
        """
        Remove all dict pairs with None values for exclude fields with no real values.

        :param instance:
        :return:
        """
        data = super().to_representation(instance)
        # Remove all dict pairs with None values
        clean_dict = {key: value for key, value in data.items() if value is not None}
        return clean_dict

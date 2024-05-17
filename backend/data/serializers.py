"""Responsible for serializers."""
from rest_framework import serializers
from .models import MainData, AccumulationOfIncoming, Profiles


class MainDataSerializer(serializers.ModelSerializer):
    """Serialize data of MainData model."""

    class Meta:
        model = MainData
        fields = ['dates', 'arrived', 'hosp', 'refused', 'signout', 'deads', 'reanimation']


class ProfilesSerializer(serializers.ModelSerializer):

    current_date = serializers.DateField(source='accumulationofincoming__dates', read_only=True)
    fact = serializers.IntegerField(source='accumulationofincoming__number', read_only=True)
    plan = serializers.IntegerField(source='plannumbers__plan', read_only=True)
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profiles
        fields = ['name', 'active', 'current_date', 'fact', 'plan', 'total']


class AccumulativeDataSerializerSave(serializers.ModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(source='profile', queryset=Profiles.objects.all())

    class Meta:
        model = AccumulationOfIncoming
        fields = ['id', 'dates', 'number', 'profile_id']


class KISDataSerializer(serializers.Serializer):
    """
    Serializer for non-model data getting from external DB.

    It contains all the required fields for all datasets
    since it serializes multiple separate datasets from the same DB.
    """
    # Fields of arrived patients.
    ch103 = serializers.IntegerField(read_only=True)
    clinic_only = serializers.IntegerField(read_only=True)
    ch103_clinic = serializers.IntegerField(read_only=True)
    singly = serializers.IntegerField(read_only=True)
    plan = serializers.IntegerField(read_only=True)

    ZL = serializers.IntegerField(read_only=True)
    foreign = serializers.IntegerField(read_only=True)
    nil = serializers.IntegerField(read_only=True)
    nr = serializers.IntegerField(read_only=True)
    dms = serializers.IntegerField(read_only=True)
    undefined = serializers.IntegerField(read_only=True)
    # Fields of deads and signout patients.
    deads = serializers.IntegerField(read_only=True)
    moved = serializers.IntegerField(read_only=True)
    signout = serializers.IntegerField(read_only=True)

    oaronmk_d = serializers.IntegerField(read_only=True)
    surgery_d = serializers.IntegerField(read_only=True)
    oar1_d = serializers.IntegerField(read_only=True)
    dp_d = serializers.IntegerField(read_only=True)
    oar_d = serializers.IntegerField(read_only=True)
    trauma_d = serializers.IntegerField(read_only=True)
    neurosurgery_d = serializers.IntegerField(read_only=True)
    oaroim_d = serializers.IntegerField(read_only=True)
    oar2_d = serializers.IntegerField(read_only=True)
    cardio_d = serializers.IntegerField(read_only=True)
    therapy_d = serializers.IntegerField(read_only=True)
    endo_d = serializers.IntegerField(read_only=True)
    neuroonmk_d = serializers.IntegerField(read_only=True)
    urology_d = serializers.IntegerField(read_only=True)
    pursurgery_d = serializers.IntegerField(read_only=True)
    cardio2_d = serializers.IntegerField(read_only=True)
    skp_d = serializers.IntegerField(read_only=True)
    gynecology_d = serializers.IntegerField(read_only=True)
    emer_d = serializers.IntegerField(read_only=True)
    multi_pay_d = serializers.IntegerField(read_only=True)
    apc_d = serializers.IntegerField(read_only=True)
    combine_d = serializers.IntegerField(read_only=True)
    pulmonology_d = serializers.IntegerField(read_only=True)

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


class KISTableSerializer(KISDataSerializer):
    """
    Serializer for non-model table-data getting from external DB.

    It contains all the required fields for all table datasets
    since it serializes multiple separate table datasets from the same DB.
    """
    # Fields to deads dataset related
    pat_fio = serializers.CharField(read_only=True)
    ib_num = serializers.CharField(read_only=True)
    sex = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    arriving_dt = serializers.DateTimeField(read_only=True)
    state = serializers.CharField(read_only=True)
    dept = serializers.CharField(read_only=True)
    days = serializers.IntegerField(read_only=True)
    diag_arr = serializers.CharField(read_only=True)
    diag_dead = serializers.CharField(read_only=True)
    # Fields to hospitalized in reanimation dataset related
    doc_fio = serializers.CharField(read_only=True)
    diag_start = serializers.CharField(read_only=True)
    # Fields to moved to reanimation dataset related
    move_date = serializers.DateTimeField(read_only=True)
    from_dept = serializers.CharField(read_only=True)


class EmergencyDataSerializer(KISTableSerializer):

    refuses_amount = serializers.IntegerField(read_only=True)


class EmergencyDetailDataSerializer(EmergencyDataSerializer, KISTableSerializer):

    diag = serializers.CharField(read_only=True)
    refuse_reason = serializers.CharField(read_only=True)
    refuse_date = serializers.DateTimeField(read_only=True)
    waiting_time = serializers.TimeField(read_only=True)


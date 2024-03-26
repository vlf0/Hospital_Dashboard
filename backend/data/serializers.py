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
        fields = ['id', 'name', 'active', 'current_date', 'fact', 'plan', 'total']


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
    ch103 = serializers.IntegerField(required=False, allow_null=True)
    clinic_only = serializers.IntegerField(required=False, allow_null=True)
    ch103_clinic = serializers.IntegerField(required=False, allow_null=True)
    singly = serializers.IntegerField(required=False, allow_null=True)
    plan = serializers.IntegerField(required=False, allow_null=True)

    ZL = serializers.IntegerField(required=False, allow_null=True)
    foreign = serializers.IntegerField(required=False, allow_null=True)
    nil = serializers.IntegerField(required=False, allow_null=True)
    nr = serializers.IntegerField(required=False, allow_null=True)
    dms = serializers.IntegerField(required=False, allow_null=True)
    undefined = serializers.IntegerField(required=False, allow_null=True)
    
    # Fields of hospitalized patients that counted by depts.
    oar_p =serializers.IntegerField(required=False, allow_null=True)
    surgery_p =serializers.IntegerField(required=False, allow_null=True)
    therapy_p =serializers.IntegerField(required=False, allow_null=True)
    emer1_p =serializers.IntegerField(required=False, allow_null=True)
    gynekology_p =serializers.IntegerField(required=False, allow_null=True)
    xray_p =serializers.IntegerField(required=False, allow_null=True)
    emer2_p =serializers.IntegerField(required=False, allow_null=True)
    transfusiology_p =serializers.IntegerField(required=False, allow_null=True)
    gpractice_p =serializers.IntegerField(required=False, allow_null=True)
    narkology_p =serializers.IntegerField(required=False, allow_null=True)
    urology_p =serializers.IntegerField(required=False, allow_null=True)
    lab_p =serializers.IntegerField(required=False, allow_null=True)
    rean_p =serializers.IntegerField(required=False, allow_null=True)
    truma_p =serializers.IntegerField(required=False, allow_null=True)
    neuro_p =serializers.IntegerField(required=False, allow_null=True)
    ultrasound_p =serializers.IntegerField(required=False, allow_null=True)
    func_p =serializers.IntegerField(required=False, allow_null=True)
    cardio_p =serializers.IntegerField(required=False, allow_null=True)
    endo_p =serializers.IntegerField(required=False, allow_null=True)
    neurology_p =serializers.IntegerField(required=False, allow_null=True)
    static_p =serializers.IntegerField(required=False, allow_null=True)
    epid_p =serializers.IntegerField(required=False, allow_null=True)
    neon_p =serializers.IntegerField(required=False, allow_null=True)
    gyst_p =serializers.IntegerField(required=False, allow_null=True)
    endocop_p =serializers.IntegerField(required=False, allow_null=True)
    pulmo_p =serializers.IntegerField(required=False, allow_null=True)
    # Fields of deads and signout patients.
    deads = serializers.IntegerField(required=False, allow_null=True)
    moved = serializers.IntegerField(required=False, allow_null=True)
    signout = serializers.IntegerField(required=False, allow_null=True)

    oaronmk_d = serializers.IntegerField(required=False, allow_null=True)
    surgery_d = serializers.IntegerField(required=False, allow_null=True)
    oar1_d = serializers.IntegerField(required=False, allow_null=True)
    dp_d = serializers.IntegerField(required=False, allow_null=True)
    oar_d = serializers.IntegerField(required=False, allow_null=True)
    trauma_d = serializers.IntegerField(required=False, allow_null=True)
    neurosurgery_d = serializers.IntegerField(required=False, allow_null=True)
    oaroim_d = serializers.IntegerField(required=False, allow_null=True)
    oar2_d = serializers.IntegerField(required=False, allow_null=True)
    cardio_d = serializers.IntegerField(required=False, allow_null=True)
    therapy_d = serializers.IntegerField(required=False, allow_null=True)
    endo_d = serializers.IntegerField(required=False, allow_null=True)
    neuroonmk_d = serializers.IntegerField(required=False, allow_null=True)
    urology_d = serializers.IntegerField(required=False, allow_null=True)
    pursurgery_d = serializers.IntegerField(required=False, allow_null=True)
    cardio2_d = serializers.IntegerField(required=False, allow_null=True)
    skp_d = serializers.IntegerField(required=False, allow_null=True)
    gynecology_d = serializers.IntegerField(required=False, allow_null=True)
    emer_d = serializers.IntegerField(required=False, allow_null=True)
    multi_pay_d = serializers.IntegerField(required=False, allow_null=True)
    apc_d = serializers.IntegerField(required=False, allow_null=True)
    combine_d = serializers.IntegerField(required=False, allow_null=True)
    pulmonology_d = serializers.IntegerField(required=False, allow_null=True)

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
    pat_fio = serializers.CharField(required=False, allow_null=True)
    ib_num = serializers.CharField(required=False, allow_null=True)
    sex = serializers.CharField(required=False, allow_null=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    arriving_dt = serializers.DateTimeField(required=False, allow_null=True)
    state = serializers.CharField(required=False, allow_null=True)
    dept = serializers.CharField(required=False, allow_null=True)
    days = serializers.IntegerField(required=False, allow_null=True)
    diag_arr = serializers.CharField(required=False, allow_null=True)
    diag_dead = serializers.CharField(required=False, allow_null=True)
    # Fields to hospitalized in reanimation dataset related
    # ages = serializers.IntegerField(required=False, allow_null=True)
    doc_fio = serializers.CharField(required=False, allow_null=True)
    diag_start = serializers.CharField(required=False, allow_null=True)
    # Fields to moved to reanimation dataset related
    move_date = serializers.DateTimeField(required=False, allow_null=True)
    from_dept = serializers.CharField(required=False, allow_null=True)
    # Fields to deads from reanimation dataset related





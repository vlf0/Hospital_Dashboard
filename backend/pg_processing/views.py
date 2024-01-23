"""This module provide work of main django functions - views."""
from rest_framework.viewsets import ModelViewSet
from .models import MainData
from .serializers import MainDataSerializer


class MainDataViewSet(ModelViewSet):
    """Allow access to read main data from DMK DB by using GET method only defined explicitly."""

    queryset = MainData.objects.all()
    serializer_class = MainDataSerializer
    http_method_names = ['get']



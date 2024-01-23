"""This module provide work of main django functions - views."""
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import MainData
from .serializers import MainDataSerializer
from datetime import date


class MainDataReadViewSet(ReadOnlyModelViewSet):
    """Allow access to read main data from DMK DB by using GET method only."""

    queryset = MainData.objects.all()
    serializer_class = MainDataSerializer




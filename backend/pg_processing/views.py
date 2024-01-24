"""This module provide work of main django functions - views."""
from django.db.models.query import QuerySet
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import MainData
from .serializers import MainDataSerializer


class MainDataReadViewSet(ReadOnlyModelViewSet):
    """Allow access to read main data from DMK DB by using GET method only."""

    queryset = MainData.objects.custom_filter()
    serializer_class = MainDataSerializer






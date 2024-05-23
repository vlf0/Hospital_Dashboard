"""This file is responsible for router objects working."""
from rest_framework import routers
from .views import KISDataReadViewSet, KISDataAnotherDates, EmergencyDataViewSet


router = routers.DefaultRouter()
router.register(r'main_data', KISDataReadViewSet, basename='both_dbses')
router.register(r'details', KISDataAnotherDates, basename='kis')
router.register(r'emergency', EmergencyDataViewSet, basename='emergency_all')



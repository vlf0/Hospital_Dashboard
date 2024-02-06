"""This file is responsible for router objects working."""
from rest_framework import routers
from .views import KISDataReadViewSet


router = routers.DefaultRouter()
router.register(r'main_data', KISDataReadViewSet, basename='both_dbses')


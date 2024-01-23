"""This file is responsible for router objects working."""
from rest_framework import routers
from .views import MainDataReadViewSet

router = routers.SimpleRouter()
router.register(r'main_data', MainDataReadViewSet)


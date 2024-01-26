"""This file is responsible for router objects working."""
from rest_framework import routers
from .views import MainDataReadViewSet, KISDataReadViewSet


class CustomReadOnlyRouter(routers.SimpleRouter):
    """
    A router for read-only APIs, which uses trailing slashes.
    """
    routes = [
        routers.Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
    ]


router = CustomReadOnlyRouter()
# router.register(r'main_data', MainDataReadViewSet)
router.register(r'main_data', KISDataReadViewSet, basename='KIS')
print(router.urls)


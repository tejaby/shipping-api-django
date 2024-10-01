from rest_framework.routers import DefaultRouter

from .api import LocationViewSet

router = DefaultRouter()


router.register('locations', LocationViewSet)

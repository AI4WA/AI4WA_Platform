from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wamex.views import SpatialMetaDataViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewset with the router
router.register(r'spatial-metadata', SpatialMetaDataViewSet, basename='spatialmetadata')

# Define the urlpatterns
urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
]

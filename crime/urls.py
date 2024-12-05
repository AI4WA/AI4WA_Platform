from crime.views import CrimeListView, CrimeDetailView, CrimeViewSet

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'views', CrimeViewSet)

app_name = 'crimes'  # for namespace

urlpatterns = [
    path('', CrimeListView.as_view(), name='crime_list'),
    path('<int:pk>/', CrimeDetailView.as_view(), name='crime_detail'),
    path('api/', include(router.urls)),
]

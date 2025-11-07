# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoinViewSet

router = DefaultRouter()
router.register(r"coins", CoinViewSet, basename="coin")

urlpatterns = [
    path("", include(router.urls)),
]

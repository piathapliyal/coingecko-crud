from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, fetch_btc, report

router = DefaultRouter()
router.register(r'items', ItemViewSet)


urlpatterns = [
    path('', include(router.urls)),    
    path('fetch-btc/', fetch_btc),    
    path('report/', report),         
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'customer', views.CustomerViewSet)
router.register(r'account', views.ActionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = DefaultRouter()

router.register(r'customer', views.CustomerViewSet)
router.register(r'account', views.ActionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
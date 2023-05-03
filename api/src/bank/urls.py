from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'account', views.AccountViewSet)
router.register(r'action', views.ActionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('customer/', views.CustomerView.as_view()),
]
from django.contrib import admin
from django.urls import path, re_path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('src.bank.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
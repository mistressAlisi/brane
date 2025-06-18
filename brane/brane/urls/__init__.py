from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path('admin/', admin.site.urls)
]
if settings.BRANE_SETUP:
    from .runtime import _urlpatterns
else:
   from .setup import _urlpatterns
urlpatterns += _urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
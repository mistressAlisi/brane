from django.contrib import admin
from django.urls import path, include
from . import views
# Brane setup application
urlpatterns = [
    path("api/", include("setup.api_urls")),
    path("", views.index_handle, name="index_handle"),
    path("create", views.create_pod_handle, name="create_pod_handle"),
    path("create/validate", views.create_pod_validate_handle, name="create_pod_validate_handle"),
    path("create/execute", views.create_pod_execute_handle, name="create_pod_execute_handle"),
]

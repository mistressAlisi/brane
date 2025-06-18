from django.urls import path
from . import api_views
urlpatterns = [
    path("create/execute",api_views.install_exec_handle,name="install_exec_handle"),
]
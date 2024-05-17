from django.urls import path, include
from base.views import start, admin

urlpatterns = [
    path("start", start, name="index"),
    path("bot/admin/", admin, name="admin"),
]

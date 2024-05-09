from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    # path("profile", views.profile, name="profile"),
    # ... other URL patterns myapp/urls.py
    path("", include("myapp.urls")),
    path("admin/", admin.site.urls),
]

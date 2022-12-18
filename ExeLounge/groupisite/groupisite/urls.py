"""groupisite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
import groupisite.views as groupisite_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from forum import views as forum_views
from public_chat import views as chat_views
from users import views as users_views

urlpatterns = [
    path("favicon.ico", groupisite_views.favicon),
    path("admin/login/", users_views.user_login),
    path("admin/", admin.site.urls),
    path("register/", users_views.user_register),
    path("login/", users_views.user_login),
    path("", groupisite_views.home),
    path("logout/", users_views.user_logout),
    path("settings/", users_views.settings),
    path("settings/change-password/", users_views.change_password),
    path(".well-known/change-password/", users_views.change_password_redirect),
    path("change-password/", users_views.change_password_redirect),
    path("live-chat/", chat_views.live_chat),
    path("forums/", forum_views.forum_home),
    path("forums/<slug:category>/<slug:section>/", forum_views.forum_section),
    path("forums/<slug:category>/<slug:section>/<slug:thread>/", forum_views.forum_thread),
    path("forums/<slug:category>/<slug:section>/<slug:thread>/<slug:post>/", forum_views.forum_post)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

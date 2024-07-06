"""
URL configuration for YT_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("master/", include('master.urls')),#URL Path for master app
    # path("base_user/", include('base_user.urls')),#URL Path for base_users app
    path("app_users/", include('app_users.urls')),#URL Path for app_users app
    path("video/", include('video.urls')),#URL Path for video app
]

# Media files settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
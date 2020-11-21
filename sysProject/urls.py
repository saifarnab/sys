"""sysProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('sys/admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', include(('userProfile.urls'))),
    path('event/', include('event.urls')),
    path('banner/', include('banner.urls')),
    path('videos/', include('videos.urls')),
    path('', include('home.urls')),
    path('slider/', include('slider.urls')),
    path('invoice/', include('invoice.urls')),
    path('org-event-confirm/', include('orgEventConfirm.urls')),

]

# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

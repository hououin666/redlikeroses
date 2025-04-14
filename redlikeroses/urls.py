"""
URL configuration for redlikeroses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from ast import increment_lineno

from django.conf import settings
from django.conf.urls.static import  static
from django.contrib import admin
from django.urls import path
from django.urls import include




admin.site.site_title = "Rings site admin"
admin.site.site_header = "Rings administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'), name='products'),
    path('users/', include('users.urls'), name='users'),
    path('cart/', include('cart.urls'), name ='cart'),
    path('orders/', include('orders.urls'), name='orders'),



]


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



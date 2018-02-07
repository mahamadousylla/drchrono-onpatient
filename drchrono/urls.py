"""drchrono URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from polls import views


urlpatterns = [
	# url(r'', views.welcome, name='welcome'),
	url(r'^welcome', views.welcome, name='welcome'),
	url(r'home', views.home, name='home'),

	url(r'^bp', views.bp, name='bp'),
  url(r'^chart_bp', views.chart_bp, name='chart_bp'),

	url(r'^sleep', views.sleep, name='sleep'),
  url(r'^chart_sleep', views.chart_sleep, name='chart_sleep'),

  url(r'^weight', views.weight, name='weight'),
  url(r'^chart_weight', views.chart_weight, name='chart_weight'),

  url(r'^hydrate', views.hydrate, name='hydrate'),
  url(r'^chart_hydrate', views.chart_hydrate, name='chart_hydrate'),

  url(r'index', views.logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

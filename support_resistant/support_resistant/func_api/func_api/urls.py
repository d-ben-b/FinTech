"""func_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from options_func import views

router = routers.DefaultRouter()
router.register(r'gap', views.GapViewSet, basename="gap")
router.register(r'volume', views.VolumeViewSet, basename="volume")
router.register(r'supportresistance', views.SupportResistanceViewSet, basename="supportresistance")
router.register(r'supportsignal', views.SupportSignalViewSet, basename="supportsignal")
router.register(r'resistancesignal', views.ResistanceSignalViewSet, basename="resistancesignal")
router.register(r'neckline', views.NecklineViewSet, basename="neckline")
router.register(r'necklinesupsignal', views.NecklineSupSignalViewSet, basename="necklinesupsignal")
router.register(r'necklineressignal', views.NecklineResSignalViewSet, basename="necklineressignal")
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('usFunc2/admin/', admin.site.urls),
    path('usFunc2/', include(router.urls)),
    path('usFunc2/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


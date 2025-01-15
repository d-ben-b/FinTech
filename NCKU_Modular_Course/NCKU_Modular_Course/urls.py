"""
URL configuration for NCKU_Modular_Course project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from sum import views
from day1 import views as day1_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sum/", views.sum),
    path("ajax_sum/", views.ajax_sum),
    # path("day1/", include("day1.urls")),
    # path("day1/", day1_views.day1_view, name="day1"),
    path("day1/analyze/", day1_views.analyze_from_vue, name="analyze"),
    path("day2/", include("day2.urls")),
    path("day3/", include("day3.urls")),
]

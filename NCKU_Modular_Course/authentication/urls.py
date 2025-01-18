from day1 import views as day1_views
from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("day1/analyze/", day1_views.analyze_from_vue, name="analyze"),
    path("day2/", include("day2.urls")),
    path("day3/", include("day3.urls")),
    path("check-auth/", views.CheckAuthAPIView.as_view(), name="check-auth"),
]

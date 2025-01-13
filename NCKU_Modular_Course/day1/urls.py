from django.urls import path
from . import views

urlpatterns = [
    path("day1/", views.analyze, name="analyze"),
]

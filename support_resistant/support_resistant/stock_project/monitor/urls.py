from django.urls import path
from . import views

urlpatterns = [
    path('', views.web, name='web'),
    path('get_track_list/', views.get_track_list, name='get_track_list'),
    path('add_track/', views.add_track, name='add_track'),
    path('remove_track/', views.remove_track, name='remove_track'),
    path('run_analysis/', views.run_analysis, name='run_analysis'),
]

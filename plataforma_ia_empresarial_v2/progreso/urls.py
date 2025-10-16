from django.urls import path
from . import views

app_name = 'progreso'

urlpatterns = [
    path('', views.panel_progreso, name='panel_progreso'),
]
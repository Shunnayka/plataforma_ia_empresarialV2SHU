from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('', views.lista_modulos, name='lista_modulos'),
    path('modulo/<int:modulo_id>/', views.modulo_detalle, name='modulo_detalle'),
    path('dashboard-adaptativo/', views.dashboard_adaptativo, name='dashboard_adaptativo'),
]
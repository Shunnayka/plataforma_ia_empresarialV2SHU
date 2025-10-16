from django.urls import path
from . import views

app_name = 'evaluaciones'

urlpatterns = [
    path('diagnostico/<int:modulo_id>/', views.diagnostico_modulo, name='diagnostico_modulo'),
    path('resultado/<int:modulo_id>/', views.resultado_diagnostico, name='resultado_diagnostico'),
]
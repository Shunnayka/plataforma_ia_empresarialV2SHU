from django.urls import path
from . import views

app_name = 'certificados'

urlpatterns = [
    path('generar/<int:modulo_id>/', views.generar_certificado, name='generar_certificado'),
    path('mis-certificados/', views.mis_certificados, name='mis_certificados'),
    path('verificar/<str:codigo>/', views.verificar_certificado, name='verificar_certificado'),
]
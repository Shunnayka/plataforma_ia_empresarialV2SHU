from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    path('dashboard-empresa/', views.dashboard_empresa, name='dashboard_empresa'),
    path('empleados/<str:empresa>/', views.detalle_empleados, name='detalle_empleados'),
]
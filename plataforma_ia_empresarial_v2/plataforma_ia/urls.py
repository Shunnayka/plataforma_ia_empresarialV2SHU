from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cursos/', include('cursos.urls')),
    path('evaluaciones/', include('evaluaciones.urls')),
    path('progreso/', include('progreso.urls')),
    path('tutor-ia/', include('tutor_ia.urls')),
    path('certificados/', include('certificados.urls')),
    path('', usuarios_views.login_view, name='login'),
    path('usuarios/registro/', usuarios_views.registro_view, name='registro'),
    path('administracion/', include('administracion.urls')),
]
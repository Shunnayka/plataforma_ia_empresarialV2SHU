from django.urls import path
from . import views

app_name = 'tutor_ia'

urlpatterns = [
    path('chat/', views.chat_tutor, name='chat_tutor'),
    path('chat/<int:modulo_id>/', views.chat_tutor, name='chat_modulo'),
    path('enviar-pregunta/', views.enviar_pregunta, name='enviar_pregunta'),
    path('borrar-conversacion/', views.borrar_conversacion, name='borrar_conversacion'), 
]
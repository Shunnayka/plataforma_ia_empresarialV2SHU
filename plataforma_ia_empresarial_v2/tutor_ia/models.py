from django.db import models
from cursos.models import Modulo
from usuarios.models import Usuario

class RespuestaPredefinida(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, null=True, blank=True)
    pregunta_clave = models.CharField(max_length=200)
    respuesta = models.TextField()
    tags = models.CharField(max_length=100, help_text="Palabras clave separadas por coma")
    
    class Meta:
        app_label = 'tutor_ia' 
    
    def __str__(self):
        return self.pregunta_clave

class ConversacionTutor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.SET_NULL, null=True, blank=True)
    pregunta = models.TextField()
    respuesta = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'tutor_ia' 
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.usuario.email} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
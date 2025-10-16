from django.db import models
from usuarios.models import Usuario
from cursos.models import Modulo

class Pregunta(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    texto = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ('opcion_multiple', 'Opción Múltiple'),
        ('verdadero_falso', 'Verdadero/Falso'),
    ])
    
    def __str__(self):
        return f"{self.modulo.nombre}: {self.texto[:50]}..."

class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=200)
    es_correcta = models.BooleanField(default=False)
    
    def __str__(self):
        return self.texto

class DiagnosticoInicial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    puntaje = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['usuario', 'modulo']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.modulo.nombre}: {self.puntaje}"
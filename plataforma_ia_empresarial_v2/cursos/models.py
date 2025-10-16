from django.db import models
from usuarios.models import Usuario

class Modulo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_estimada = models.IntegerField(help_text="Duración en minutos")
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return self.nombre

class ContenidoModulo(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='contenidos')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=[
        ('teoria', 'Teoría'),
        ('video', 'Video'), 
        ('ejercicio', 'Ejercicio'),
        ('quiz', 'Quiz'),
    ])
    contenido = models.TextField()
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):  
        return f"{self.modulo.nombre} - {self.titulo}"

class RecomendacionEstudio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    modulo_recomendado = models.ForeignKey(Modulo, on_delete=models.CASCADE)  
    razon = models.TextField()
    prioridad = models.IntegerField(default=1)
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    completada = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['prioridad', '-fecha_recomendacion']
    
    def __str__(self):
        return f"Recomendación para {self.usuario.username}: {self.modulo_recomendado.nombre}"
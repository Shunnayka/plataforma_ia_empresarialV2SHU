from django.db import models
from usuarios.models import Usuario
from cursos.models import Modulo

class ProgresoUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    modulos_completados = models.ManyToManyField(Modulo, blank=True)
    total_modulos = models.IntegerField(default=3)  # Tus 3 módulos
    porcentaje_avance = models.FloatField(default=0.0)
    
    def actualizar_progreso(self):
        completados = self.modulos_completados.count()
        self.porcentaje_avance = (completados / self.total_modulos) * 100
        self.save()
    
    def __str__(self):
        return f"Progreso de {self.usuario.username}: {self.porcentaje_avance}%"
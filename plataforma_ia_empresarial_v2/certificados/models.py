from django.db import models
from usuarios.models import Usuario
from cursos.models import Modulo
import uuid

class Certificado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    codigo_verificacion = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_completacion = models.DateTimeField()
    puntaje_final = models.IntegerField()
    
    class Meta:
        unique_together = ['usuario', 'modulo']
    
    def __str__(self):
        return f"Certificado {self.modulo.nombre} - {self.usuario.username}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_verificacion:
            self.codigo_verificacion = f"CERT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
from django.db import models
from usuarios.models import Usuario
from cursos.models import Modulo

class ReporteEmpresa(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    total_empleados = models.IntegerField(default=0)
    modulos_completados = models.IntegerField(default=0)
    promedio_general = models.FloatField(default=0.0)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reporte {self.nombre_empresa} - {self.fecha_generacion.date()}"

class BrechaCompetencia(models.Model):
    empresa = models.CharField(max_length=100)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    porcentaje_bajo = models.FloatField(default=0.0)
    empleados_afectados = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Brecha {self.modulo.nombre} - {self.empresa}"
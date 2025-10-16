from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    empresa = models.CharField(max_length=100, blank=True)
    puesto = models.CharField(max_length=100, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    class Meta:
        db_table = 'usuarios'
    
    def __str__(self):
        return f"{self.username} - {self.empresa}"
from django.contrib import admin
from .models import Modulo, ContenidoModulo

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'activo')
    list_filter = ('activo',)
    ordering = ('orden',)

@admin.register(ContenidoModulo)
class ContenidoModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'tipo', 'orden')
    list_filter = ('modulo', 'tipo')
    ordering = ('modulo', 'orden')
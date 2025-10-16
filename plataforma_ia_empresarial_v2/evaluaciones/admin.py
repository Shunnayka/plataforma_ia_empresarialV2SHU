from django.contrib import admin
from .models import Pregunta, OpcionRespuesta, DiagnosticoInicial

class OpcionRespuestaInline(admin.TabularInline):
    model = OpcionRespuesta
    extra = 4

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'modulo', 'tipo']
    list_filter = ['modulo', 'tipo']
    inlines = [OpcionRespuestaInline]

admin.site.register(DiagnosticoInicial)
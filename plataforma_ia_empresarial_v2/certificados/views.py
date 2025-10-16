from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Certificado
from cursos.models import Modulo
from evaluaciones.models import DiagnosticoInicial
from datetime import datetime

@login_required
def generar_certificado(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    
    # Verificar si el usuario completó el módulo
    diagnostico = DiagnosticoInicial.objects.filter(
        usuario=request.user,
        modulo=modulo,
        completado=True
    ).order_by('-fecha').first()
    
    if not diagnostico or diagnostico.puntaje < 2:
        return render(request, 'certificados/no_aprobado.html', {
            'modulo': modulo,
            'diagnostico': diagnostico
        })
    
    # Crear o obtener certificado
    certificado, created = Certificado.objects.get_or_create(
        usuario=request.user,
        modulo=modulo,
        defaults={
            'fecha_completacion': diagnostico.fecha,
            'puntaje_final': diagnostico.puntaje
        }
    )
    
    # Calcular porcentaje
    porcentaje = round((certificado.puntaje_final / 3) * 100)
    
    return render(request, 'certificados/certificado.html', {
        'certificado': certificado,
        'modulo': modulo,
        'usuario': request.user,
        'porcentaje': porcentaje
    })

@login_required
def mis_certificados(request):
    certificados = Certificado.objects.filter(usuario=request.user).order_by('-fecha_emision')
    return render(request, 'certificados/lista.html', {
        'certificados': certificados
    })

@login_required
def verificar_certificado(request, codigo):
    certificado = get_object_or_404(Certificado, codigo_verificacion=codigo)
    return render(request, 'certificados/verificacion.html', {
        'certificado': certificado
    })
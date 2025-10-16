from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProgresoUsuario
from cursos.models import Modulo
from evaluaciones.models import DiagnosticoInicial

@login_required
def panel_progreso(request):
    # Obtener o crear progreso del usuario
    progreso, created = ProgresoUsuario.objects.get_or_create(usuario=request.user)
    
    # Obtener todos los módulos con su estado
    modulos_con_estado = []
    for modulo in Modulo.objects.all():
        diagnostico = DiagnosticoInicial.objects.filter(
            usuario=request.user, 
            modulo=modulo
        ).order_by('-fecha').first()
        
        completado = diagnostico and diagnostico.puntaje >= 2  # 2/3 o más
        
        modulos_con_estado.append({
            'modulo': modulo,
            'completado': completado,
            'puntaje': diagnostico.puntaje if diagnostico else 0,
            'total_preguntas': 3  # Tus módulos tienen 3 preguntas
        })
    
    # Actualizar progreso
    progreso.actualizar_progreso()
    
    return render(request, 'progreso/panel.html', {
        'progreso': progreso,
        'modulos_con_estado': modulos_con_estado
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Pregunta, DiagnosticoInicial
from cursos.models import Modulo
from cursos.utils import generar_recomendaciones_adaptativas

@login_required
def diagnostico_modulo(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    preguntas = Pregunta.objects.filter(modulo=modulo)
    
    if request.method == 'POST':
        puntaje = 0
        for pregunta in preguntas:
            respuesta_id = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_id:
                try:
                    opcion_elegida = pregunta.opciones.get(id=respuesta_id)
                    if opcion_elegida.es_correcta:
                        puntaje += 1
                except:
                    pass
        
        diagnostico, created = DiagnosticoInicial.objects.get_or_create(
            usuario=request.user,
            modulo=modulo
        )
        diagnostico.puntaje = puntaje
        diagnostico.completado = True
        diagnostico.save()

        generar_recomendaciones_adaptativas(request.user)
        
        return redirect('evaluaciones:resultado_diagnostico', modulo_id=modulo_id)
    
    return render(request, 'evaluaciones/diagnostico.html', {
        'modulo': modulo,
        'preguntas': preguntas,
    })

@login_required
def resultado_diagnostico(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    diagnostico = DiagnosticoInicial.objects.filter(
        usuario=request.user, 
        modulo=modulo
    ).order_by('-fecha').first()
    
    total_preguntas = Pregunta.objects.filter(modulo=modulo).count()
    porcentaje = 0
    if total_preguntas > 0:
        porcentaje = round((diagnostico.puntaje / total_preguntas) * 100)
    
    return render(request, 'evaluaciones/resultado.html', {
        'modulo': modulo,
        'diagnostico': diagnostico,
        'total_preguntas': total_preguntas,
        'porcentaje': porcentaje
    })
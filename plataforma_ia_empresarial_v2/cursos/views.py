from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Modulo, ContenidoModulo
from .utils import obtener_ruta_aprendizaje, generar_recomendaciones_adaptativas

@login_required
def lista_modulos(request):
    modulos = Modulo.objects.filter(activo=True).order_by('orden')
    return render(request, 'cursos/lista_modulos.html', {'modulos': modulos})

@login_required
def modulo_detalle(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    contenidos = modulo.contenidos.all().order_by('orden')
    return render(request, 'cursos/modulo_detalle.html', {
        'modulo': modulo,
        'contenidos': contenidos
    })

@login_required
def dashboard_adaptativo(request):
    ruta_aprendizaje = obtener_ruta_aprendizaje(request.user)
    
    modulos_completados = []
    for modulo in Modulo.objects.filter(activo=True):
        from evaluaciones.models import DiagnosticoInicial
        diagnostico = DiagnosticoInicial.objects.filter(
            usuario=request.user,
            modulo=modulo,
            completado=True,
            puntaje__gte=2
        ).first()
        if diagnostico:
            modulos_completados.append(modulo)
    
    return render(request, 'cursos/dashboard_adaptativo.html', {
        'ruta_aprendizaje': ruta_aprendizaje,
        'modulos_completados': modulos_completados,
        'total_modulos': Modulo.objects.filter(activo=True).count()
    })
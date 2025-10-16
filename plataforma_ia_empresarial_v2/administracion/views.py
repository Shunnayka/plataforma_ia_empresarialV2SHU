from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.models import Usuario
from cursos.models import Modulo
from evaluaciones.models import DiagnosticoInicial
from certificados.models import Certificado

def es_administrador(user):
    return user.is_staff

@login_required
@user_passes_test(es_administrador)
def dashboard_empresa(request):
    # Obtener todas las empresas únicas
    empresas = Usuario.objects.exclude(empresa='').values_list('empresa', flat=True).distinct()
    
    reportes_empresas = []
    
    for empresa in empresas:
        empleados = Usuario.objects.filter(empresa=empresa)
        total_empleados = empleados.count()
        
        # Calcular métricas
        modulos_completados = 0
        puntajes_totales = 0
        diagnosticos_totales = 0
        
        for empleado in empleados:
            certificados = Certificado.objects.filter(usuario=empleado)
            modulos_completados += certificados.count()
            
            diagnosticos = DiagnosticoInicial.objects.filter(usuario=empleado, completado=True)
            diagnosticos_totales += diagnosticos.count()
            for diagnostico in diagnosticos:
                puntajes_totales += diagnostico.puntaje
        
        promedio_general = 0
        if diagnosticos_totales > 0:
            promedio_general = round((puntajes_totales / diagnosticos_totales) * 33.33, 2)
        
        reportes_empresas.append({
            'empresa': empresa,
            'total_empleados': total_empleados,
            'modulos_completados': modulos_completados,
            'promedio_general': promedio_general,
            'empleados': empleados
        })
    
    return render(request, 'administracion/dashboard_empresa.html', {
        'reportes_empresas': reportes_empresas
    })

@login_required
@user_passes_test(es_administrador)
def detalle_empleados(request, empresa):
    empleados = Usuario.objects.filter(empresa=empresa)
    
    empleados_con_progreso = []
    for empleado in empleados:
        certificados = Certificado.objects.filter(usuario=empleado)
        diagnosticos = DiagnosticoInicial.objects.filter(usuario=empleado, completado=True)
        
        progreso = {
            'empleado': empleado,
            'certificados': certificados,
            'total_diagnosticos': diagnosticos.count(),
            'modulos_completados': certificados.count()
        }
        empleados_con_progreso.append(progreso)
    
    return render(request, 'administracion/detalle_empleados.html', {
        'empresa': empresa,
        'empleados_con_progreso': empleados_con_progreso
    })
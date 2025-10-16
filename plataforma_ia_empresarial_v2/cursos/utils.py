from .models import Modulo, RecomendacionEstudio
from evaluaciones.models import DiagnosticoInicial

def generar_recomendaciones_adaptativas(usuario):
    # Eliminar recomendaciones anteriores no completadas
    RecomendacionEstudio.objects.filter(usuario=usuario, completada=False).delete()
    
    recomendaciones = []
    
    # Analizar resultados de diagnóstico por módulo
    for modulo in Modulo.objects.filter(activo=True):
        diagnostico = DiagnosticoInicial.objects.filter(
            usuario=usuario,
            modulo=modulo,
            completado=True
        ).order_by('-fecha').first()
        
        if not diagnostico:
            # Si no ha hecho diagnóstico, recomendar hacerlo
            recomendaciones.append(RecomendacionEstudio(
                usuario=usuario,
                modulo_recomendado=modulo,  # ← CAMBIAR 'modulo' por 'modulo_recomendado'
                razon=f"Realiza el diagnóstico inicial para evaluar tus conocimientos en {modulo.nombre}",
                prioridad=1
            ))
        elif diagnostico.puntaje < 2:
            # Si salió mal, recomendar reforzar
            recomendaciones.append(RecomendacionEstudio(
                usuario=usuario,
                modulo_recomendado=modulo,  # ← CAMBIAR 'modulo' por 'modulo_recomendado'
                razon=f"Necesitas reforzar {modulo.nombre} (puntaje: {diagnostico.puntaje}/3)",
                prioridad=1
            ))
        elif diagnostico.puntaje == 2:
            # Si salió regular, recomendar practicar
            recomendaciones.append(RecomendacionEstudio(
                usuario=usuario,
                modulo_recomendado=modulo,  # ← CAMBIAR 'modulo' por 'modulo_recomendado'
                razon=f"Puedes mejorar en {modulo.nombre} (puntaje: {diagnostico.puntaje}/3)",
                prioridad=2
            ))
        else:
            # Si salió bien, marcar como completada si existe recomendación
            pass
    
    # Guardar todas las recomendaciones
    RecomendacionEstudio.objects.bulk_create(recomendaciones)
    
    return recomendaciones

def obtener_ruta_aprendizaje(usuario):
    # Generar recomendaciones actualizadas
    generar_recomendaciones_adaptativas(usuario)
    
    # Obtener recomendaciones ordenadas por prioridad
    return RecomendacionEstudio.objects.filter(usuario=usuario, completada=False)
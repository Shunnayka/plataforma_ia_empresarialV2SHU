from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Importaciones CORREGIDAS
from .models import ConversacionTutor, RespuestaPredefinida
from cursos.models import Modulo

@login_required
def chat_tutor(request, modulo_id=None):
    modulo = None
    if modulo_id:
        modulo = get_object_or_404(Modulo, id=modulo_id)
    
    conversaciones = ConversacionTutor.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:10]
    
    return render(request, 'tutor_ia/chat.html', {
        'modulo': modulo,
        'conversaciones': conversaciones
    })

@login_required
@csrf_exempt
def enviar_pregunta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pregunta = data.get('pregunta', '').strip()
            modulo_id = data.get('modulo_id')
            
            if not pregunta:
                return JsonResponse({'error': 'La pregunta no puede estar vacía'}, status=400)
            
            modulo = None
            if modulo_id:
                try:
                    modulo = Modulo.objects.get(id=modulo_id)
                except Modulo.DoesNotExist:
                    pass
            
            # Usa tu función generar_respuesta original
            respuesta = generar_respuesta(pregunta, modulo, request.user)
            
            conversacion = ConversacionTutor.objects.create(
                usuario=request.user,
                modulo=modulo,
                pregunta=pregunta,
                respuesta=respuesta
            )
            
            return JsonResponse({
                'respuesta': respuesta,
                'fecha': conversacion.fecha.strftime('%d/%m/%Y %H:%M')
            })
            
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
@csrf_exempt
def borrar_conversacion(request):
    if request.method == 'POST':
        try:
            # Borrar todas las conversaciones del usuario
            conversaciones_borradas = ConversacionTutor.objects.filter(
                usuario=request.user
            ).delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Se borraron {conversaciones_borradas[0]} conversaciones'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Error al borrar la conversación'
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# PEGA AQUÍ TU FUNCIÓN generar_respuesta ORIGINAL COMPLETA
def generar_respuesta(pregunta, modulo, usuario):
    pregunta_lower = pregunta.lower().strip()
    
    # ===== 1. SALUDOS Y CORTESÍAS =====
    saludos = ['hola', 'holi', 'hey', 'hi', 'buenos días', 'buenas tardes', 'buenas noches', 'qué tal', 'qué hubo']
    if any(saludo in pregunta_lower for saludo in saludos):
        return "¡Hola! 👋 Soy tu tutor IA. Puedo ayudarte con:\n• Tu progreso y áreas a mejorar\n• Explicación de temas\n• Resultados de diagnósticos\n• Consejos de aprendizaje\n• Cómo usar la plataforma\n\n¿En qué te puedo ayudar hoy?"
    
    # ===== 2. DESPEDIDAS =====
    despedidas = ['adiós', 'chao', 'bye', 'nos vemos', 'hasta luego', 'gracias', 'thx', 'ty']
    if any(despedida in pregunta_lower for despedida in despedidas):
        return "¡Ha sido un gusto ayudarte! 😊 Recuerda que estoy aquí cuando necesites. ¡Mucho éxito en tu aprendizaje! 🚀"
    
    # ===== 3. PROGRESO Y ÁREAS A MEJORAR =====
    if any(palabra in pregunta_lower for palabra in ['mejorar', 'áreas', 'débil', 'fortaleza', 'progreso', 'avance', 'cómo voy', 'cómo estoy', 'debo mejorar', 'qué me falta']):
        from cursos.utils import obtener_ruta_aprendizaje
        from evaluaciones.models import DiagnosticoInicial
        
        ruta_aprendizaje = obtener_ruta_aprendizaje(usuario)
        diagnosticos = DiagnosticoInicial.objects.filter(usuario=usuario, completado=True)
        
        if ruta_aprendizaje:
            modulos_alta = [r.modulo_recomendado for r in ruta_aprendizaje if r.prioridad == 1]
            modulos_media = [r.modulo_recomendado for r in ruta_aprendizaje if r.prioridad == 2]
            
            respuesta = ""
            
            if modulos_alta:
                respuesta += f"🎯 **Áreas críticas para mejorar (Alta prioridad)**:\n"
                for modulo in modulos_alta:
                    # Verificar si ya hizo diagnóstico
                    diag = diagnosticos.filter(modulo=modulo).first()
                    puntaje = f" - Puntaje: {diag.puntaje}/3" if diag else " - Sin diagnóstico"
                    respuesta += f"• {modulo.nombre}{puntaje}\n"
                
                respuesta += "\n**Acción recomendada**:\n"
                respuesta += "1. 📖 Revisa el contenido del módulo\n"
                respuesta += "2. 🧪 Realiza el diagnóstico inicial\n" 
                respuesta += "3. 🔄 Practica con ejercicios prácticos\n"
                respuesta += "4. 📊 Vuelve a evaluar tu progreso\n\n"
            
            if modulos_media:
                respuesta += f"📈 **Áreas para fortalecer (Prioridad media)**:\n"
                for modulo in modulos_media:
                    diag = diagnosticos.filter(modulo=modulo).first()
                    puntaje = f" - Puntaje: {diag.puntaje}/3" if diag else " - Sin diagnóstico"
                    respuesta += f"• {modulo.nombre}{puntaje}\n"
                
                respuesta += "\n**Sugerencia**: Puedes repasar estos temas cuando tengas tiempo disponible.\n\n"
            
            if not modulos_alta and not modulos_media:
                respuesta += "¡Excelente! 🎉 No tienes áreas críticas que mejorar. "
            
            respuesta += "¿Quieres que te explique algún tema específico o necesitas más detalles sobre algún módulo?"
            
            return respuesta
        else:
            return "🤔 **Para conocer tus áreas a mejorar**, realiza los diagnósticos de los módulos. Cada diagnóstico te dará recomendaciones personalizadas basadas en tus resultados.\n\n¿Quieres intentar con algún módulo en particular?"
        
    # ===== 3.1 QUÉ ESTUDIAR - RECOMENDACIONES DE ESTUDIO =====
    if any(palabra in pregunta_lower for palabra in ['qué debo estudiar', 'qué estudiar', 'qué aprender', 'por dónde empezar', 'recomiéndame', 'qué módulo', 'cuál módulo']):
        from cursos.utils import obtener_ruta_aprendizaje
        from evaluaciones.models import DiagnosticoInicial
        from certificados.models import Certificado
        
        # Obtener módulos completados
        modulos_completados = Certificado.objects.filter(usuario=usuario).values_list('modulo_id', flat=True)
        
        # Obtener diagnósticos realizados
        diagnosticos_realizados = DiagnosticoInicial.objects.filter(usuario=usuario, completado=True).values_list('modulo_id', flat=True)
        
        # Obtener ruta de aprendizaje personalizada
        ruta_aprendizaje = obtener_ruta_aprendizaje(usuario)
        
        if ruta_aprendizaje:
            # Filtrar módulos no completados y con alta prioridad
            modulos_recomendados = [
                r.modulo_recomendado for r in ruta_aprendizaje 
                if r.modulo_recomendado.id not in modulos_completados
            ]
            
            if modulos_recomendados:
                respuesta = "🎯 **Basado en tu progreso, te recomiendo estudiar**:\n\n"
                
                for i, modulo in enumerate(modulos_recomendados[:3], 1):
                    estado = "⚠️ **CRÍTICO**" if modulo.id in diagnosticos_realizados else "📚 **NUEVO**"
                    respuesta += f"{i}. **{modulo.nombre}** - {estado}\n"
                    respuesta += f"   • {modulo.descripcion}\n"
                    respuesta += f"   • Duración: {modulo.duracion_estimada}\n\n"
                
                respuesta += "💡 **Sugerencia**: Comienza por el módulo marcado como ⚠️ CRÍTICO si necesitas mejorar, o por 📚 NUEVO para aprender algo diferente."
                
                return respuesta
        
        # Si no hay ruta de aprendizaje personalizada, sugerir módulos generales
        from cursos.models import Modulo
        modulos_disponibles = Modulo.objects.exclude(id__in=modulos_completados)
        
        if modulos_disponibles:
            respuesta = "📚 **Te recomiendo estos módulos disponibles**:\n\n"
            for i, modulo in enumerate(modulos_disponibles[:4], 1):
                respuesta += f"{i}. **{modulo.nombre}**\n"
                respuesta += f"   • {modulo.descripcion}\n"
                respuesta += f"   • Nivel: {modulo.get_nivel_dificultad_display()}\n\n"
            
            respuesta += "✨ **Consejo**: Si no estás seguro por dónde empezar, realiza el diagnóstico inicial de cualquier módulo para obtener recomendaciones personalizadas."
            
            return respuesta
        else:
            return "🎉 **¡Felicidades!** Has completado todos los módulos disponibles. ¿Te gustaría repasar algún tema específico o profundizar en lo que ya aprendiste?"
    
    # ===== 3.2 PLAN DE ESTUDIO PERSONALIZADO =====
    if any(palabra in pregunta_lower for palabra in ['plan de estudio', 'plan de estudios', 'organizar estudio', 'cómo organizarme', 'rutina de estudio']):
        from cursos.models import Modulo
        from certificados.models import Certificado
        
        modulos_completados = Certificado.objects.filter(usuario=usuario).count()
        modulos_totales = Modulo.objects.count()
        progreso = (modulos_completados / modulos_totales * 100) if modulos_totales > 0 else 0
        
        respuesta = f"📊 **Tu progreso actual**: {modulos_completados}/{modulos_totales} módulos ({progreso:.1f}%)\n\n"
        respuesta += "🎯 **Plan de estudio recomendado**:\n\n"
        respuesta += "1. **Sesiones cortas** (25-30 minutos) con descansos de 5 minutos\n"
        respuesta += "2. **Consistencia** > Intensidad: Mejor 30 min/día que 3 horas un día\n"
        respuesta += "3. **Orden sugerido**:\n"
        respuesta += "   - Lunes: Seguridad Digital 🔒\n"
        respuesta += "   - Martes: Word 📝\n"
        respuesta += "   - Miércoles: Excel 📊\n"
        respuesta += "   - Jueves: PowerPoint 🎯\n"
        respuesta += "   - Viernes: Comunicación Digital 📧\n"
        respuesta += "   - Fin de semana: Repaso y práctica\n\n"
        respuesta += "💡 **Tips adicionales**:\n"
        respuesta += "• Establece metas diarias realistas\n"
        respuesta += "• Practica inmediatamente lo aprendido\n"
        respuesta += "• Enseña a alguien más para reforzar\n"
        respuesta += "• Usa los diagnósticos para medir tu avance\n\n"
        respuesta += "¿Te gustaría que personalice más este plan según tu disponibilidad de tiempo?"
        
        return respuesta
    
    # ===== 4. MÓDULOS COMPLETADOS Y CERTIFICADOS =====
    if any(palabra in pregunta_lower for palabra in ['completado', 'terminado', 'hecho', 'finalizado', 'certificado', 'diploma']):
        from certificados.models import Certificado
        certificados = Certificado.objects.filter(usuario=usuario)
        
        if certificados:
            modulos = [f"{cert.modulo.nombre} ({cert.puntaje_final}/3)" for cert in certificados]
            return f"🏆 **Módulos completados**:\n{chr(10).join(['• ' + modulo for modulo in modulos])}\n\n¡Felicidades! ¿Quieres seguir con otro módulo o reforzar lo aprendido?"
        else:
            return "📚 **Aún no tienes módulos completados**. Para obtener un certificado:\n1. Estudia el módulo\n2. Realiza el diagnóstico\n3. Obtén 2/3 o más\n4. Ve a 'Obtener Certificado'\n\n¿Por cuál módulo quieres empezar?"
    
    # ===== 5. PUNTAJES Y RESULTADOS =====
    if any(palabra in pregunta_lower for palabra in ['puntaje', 'calificación', 'nota', 'resultado', 'cuánto saqué']):
        from evaluaciones.models import DiagnosticoInicial
        diagnosticos = DiagnosticoInicial.objects.filter(usuario=usuario, completado=True).order_by('-fecha')
        
        if diagnosticos:
            respuesta = "📊 **Tus resultados recientes**:\n"
            for diagnostico in diagnosticos[:5]:
                emoji = "✅" if diagnostico.puntaje >= 2 else "⚠️"
                respuesta += f"{emoji} {diagnostico.modulo.nombre}: {diagnostico.puntaje}/3\n"
            
            if any(d.puntaje < 2 for d in diagnosticos):
                respuesta += "\n💡 **Consejo**: Los módulos con ⚠️ necesitan repaso. ¿Quieres mejorar algún puntaje?"
            else:
                respuesta += "\n🎉 **¡Excelente trabajo!** Todos tus resultados son sólidos."
            
            return respuesta
        else:
            return "📝 **Aún no tienes resultados**. Realiza el diagnóstico de algún módulo para:\n• Conocer tu nivel actual\n• Obtener recomendaciones\n• Identificar áreas de mejora\n\n¿Quieres intentar con algún módulo?"
    
    # ===== 6. CÓMO FUNCIONA LA PLATAFORMA =====
    if any(palabra in pregunta_lower for palabra in ['cómo funciona', 'usar', 'utilizar', 'qué hago', 'por dónde']):
        return "🛠️ **Guía rápida de la plataforma**:\n\n1. **Módulos**: Estudia el contenido de cada tema\n2. **Diagnóstico**: Evalúa tu conocimiento (3 preguntas)\n3. **Resultado**: Obtén tu puntaje y recomendaciones\n4. **Certificado**: Consíguelo al aprobar (2/3 o más)\n5. **Progreso**: Ve tu avance general\n6. **Tutor IA**: Pregúntame cualquier duda\n\n¿Necesitas ayuda con algo específico?"
    
    # ===== 7. EXPLICACIÓN DE CONTENIDOS =====
    # SEGURIDAD DIGITAL
    if any(palabra in pregunta_lower for palabra in ['seguridad', 'contraseña', 'password', 'phishing', 'hacker', 'virus', 'malware']):
        return "🔒 **Seguridad Digital - Conceptos clave**:\n\n• **Contraseñas seguras**: Mínimo 8 caracteres, mezcla mayúsculas, minúsculas, números y símbolos. No reutilices contraseñas.\n\n• **Phishing**: Emails falsos que buscan robar información. Señales: urgencia, errores gramaticales, enlaces sospechosos.\n\n• **Autenticación en dos factores**: Capa extra de seguridad además de la contraseña.\n\n¿Quieres profundizar en algún tema específico de seguridad?"
    
    # OFIMÁTICA
    if any(palabra in pregunta_lower for palabra in ['word', 'documento', 'texto', 'ofimática', 'office']):
        return "📝 **Microsoft Word - Lo esencial**:\n\n• **Formato profesional**: Estilos de texto, numeración, viñetas\n• **Estructura**: Portada, índice, encabezados, pie de página\n• **Elementos**: Tablas, imágenes, gráficos, hipervínculos\n• **Revisión**: Ortografía, gramática, diseño coherente\n\n¿Necesitas ayuda con alguna función específica de Word?"
    
    if any(palabra in pregunta_lower for palabra in ['excel', 'hoja de cálculo', 'fórmula', 'tabla', 'gráfico']):
        return "📊 **Microsoft Excel - Poder en datos**:\n\n• **Fórmulas básicas**: SUMA, PROMEDIO, CONTAR, SI\n• **Formato**: Celdas, bordes, colores condicionales\n• **Gráficos**: Barras, líneas, tortas para visualizar datos\n• **Organización**: Filtros, ordenamiento, tablas dinámicas\n\n¿Qué te gustaría aprender de Excel?"
    
    if any(palabra in pregunta_lower for palabra in ['powerpoint', 'presentación', 'diapositiva', 'slides']):
        return "🎯 **Microsoft PowerPoint - Presentaciones impactantes**:\n\n• **Estructura**: Portada, introducción, desarrollo, conclusión\n• **Diseño**: Plantillas profesionales, colores, fuentes\n• **Animaciones**: Transiciones sutiles, efectos de entrada\n• **Consejo**: Menos texto, más imágenes. Máximo 6 líneas por diapositiva\n\n¿Preparando una presentación?"
    
    # COMUNICACIÓN DIGITAL
    if any(palabra in pregunta_lower for palabra in ['email', 'correo', 'comunicación', 'redacción', 'profesional']):
        return "📧 **Comunicación Digital Efectiva**:\n\n• **Asunto**: Claro y específico (ej: 'Informe mensual - Abril 2024')\n• **Saludo**: Formal ('Estimado Sr./Sra.')\n• **Cuerpo**: Párrafos cortos, ideas claras, propósito evidente\n• **Despedida**: Cortés ('Quedo atento a sus comentarios')\n• **Firma**: Nombre, cargo, contacto\n\n¿Tienes dudas sobre cómo redactar algún tipo de comunicación?"
    
    # ===== 8. MOTIVACIÓN Y APRENDIZAJE =====
    if any(palabra in pregunta_lower for palabra in ['difícil', 'complicado', 'no entiendo', 'no puedo', 'frustrado']):
        return "😊 **¡Tranquilo/a! El aprendizaje es un proceso**:\n\n• **Paso a paso**: No intentes aprender todo de una vez\n• **Practica**: La repetición consolida el conocimiento\n• **Descansa**: Tomar pausas mejora la retención\n• **Pide ayuda**: Yo estoy aquí para apoyarte\n\n¿Qué tema específico se te está haciendo difícil?"
    
    if any(palabra in pregunta_lower for palabra in ['consejo', 'tip', 'recomienda', 'sugerencia', 'truco']):
        return "💡 **Consejos para aprender mejor**:\n\n1. **Establece metas pequeñas** (ej: 'hoy estudio 30 minutos')\n2. **Practica regularmente** (mejor 15 min diarios que 2 horas semanales)\n3. **Enseña a otros** (explicar consolida tu aprendizaje)\n4. **Toma notas** a mano (mejora la retención)\n5. **Relaciona con tu trabajo** (hazlo práctico y relevante)\n\n¿Necesitas algún consejo específico?"
    
    # ===== 9. PREGUNTAS SOBRE EL TUTOR IA =====
    if any(palabra in pregunta_lower for palabra in ['quién eres', 'qué eres', 'tutor', 'ia', 'inteligencia artificial']):
        return "🤖 **Soy tu Tutor IA**:\n\n• **Mi propósito**: Ayudarte en tu proceso de aprendizaje\n• **Puedo**: Explicar temas, revisar tu progreso, dar consejos\n• **No puedo**: Hacer los diagnósticos por ti (esa parte te toca 😉)\n• **Mi conocimiento**: Competencias digitales, ofimática, seguridad\n\n¿En qué más puedo asistirte?"
    
    # ===== 10. RESPUESTA POR DEFECTO INTELIGENTE =====
    sugerencias = [
        "Puedo explicarte temas de: Seguridad digital, Word, Excel, PowerPoint o Comunicación profesional",
        "¿Quieres saber tu progreso actual o áreas que necesitas mejorar?",
        "¿Necesitas consejos para aprender mejor o preparar una presentación?",
        "Puedo ayudarte con: resultados de diagnósticos, módulos completados, o cómo usar la plataforma",
        "¿Tienes dudas sobre contraseñas seguras, redacción de emails o uso de Excel?"
    ]
    
    import random
    return f"🤔 **No estoy seguro de entenderte completamente.**\n\n{random.choice(sugerencias)}\n\n¿Puedes reformular tu pregunta o elegir alguna de estas opciones?"


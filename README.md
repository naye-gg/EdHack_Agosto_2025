# 🎯 PresentAI - EdHack Agosto 2025

## 📖 Descripción del Proyecto

**PresentAI** es una aplicación web inteligente diseñada para ayudar a estudiantes de instituciones educativas a mejorar sus habilidades de presentación en proyectos académicos. Mediante el análisis automatizado de videos, la aplicación proporciona feedback detallado para preparar mejor a los estudiantes para concursos regionales y presentaciones académicas.

## 🎯 Contexto del Problema

Los estudiantes frecuentemente fallan en concursos regionales debido a la falta de preparación en comunicación efectiva. Las principales deficiencias se presentan en:

- **Comunicación verbal**: Falta de claridad, uso excesivo de muletillas, problemas de entonación
- **Lenguaje corporal**: Postura inadecuada, gestos inapropiados, movimientos nerviosos  
- **Presencia escénica**: Falta de contacto visual, expresiones faciales que denotan nerviosismo

PresentAI busca solucionar estos problemas mediante análisis automatizado con retroalimentación constructiva y seguimiento del progreso.

## ✨ Características Principales

### 🎥 Análisis Integral de Presentaciones
- **Subida de videos**: Permite a los estudiantes cargar videos de sus ensayos en formato MP4
- **Análisis multimodal**: Evaluación simultánea de voz, lenguaje corporal y expresiones faciales
- **Feedback inmediato**: Resultados detallados categorizados por área de mejora

### 📊 Tres Dimensiones de Evaluación

#### 🗣️ **Voz y Prosodia**
- Análisis de claridad del habla
- Detección de muletillas ("eh", "este", "pues", etc.)
- Evaluación de tono y entonación
- Ritmo y pausas en el discurso

#### 🕴️ **Lenguaje Corporal**
- Análisis de postura corporal
- Evaluación de gestos y movimientos
- Detección de movimientos nerviosos o repetitivos
- Uso del espacio escénico

#### 😃 **Expresiones Faciales**
- Análisis de contacto visual con la audiencia
- Detección de confianza vs. nerviosismo
- Evaluación de expresiones faciales apropiadas
- Coherencia entre mensaje y expresión

### 📈 Seguimiento de Progreso
- **Historial de presentaciones**: Registro de todas las evaluaciones anteriores
- **Gráficos de progreso**: Visualización del mejoramiento en cada dimensión
- **Diagramas temporales**: Análisis de emociones a lo largo de la presentación
- **Métricas de evolución**: Comparación entre presentaciones pasadas y actuales

## 🛠️ Especificaciones Técnicas

### Entorno de Desarrollo
- **Plataforma**: Replit
- **Framework**: Streamlit (Python)
- **Formato de videos**: MP4

### Librerías Requeridas
```python
streamlit          # Interfaz web
opencv-python      # Procesamiento de video
mediapipe         # Análisis de lenguaje corporal
matplotlib        # Gráficos y visualizaciones
numpy             # Procesamiento numérico
whisper           # Transcripción de voz
```

### Arquitectura de la Aplicación

#### Interfaz de Usuario
- **Página principal**: Botón de carga de videos intuitivo
- **Panel de resultados**: Organizado en pestañas para fácil navegación
  - 📝 **Pestaña Texto**: Feedback detallado por categoría
  - 📊 **Pestaña Gráficos**: Progreso histórico en puntajes
  - 📈 **Pestaña Diagramas**: Flujo temporal de análisis

#### Motor de Análisis
- **Módulo de Voz**: Whisper AI para transcripción y análisis prosódico
- **Módulo Corporal**: MediaPipe Pose para evaluación postural
- **Módulo Facial**: OpenCV + Emotion Recognition para análisis emocional

## 📋 Funcionalidades del Prototipo

### 🔄 Flujo de Trabajo
1. **Carga de Video**: El estudiante sube su video de presentación
2. **Procesamiento**: La IA analiza las tres dimensiones simultáneamente
3. **Generación de Feedback**: Creación de reportes detallados por área
4. **Visualización de Resultados**: Presentación de datos en formato amigable
5. **Almacenamiento**: Guardado del progreso para comparaciones futuras

### 📊 Tipos de Visualización

#### Gráficos de Progreso
- Gráfico de barras comparativo por dimensión
- Línea de tendencia histórica
- Radar chart de habilidades

#### Diagramas Temporales
- Gráfico de línea de emociones durante la presentación
- Mapa de calor de intensidad emocional
- Timeline de momentos críticos

### 🎯 Métricas de Evaluación

#### Voz y Prosodia (0-100)
- Claridad del habla
- Frecuencia de muletillas
- Variación tonal
- Ritmo apropiado

#### Lenguaje Corporal (0-100)
- Postura correcta
- Gesticulación apropiada
- Uso del espacio
- Movimientos seguros

#### Expresiones Faciales (0-100)
- Contacto visual
- Confianza percibida
- Expresiones apropiadas
- Coherencia emocional

## 🎨 Experiencia de Usuario

### Interfaz Intuitiva
- Diseño minimalista y profesional
- Navegación clara entre secciones
- Visualizaciones interactivas
- Responsive design para diferentes dispositivos

### Feedback Constructivo
- Comentarios específicos y accionables
- Sugerencias de mejora personalizadas
- Ejemplos de buenas prácticas
- Recursos adicionales de aprendizaje

## 🚀 Objetivos del Prototipo

### Inmediatos
- [ ] Interfaz funcional de carga de videos
- [ ] Análisis básico de las tres dimensiones
- [ ] Generación de feedback textual
- [ ] Visualización simple de resultados

### A Medio Plazo
- [ ] Perfeccionamiento de algoritmos de análisis
- [ ] Implementación de gráficos interactivos
- [ ] Sistema de almacenamiento de progreso
- [ ] Personalización de feedback

### A Largo Plazo
- [ ] Integración con plataformas educativas
- [ ] Análisis colaborativo de presentaciones grupales
- [ ] Gamificación del proceso de aprendizaje
- [ ] Exportación de reportes detallados

## 🎓 Impacto Educativo

PresentAI está diseñado para:
- **Democratizar** el acceso a entrenamiento de presentaciones
- **Personalizar** el aprendizaje según las necesidades individuales
- **Motivar** la mejora continua a través del seguimiento del progreso
- **Preparar** efectivamente a los estudiantes para competencias académicas

---

*Proyecto desarrollado para EdHack Agosto 2025 - Transformando la educación a través de la inteligencia artificial*
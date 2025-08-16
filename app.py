import streamlit as st
import os
import tempfile
import json
from datetime import datetime
import pandas as pd

# Import analysis modules
from analysis.voice_analyzer import VoiceAnalyzer
from analysis.body_language_analyzer import BodyLanguageAnalyzer
from analysis.facial_analyzer import FacialAnalyzer
from utils.data_storage import DataStorage
from utils.video_processor import VideoProcessor
from visualization.charts import ChartGenerator

# Configure page
st.set_page_config(
    page_title="PresentAI - Analizador de Habilidades de Presentación",
    page_icon="🎤",
    layout="wide"
)

# Initialize components
@st.cache_resource
def initialize_components():
    return {
        'voice_analyzer': VoiceAnalyzer(),
        'body_analyzer': BodyLanguageAnalyzer(),
        'facial_analyzer': FacialAnalyzer(),
        'data_storage': DataStorage(),
        'video_processor': VideoProcessor(),
        'chart_generator': ChartGenerator()
    }

def main():
    st.title("🎤 PresentAI - Analizador de Habilidades de Presentación")
    st.markdown("### Mejora tus habilidades de presentación con análisis IA")
    
    # Initialize components
    components = initialize_components()
    
    # Sidebar for user identification
    with st.sidebar:
        st.header("👨‍🎓 Información del Usuario")
        student_name = st.text_input("Nombre del estudiante", value="Estudiante")
        presentation_topic = st.text_input("Tema de la presentación", value="Proyecto Académico")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📹 Subir Video de Práctica")
        uploaded_file = st.file_uploader(
            "Selecciona tu video de presentación (MP4)",
            type=['mp4'],
            help="Sube un video de tu práctica de presentación para recibir feedback personalizado"
        )
        
        if uploaded_file is not None:
            # Display video
            st.video(uploaded_file)
            
            # Analyze button
            if st.button("🔍 Analizar Presentación", type="primary"):
                analyze_presentation(uploaded_file, student_name, presentation_topic, components)
    
    with col2:
        st.header("📊 Progreso Histórico")
        display_historical_progress(student_name, components['data_storage'], components['chart_generator'])

def analyze_presentation(uploaded_file, student_name, topic, components):
    """Analyze the uploaded presentation video"""
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name
        
        # Step 1: Process video
        status_text.text("🎬 Procesando video...")
        progress_bar.progress(10)
        
        video_info = components['video_processor'].process_video(video_path)
        if not video_info['success']:
            st.error(f"Error procesando video: {video_info['error']}")
            return
        
        # Step 2: Voice analysis
        status_text.text("🗣️ Analizando voz y prosodia...")
        progress_bar.progress(30)
        
        voice_results = components['voice_analyzer'].analyze(video_path)
        
        # Step 3: Body language analysis
        status_text.text("🕴️ Analizando lenguaje corporal...")
        progress_bar.progress(60)
        
        body_results = components['body_analyzer'].analyze(video_path)
        
        # Step 4: Facial expression analysis
        status_text.text("😊 Analizando expresiones faciales...")
        progress_bar.progress(80)
        
        facial_results = components['facial_analyzer'].analyze(video_path)
        
        # Step 5: Compile results
        status_text.text("📊 Compilando resultados...")
        progress_bar.progress(90)
        
        # Combine all results
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'student_name': student_name,
            'topic': topic,
            'video_duration': video_info['duration'],
            'voice_analysis': voice_results,
            'body_analysis': body_results,
            'facial_analysis': facial_results,
            'overall_score': calculate_overall_score(voice_results, body_results, facial_results)
        }
        
        # Save results
        components['data_storage'].save_analysis(student_name, analysis_results)
        
        # Display results
        progress_bar.progress(100)
        status_text.text("✅ ¡Análisis completado!")
        
        display_analysis_results(analysis_results, components['chart_generator'])
        
        # Clean up
        os.unlink(video_path)
        
    except Exception as e:
        st.error(f"Error durante el análisis: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def calculate_overall_score(voice_results, body_results, facial_results):
    """Calculate overall presentation score"""
    voice_score = voice_results.get('score', 0)
    body_score = body_results.get('score', 0)
    facial_score = facial_results.get('score', 0)
    
    # Weighted average (voice 40%, body 35%, facial 25%)
    overall = (voice_score * 0.4) + (body_score * 0.35) + (facial_score * 0.25)
    return round(overall, 1)

def display_analysis_results(results, chart_generator):
    """Display analysis results in tabbed interface"""
    
    st.header("📋 Resultados del Análisis")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📝 Feedback Detallado", "📊 Gráficos", "📈 Diagramas"])
    
    with tab1:
        display_detailed_feedback(results)
    
    with tab2:
        display_graphics(results, chart_generator)
    
    with tab3:
        display_diagrams(results, chart_generator)

def display_detailed_feedback(results):
    """Display detailed text feedback"""
    
    # Overall score
    overall_score = results['overall_score']
    score_color = "green" if overall_score >= 7 else "orange" if overall_score >= 5 else "red"
    
    st.markdown(f"### Puntuación General: :{score_color}[{overall_score}/10]")
    
    # Voice feedback
    st.subheader("🗣️ Análisis de Voz y Prosodia")
    voice_analysis = results['voice_analysis']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Puntuación de Voz", f"{voice_analysis['score']}/10")
        st.metric("Claridad", f"{voice_analysis['clarity_score']}/10")
    with col2:
        st.metric("Velocidad (ppm)", voice_analysis['speaking_rate'])
        st.metric("Muletillas detectadas", voice_analysis['filler_count'])
    
    st.markdown("**Feedback:**")
    for feedback in voice_analysis['feedback']:
        st.write(f"• {feedback}")
    
    # Body language feedback
    st.subheader("🕴️ Análisis de Lenguaje Corporal")
    body_analysis = results['body_analysis']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Puntuación Corporal", f"{body_analysis['score']}/10")
        st.metric("Estabilidad de Postura", f"{body_analysis['posture_stability']}/10")
    with col2:
        st.metric("Gestos Detectados", body_analysis['gesture_count'])
        st.metric("Movimiento General", f"{body_analysis['movement_score']}/10")
    
    st.markdown("**Feedback:**")
    for feedback in body_analysis['feedback']:
        st.write(f"• {feedback}")
    
    # Facial expression feedback
    st.subheader("😊 Análisis de Expresiones Faciales")
    facial_analysis = results['facial_analysis']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Puntuación Facial", f"{facial_analysis['score']}/10")
        st.metric("Contacto Visual", f"{facial_analysis['eye_contact_score']}/10")
    with col2:
        st.metric("Confianza Promedio", f"{facial_analysis['confidence_score']}/10")
        st.metric("Sonrisas Detectadas", facial_analysis['smile_count'])
    
    st.markdown("**Feedback:**")
    for feedback in facial_analysis['feedback']:
        st.write(f"• {feedback}")

def display_graphics(results, chart_generator):
    """Display graphical analysis"""
    
    # Current session scores
    scores = {
        'Voz': results['voice_analysis']['score'],
        'Lenguaje Corporal': results['body_analysis']['score'],
        'Expresiones Faciales': results['facial_analysis']['score'],
        'Puntuación General': results['overall_score']
    }
    
    st.subheader("📊 Puntuaciones de la Sesión Actual")
    fig_current = chart_generator.create_score_bar_chart(scores)
    st.pyplot(fig_current)
    
    # Detailed metrics
    st.subheader("📈 Métricas Detalladas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Voice metrics pie chart
        voice_metrics = {
            'Claridad': results['voice_analysis']['clarity_score'],
            'Velocidad': min(10, results['voice_analysis']['speaking_rate'] / 20),  # Normalize
            'Sin Muletillas': max(0, 10 - results['voice_analysis']['filler_count'])
        }
        fig_voice = chart_generator.create_metrics_pie_chart(voice_metrics, "Métricas de Voz")
        st.pyplot(fig_voice)
    
    with col2:
        # Body language metrics
        body_metrics = {
            'Postura': results['body_analysis']['posture_stability'],
            'Movimiento': results['body_analysis']['movement_score'],
            'Gestos': min(10, results['body_analysis']['gesture_count'])
        }
        fig_body = chart_generator.create_metrics_pie_chart(body_metrics, "Métricas Corporales")
        st.pyplot(fig_body)

def display_diagrams(results, chart_generator):
    """Display temporal diagrams"""
    
    st.subheader("📈 Análisis Temporal")
    
    # Emotion timeline
    if 'emotion_timeline' in results['facial_analysis']:
        fig_emotions = chart_generator.create_emotion_timeline(
            results['facial_analysis']['emotion_timeline']
        )
        st.pyplot(fig_emotions)
    
    # Voice confidence over time
    if 'confidence_timeline' in results['voice_analysis']:
        fig_confidence = chart_generator.create_confidence_timeline(
            results['voice_analysis']['confidence_timeline']
        )
        st.pyplot(fig_confidence)
    
    # Movement activity
    if 'movement_timeline' in results['body_analysis']:
        fig_movement = chart_generator.create_movement_timeline(
            results['body_analysis']['movement_timeline']
        )
        st.pyplot(fig_movement)

def display_historical_progress(student_name, data_storage, chart_generator):
    """Display historical progress for the student"""
    
    history = data_storage.get_student_history(student_name)
    
    if not history:
        st.info("No hay datos históricos disponibles. ¡Sube tu primer video para comenzar!")
        return
    
    # Progress over time
    df = pd.DataFrame(history)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    
    # Recent scores trend
    if len(df) > 1:
        fig_trend = chart_generator.create_progress_trend(df)
        st.pyplot(fig_trend)
    
    # Statistics
    st.subheader("📊 Estadísticas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total de Análisis", len(history))
        if len(history) > 0:
            latest_score = history[-1]['overall_score']
            st.metric("Última Puntuación", f"{latest_score}/10")
    
    with col2:
        if len(history) > 1:
            avg_score = sum(h['overall_score'] for h in history) / len(history)
            st.metric("Promedio General", f"{avg_score:.1f}/10")
            
            # Improvement calculation
            recent_avg = sum(h['overall_score'] for h in history[-3:]) / min(3, len(history))
            older_avg = sum(h['overall_score'] for h in history[:-3]) / max(1, len(history) - 3)
            improvement = recent_avg - older_avg if len(history) > 3 else 0
            
            st.metric("Mejora Reciente", f"{improvement:+.1f}", delta=f"{improvement:+.1f}")

if __name__ == "__main__":
    main()

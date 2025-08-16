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
from analysis.content_analyzer import ContentAnalyzer
from utils.data_storage import DataStorage
from utils.video_processor import VideoProcessor
from utils.report_generator import ReportGenerator
from visualization.charts import ChartGenerator
from auth.user_manager import UserManager
from config.languages import get_text, get_available_languages

# Configure page
st.set_page_config(
    page_title="Coach AI - Análisis de Presentaciones",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .analysis-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }
    
    .analysis-card:hover {
        transform: translateY(-5px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Navigation styling */
    .nav-container {
        background: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Progress styling */
    .progress-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    
    /* Hide unnecessary elements */
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    
    /* Score styling */
    .score-excellent { color: #28a745; font-weight: bold; }
    .score-good { color: #17a2b8; font-weight: bold; }
    .score-average { color: #ffc107; font-weight: bold; }
    .score-poor { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize language
if 'language' not in st.session_state:
    st.session_state.language = 'es'

# Initialize components
@st.cache_resource
def initialize_components():
    return {
        'voice_analyzer': VoiceAnalyzer(),
        'body_analyzer': BodyLanguageAnalyzer(),
        'facial_analyzer': FacialAnalyzer(),
        'content_analyzer': ContentAnalyzer(),
        'data_storage': DataStorage(),
        'video_processor': VideoProcessor(),
        'chart_generator': ChartGenerator(),
        'report_generator': ReportGenerator(),
        'user_manager': UserManager()
    }

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'language' not in st.session_state:
        st.session_state.language = 'es'
    if 'model_version' not in st.session_state:
        st.session_state.model_version = 'basic'

def main():
    """Main application function with modern interface"""
    
    # Initialize session state and components
    initialize_session_state()
    components = initialize_components()
    
    # Check authentication
    if not st.session_state.authenticated:
        show_modern_auth_interface(components['user_manager'])
        return
    
    # Show main application
    show_modern_main_interface(components)

def show_modern_auth_interface(user_manager):
    """Show modern authentication interface"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🎯 Coach AI</div>
        <div class="header-subtitle">Sistema Inteligente de Análisis de Presentaciones</div>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            Mejora tus habilidades de presentación con análisis de IA en tiempo real
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the authentication form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Authentication tabs with modern styling
        tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "📝 Registro"])
        
        with tab1:
            show_modern_login_form(user_manager)
        
        with tab2:
            show_modern_register_form(user_manager)

def show_modern_login_form(user_manager):
    """Show modern login form"""
    
    st.markdown("""
    
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
        password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingresa tu contraseña")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_button = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
        
        if login_button:
            if username and password:
                result = user_manager.authenticate(username, password)
                
                if result["success"]:
                    st.session_state.authenticated = True
                    st.session_state.user = result["user"]
                    
                    # Load user settings
                    settings = result["user"].get("settings", {})
                    st.session_state.language = settings.get("language", "es")
                    
                    st.success("✅ ¡Inicio de sesión exitoso!")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning("⚠️ Por favor completa todos los campos")

def show_modern_register_form(user_manager):
    """Show modern registration form"""
    
    st.markdown("""
    <div class="analysis-card">
        <h3 style="text-align: center; margin-bottom: 2rem;">Crear Nueva Cuenta</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form", clear_on_submit=True):
        username = st.text_input("👤 Usuario", placeholder="Elige un nombre de usuario")
        password = st.text_input("🔒 Contraseña", type="password", placeholder="Crea una contraseña segura")
        full_name = st.text_input("🏷️ Nombre Completo", placeholder="Tu nombre completo")
        institution = st.text_input("🏫 Institución", placeholder="Nombre de tu institución (opcional)")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            register_button = st.form_submit_button("✨ Crear Cuenta", use_container_width=True)
        
        if register_button:
            if username and password and full_name:
                result = user_manager.register_teacher(username, password, full_name, institution)
                
                if result["success"]:
                    st.success("✅ ¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.")
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning("⚠️ Por favor completa todos los campos obligatorios")

def show_modern_main_interface(components):
    """Show modern main application interface"""
    
    user = st.session_state.user
    
    # Modern header with user info
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="header-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0;">👋 Hola, {user['full_name']}</h2>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">
                        {user.get('institution', 'Coach AI Dashboard')}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Cerrar Sesión", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Navigation with modern tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard", 
        "🎥 Análisis de Video", 
        "👥 Estudiantes", 
        "📄 Reportes"
    ])
    
    with tab1:
        show_modern_dashboard(components, user)
    
    with tab2:
        show_modern_analysis_interface(components, user)
    
    with tab3:
        show_modern_student_management(components, user)
    
    with tab4:
        show_modern_reports_interface(components, user)

def show_modern_dashboard(components, user):
    """Show modern teacher dashboard"""
    
    st.markdown("## 📊 Panel de Control")
    
    # Get teacher statistics
    stats = components['user_manager'].get_teacher_stats(user['username'])
    
    if stats:
        # Statistics cards with modern design
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea; margin-bottom: 0.5rem;">👥 Estudiantes</h3>
                <h2 style="margin: 0; color: #333;">{stats['total_students']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: #666;">Total registrados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #28a745; margin-bottom: 0.5rem;">✅ Activos</h3>
                <h2 style="margin: 0; color: #333;">{stats['active_students']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: #666;">Este mes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #17a2b8; margin-bottom: 0.5rem;">🎥 Análisis</h3>
                <h2 style="margin: 0; color: #333;">{stats['total_analyses']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: #666;">Videos analizados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if stats['total_analyses'] > 0:
                avg_score = stats.get('average_score', 0)
                score_color = "#28a745" if avg_score >= 7 else "#ffc107" if avg_score >= 5 else "#dc3545"
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: {score_color}; margin-bottom: 0.5rem;">📈 Promedio</h3>
                    <h2 style="margin: 0; color: #333;">{avg_score:.1f}/10</h2>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">Clase general</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #6c757d; margin-bottom: 0.5rem;">📈 Promedio</h3>
                    <h2 style="margin: 0; color: #333;">--</h2>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">Sin datos</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent activity
        if stats.get('recent_activity'):
            st.markdown("### 📋 Actividad Reciente")
            
            activity_data = []
            for activity in stats['recent_activity']:
                score = activity.get('score', 0)
                score_class = 'excellent' if score >= 8 else 'good' if score >= 6.5 else 'average' if score >= 5 else 'poor'
                
                activity_data.append({
                    "👤 Estudiante": activity['student_id'],
                    "📅 Fecha": activity['timestamp'][:10],
                    "⭐ Puntuación": f"{score}/10"
                })
            
            df = pd.DataFrame(activity_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="analysis-card">
            <div style="text-align: center; padding: 2rem;">
                <h3>🚀 ¡Comienza tu primera clase!</h3>
                <p>Registra estudiantes y comienza a analizar presentaciones</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_modern_analysis_interface(components, user):
    """Show modern video analysis interface"""
    
    st.markdown("## 🎥 Análisis de Presentaciones")
    
    # Student selection
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if not students:
        st.markdown("""
        <div class="analysis-card">
            <div style="text-align: center; padding: 3rem;">
                <h3>👥 No hay estudiantes registrados</h3>
                <p>Ve a la pestaña "Estudiantes" para registrar tu primer estudiante</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Modern student selector
    st.markdown("### 👤 Seleccionar Estudiante")
    student_options = [f"{s['anonymous_id']} - {s['name']}" for s in students]
    selected_student_idx = st.selectbox(
        "Estudiante:",
        range(len(students)),
        format_func=lambda x: student_options[x],
        label_visibility="collapsed"
    )
    
    selected_student = students[selected_student_idx]
    
    # Two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <h3 style="margin-bottom: 1.5rem;">📁 Subir Video de Presentación</h3>
            <p style="margin-bottom: 1rem; color: #666;">
                Analizando para: <strong>{selected_student['anonymous_id']}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Video upload with modern styling
        uploaded_file = st.file_uploader(
            "Selecciona un video:",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Formatos soportados: MP4, AVI, MOV, MKV (Max: 300MB)",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Show video preview
            st.video(uploaded_file)
            
            # Analysis button with modern styling
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("🚀 Analizar Presentación", type="primary", use_container_width=True):
                    analyze_presentation_modern(
                        uploaded_file, selected_student, components, user
                    )
    
    with col2:
        st.markdown("### 📊 Progreso del Estudiante")
        display_student_progress_modern(selected_student, components)

def show_modern_student_management(components, user):
    """Show modern student management interface"""
    
    st.markdown("## 👥 Gestión de Estudiantes")
    
    # Register new student with modern card
    st.markdown("""
    <div class="analysis-card">
        <h3 style="margin-bottom: 1.5rem;">✨ Registrar Nuevo Estudiante</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            dni = st.text_input("🆔 DNI/ID del Estudiante", placeholder="Ingresa el identificador único")
        
        with col2:
            name = st.text_input("👤 Nombre del Estudiante", placeholder="Nombre completo (opcional)")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            register_button = st.form_submit_button("➕ Registrar Estudiante", use_container_width=True)
        
        if register_button:
            if dni:
                result = components['user_manager'].register_student(
                    user['username'], dni, name
                )
                
                if result["success"]:
                    st.success(f"✅ Estudiante registrado exitosamente - ID: {result['anonymous_id']}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning("⚠️ El DNI/ID es obligatorio")
    
    # Display existing students
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if students:
        st.markdown("### 📋 Estudiantes Registrados")
        
        # Create modern table display
        student_data = []
        for student in students:
            student_data.append({
                "🏷️ ID Anónimo": student['anonymous_id'],
                "👤 Nombre": student.get('name', 'Sin nombre'),
                "📅 Fecha de Registro": student['registered_at'][:10],
                "📊 Sesiones": student.get('total_sessions', 0)
            })
        
        df = pd.DataFrame(student_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="analysis-card">
            <div style="text-align: center; padding: 2rem;">
                <h4>📝 No hay estudiantes registrados</h4>
                <p>Registra tu primer estudiante usando el formulario de arriba</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_modern_reports_interface(components, user):
    """Show modern reports interface"""
    
    st.markdown("## 📄 Generación de Reportes")
    
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if not students:
        st.markdown("""
        <div class="analysis-card">
            <div style="text-align: center; padding: 3rem;">
                <h3>👥 No hay estudiantes para reportes</h3>
                <p>Registra estudiantes y realiza análisis para generar reportes</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Report type selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="analysis-card">
            <h3 style="margin-bottom: 1.5rem;">👤 Reporte Individual</h3>
            <p>Genera un reporte detallado para un estudiante específico</p>
        </div>
        """, unsafe_allow_html=True)
        
        student_options = [f"{s['anonymous_id']} - {s.get('name', 'Sin nombre')}" for s in students]
        selected_idx = st.selectbox(
            "Seleccionar estudiante:",
            range(len(students)),
            format_func=lambda x: student_options[x],
            key="individual_report"
        )
        
        selected_student = students[selected_idx]
        
        if selected_student.get('analyses'):
            col_pdf, col_excel = st.columns(2)
            
            with col_pdf:
                if st.button("📄 Generar PDF", use_container_width=True):
                    generate_individual_report(selected_student, components, "pdf")
            
            with col_excel:
                if st.button("📊 Generar Excel", use_container_width=True):
                    generate_individual_report(selected_student, components, "excel")
        else:
            st.info("⚠️ Este estudiante no tiene análisis disponibles")
    
    with col2:
        st.markdown("""
        <div class="analysis-card">
            <h3 style="margin-bottom: 1.5rem;">👥 Reporte de Clase</h3>
            <p>Genera un reporte consolidado de todos los estudiantes</p>
        </div>
        """, unsafe_allow_html=True)
        
        students_with_data = [s for s in students if s.get('analyses')]
        
        if students_with_data:
            st.info(f"📊 {len(students_with_data)} estudiantes con datos disponibles")
            
            col_pdf2, col_excel2 = st.columns(2)
            
            with col_pdf2:
                if st.button("📄 Reporte PDF", use_container_width=True, key="class_pdf"):
                    generate_class_report(students_with_data, components, user, "pdf")
            
            with col_excel2:
                if st.button("📊 Reporte Excel", use_container_width=True, key="class_excel"):
                    generate_class_report(students_with_data, components, user, "excel")
        else:
            st.info("⚠️ No hay estudiantes con análisis disponibles")
def analyze_presentation_modern(uploaded_file, student, components, user):
    """Modern analysis interface with enhanced UX"""
    
    # Create modern progress container
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown("""
        <div class="progress-container">
            <h3>🔄 Analizando Presentación</h3>
            <p>Procesando tu video con inteligencia artificial...</p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name
        
        # Step 1: Process video
        status_text.text("🎬 Procesando video...")
        progress_bar.progress(20)
        
        video_info = components['video_processor'].process_video(video_path)
        if not video_info['success']:
            st.error(f"❌ Error procesando video: {video_info['error']}")
            return
        
        # Step 2: Voice analysis
        status_text.text("🗣️ Analizando voz y prosodia...")
        progress_bar.progress(40)
        
        voice_results = components['voice_analyzer'].analyze(video_path)
        
        # Step 3: Body language analysis
        status_text.text("🕴️ Analizando lenguaje corporal...")
        progress_bar.progress(70)
        
        body_results = components['body_analyzer'].analyze(video_path)
        
        # Step 4: Facial expression analysis
        status_text.text("😊 Analizando expresiones faciales...")
        progress_bar.progress(90)
        
        facial_results = components['facial_analyzer'].analyze(video_path)
        
        # Step 5: Compile results
        status_text.text("📊 Compilando resultados...")
        progress_bar.progress(100)
        
        # Combine all results
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'student_id': student['anonymous_id'],
            'student_dni': student['dni'],
            'video_duration': video_info['duration'],
            'voice_analysis': voice_results,
            'body_analysis': body_results,
            'facial_analysis': facial_results,
            'overall_score': calculate_overall_score(voice_results, body_results, facial_results)
        }
        
        # Save results
        components['user_manager'].add_student_analysis(
            user['username'], 
            student['dni'], 
            analysis_results
        )
        
        # Clear progress and show results
        progress_container.empty()
        
        st.success("✅ ¡Análisis completado exitosamente!")
        display_modern_results(analysis_results, components)
        
        # Clean up
        os.unlink(video_path)
        
    except Exception as e:
        progress_container.empty()
        st.error(f"❌ Error durante el análisis: {str(e)}")

def display_student_progress_modern(student, components):
    """Display modern student progress"""
    
    if not student.get('analyses'):
        st.markdown("""
        <div class="analysis-card">
            <div style="text-align: center; padding: 2rem;">
                <h4>📊 Sin datos históricos</h4>
                <p>Los gráficos de progreso aparecerán después del primer análisis</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Student statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">📊 Análisis</h4>
            <h3 style="margin: 0; color: #333;">{student.get('total_sessions', 0)}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if student['analyses']:
            last_score = student['analyses'][-1]['data']['overall_score']
            score_color = "#28a745" if last_score >= 7 else "#ffc107" if last_score >= 5 else "#dc3545"
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {score_color}; margin-bottom: 0.5rem;">⭐ Última</h4>
                <h3 style="margin: 0; color: #333;">{last_score}/10</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Progress trend
    if len(student['analyses']) > 1:
        scores = [analysis['data']['overall_score'] for analysis in student['analyses']]
        dates = [analysis['timestamp'][:10] for analysis in student['analyses']]
        
        progress_data = pd.DataFrame({
            'Fecha': dates,
            'Puntuación': scores
        })
        
        st.markdown("#### 📈 Tendencia")
        st.line_chart(progress_data.set_index('Fecha'), height=200)

def generate_individual_report(student, components, report_type):
    """Generate individual student report"""
    try:
        if report_type == "pdf":
            latest_analysis = student['analyses'][-1]['data']
            pdf_path = components['report_generator'].generate_individual_pdf_report(
                student, latest_analysis, 'es'
            )
            
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    st.download_button(
                        "📥 Descargar PDF",
                        f.read(),
                        file_name=f"reporte_{student['anonymous_id']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.success("✅ Reporte PDF generado exitosamente")
            else:
                st.error("❌ Error generando el reporte PDF")
        
        elif report_type == "excel":
            excel_path = components['report_generator'].generate_class_excel_report(
                {'username': 'teacher'}, [student], 'es'
            )
            
            if excel_path and os.path.exists(excel_path):
                with open(excel_path, 'rb') as f:
                    st.download_button(
                        "📥 Descargar Excel",
                        f.read(),
                        file_name=f"reporte_{student['anonymous_id']}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                st.success("✅ Reporte Excel generado exitosamente")
            else:
                st.error("❌ Error generando el reporte Excel")
                
    except Exception as e:
        st.error(f"❌ Error generando el reporte: {str(e)}")

def generate_class_report(students, components, user, report_type):
    """Generate class report"""
    try:
        if report_type == "pdf":
            pdf_path = components['report_generator'].generate_class_pdf_report(
                user, students, 'es'
            )
            
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    st.download_button(
                        "📥 Descargar PDF de Clase",
                        f.read(),
                        file_name="reporte_clase.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.success("✅ Reporte de clase PDF generado exitosamente")
            else:
                st.error("❌ Error generando el reporte PDF de clase")
        
        elif report_type == "excel":
            excel_path = components['report_generator'].generate_class_excel_report(
                user, students, 'es'
            )
            
            if excel_path and os.path.exists(excel_path):
                with open(excel_path, 'rb') as f:
                    st.download_button(
                        "📥 Descargar Excel de Clase",
                        f.read(),
                        file_name="reporte_clase.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                st.success("✅ Reporte de clase Excel generado exitosamente")
            else:
                st.error("❌ Error generando el reporte Excel de clase")
                
    except Exception as e:
        st.error(f"❌ Error generando el reporte de clase: {str(e)}")

def display_modern_results(results, components):
    """Display analysis results with modern interface"""
    
    # Overall score card
    overall_score = results['overall_score']
    score_color = "#28a745" if overall_score >= 7 else "#ffc107" if overall_score >= 5 else "#dc3545"
    
    st.markdown(f"""
    <div class="analysis-card">
        <div style="text-align: center;">
            <h2 style="color: {score_color}; margin-bottom: 1rem;">
                🏆 Puntuación General: {overall_score}/10
            </h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗣️ Voz", "🕴️ Lenguaje Corporal", "😊 Expresión Facial", "📊 Gráficos"])
    
    with tab1:
        display_voice_results_modern(results['voice_analysis'])
    
    with tab2:
        display_body_results_modern(results['body_analysis'])
    
    with tab3:
        display_facial_results_modern(results['facial_analysis'])
    
    with tab4:
        display_charts_modern(results, components)

def display_voice_results_modern(voice_analysis):
    """Display voice analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = voice_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color};">🗣️ Puntuación Vocal</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        clarity = voice_analysis.get('clarity_score', 0)
        clarity_color = "#28a745" if clarity >= 7 else "#ffc107" if clarity >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {clarity_color};">🎯 Claridad</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{clarity}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rate = voice_analysis.get('speaking_rate', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8;">⚡ Velocidad</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{rate} ppm</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown("#### 💬 Retroalimentación")
    for feedback in voice_analysis.get('feedback', []):
        st.write(f"• {feedback}")

def display_body_results_modern(body_analysis):
    """Display body language analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = body_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color};">🕴️ Puntuación Corporal</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        posture = body_analysis.get('posture_stability', 0)
        posture_color = "#28a745" if posture >= 7 else "#ffc107" if posture >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {posture_color};">🧍 Postura</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{posture}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        gestures = body_analysis.get('gesture_count', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8;">👋 Gestos</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{gestures}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown("#### 💬 Retroalimentación")
    for feedback in body_analysis.get('feedback', []):
        st.write(f"• {feedback}")

def display_facial_results_modern(facial_analysis):
    """Display facial expression analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = facial_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color};">😊 Puntuación Facial</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        eye_contact = facial_analysis.get('eye_contact_score', 0)
        eye_color = "#28a745" if eye_contact >= 7 else "#ffc107" if eye_contact >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {eye_color};">👁️ Contacto Visual</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{eye_contact}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        smiles = facial_analysis.get('smile_count', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #28a745;">😄 Sonrisas</h4>
            <h2 style="color: #333; margin: 0.5rem 0;">{smiles}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown("#### 💬 Retroalimentación")
    for feedback in facial_analysis.get('feedback', []):
        st.write(f"• {feedback}")

def display_charts_modern(results, components):
    """Display modern charts"""
    
    # Scores comparison
    scores = {
        'Voz': results['voice_analysis'].get('score', 0),
        'Corporal': results['body_analysis'].get('score', 0),
        'Facial': results['facial_analysis'].get('score', 0)
    }
    
    # Create chart
    try:
        fig = components['chart_generator'].create_score_bar_chart(scores)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generando gráfico: {str(e)}")

def calculate_overall_score(voice_results, body_results, facial_results):
    """Calculate overall presentation score"""
    voice_score = voice_results.get('score', 0)
    body_score = body_results.get('score', 0)
    facial_score = facial_results.get('score', 0)
    
    # Weighted average (voice 40%, body 35%, facial 25%)
    overall = (voice_score * 0.4) + (body_score * 0.35) + (facial_score * 0.25)
    return round(overall, 1)

def show_dashboard(components, lang, user):
    """Show teacher dashboard with class overview"""
    
    st.header(get_text("dashboard", lang))
    
    # Get teacher statistics
    stats = components['user_manager'].get_teacher_stats(user['username'])
    
    if stats:
        # Statistics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                get_text("total_students", lang),
                stats['total_students']
            )
        
        with col2:
            st.metric(
                get_text("active_students", lang),
                stats['active_students']
            )
        
        with col3:
            st.metric(
                get_text("total_analyses", lang),
                stats['total_analyses']
            )
        
        with col4:
            if stats['total_analyses'] > 0:
                avg_score = stats.get('average_score', 0)
                st.metric(
                    get_text("class_average", lang),
                    f"{avg_score:.1f}/10"
                )
        
        # Recent activity
        if stats['recent_activity']:
            st.subheader(get_text("recent_activity", lang))
            
            activity_data = []
            for activity in stats['recent_activity']:
                activity_data.append({
                    get_text("student", lang): activity['student_id'],
                    get_text("date", lang): activity['timestamp'][:10],
                    get_text("score", lang): f"{activity['score']}/10"
                })
            
            df = pd.DataFrame(activity_data)
            st.dataframe(df, use_container_width=True)
    else:
        st.info(get_text("no_data_available", lang))

def show_analysis_interface(components, lang, user):
    """Show video analysis interface"""
    
    st.header(get_text("video_analysis", lang))
    
    # Student selection
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if not students:
        st.warning(get_text("no_students_registered", lang))
        st.info(get_text("register_students_first", lang))
        return
    
    # Student selector
    student_options = [f"{s['anonymous_id']} - {s['name']}" for s in students]
    selected_student_idx = st.selectbox(
        get_text("select_student", lang),
        range(len(students)),
        format_func=lambda x: student_options[x]
    )
    
    selected_student = students[selected_student_idx]
    
    st.subheader(f"{get_text('analyzing_for', lang)}: {selected_student['anonymous_id']}")
    
    # Video upload
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header(get_text("upload_video", lang))
        
        # Adjust max file size based on settings
        max_size_mb = user.get('settings', {}).get('max_video_size_mb', 350)
        
        uploaded_file = st.file_uploader(
            get_text("select_video", lang),
            type=['mp4', 'avi', 'mov', 'mkv'],
            help=f"{get_text('video_help', lang)} (Max: {max_size_mb}MB)"
        )
        
        # Advanced model features
        script_text = None
        rubric_text = None
        
        if st.session_state.model_version == 'advanced':
            st.subheader(get_text("additional_content", lang))
            
            # Script upload/input
            script_option = st.radio(
                get_text("presentation_script", lang),
                [get_text("no_script", lang), get_text("upload_script", lang), get_text("type_script", lang)]
            )
            
            if script_option == get_text("upload_script", lang):
                script_file = st.file_uploader(
                    get_text("upload_script", lang),
                    type=['txt', 'docx'],
                    help=get_text("script_help", lang)
                )
                if script_file:
                    script_text = script_file.read().decode('utf-8')
            
            elif script_option == get_text("type_script", lang):
                script_text = st.text_area(
                    get_text("type_script", lang),
                    height=200,
                    help=get_text("script_help", lang)
                )
            
            # Rubric upload
            rubric_file = st.file_uploader(
                get_text("upload_rubric", lang),
                type=['txt', 'docx'],
                help=get_text("rubric_help", lang)
            )
            if rubric_file:
                rubric_text = rubric_file.read().decode('utf-8')
        
        # Analysis button
        if uploaded_file is not None:
            st.video(uploaded_file)
            
            if st.button(get_text("analyze_presentation", lang), type="primary"):
                analyze_presentation_advanced(
                    uploaded_file, selected_student, components, 
                    script_text, rubric_text, lang, user
                )
    
    with col2:
        st.header(get_text("student_progress", lang))
        display_student_progress(selected_student, components, lang)

def show_student_management(components, lang, user):
    """Show student management interface"""
    
    st.header(get_text("student_management", lang))
    
    # Register new student
    with st.expander(get_text("register_new_student", lang)):
        with st.form("register_student_form"):
            dni = st.text_input(get_text("student_dni", lang))
            name = st.text_input(get_text("student_name", lang))
            
            if st.form_submit_button(get_text("register_student", lang)):
                if dni:
                    result = components['user_manager'].register_student(
                        user['username'], dni, name
                    )
                    
                    if result["success"]:
                        st.success(f"{result['message']} - ID: {result['anonymous_id']}")
                        st.rerun()
                    else:
                        st.error(result["message"])
                else:
                    st.warning(get_text("dni_required", lang))
    
    # Display existing students
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if students:
        st.subheader(get_text("registered_students", lang))
        
        # Create DataFrame for display
        student_data = []
        for student in students:
            student_data.append({
                get_text("anonymous_id", lang): student['anonymous_id'],
                get_text("name", lang): student['name'],
                get_text("registration_date", lang): student['registered_at'][:10],
                get_text("total_sessions", lang): student['total_sessions']
            })
        
        df = pd.DataFrame(student_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info(get_text("no_students_registered", lang))

def show_reports_interface(components, lang, user):
    """Show reports interface"""
    
    st.header(get_text("reports", lang))
    
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if not students:
        st.warning(get_text("no_students_for_reports", lang))
        return
    
    # Report type selection
    report_type = st.radio(
        get_text("report_type", lang),
        [get_text("individual_report", lang), get_text("class_report", lang)]
    )
    
    if report_type == get_text("individual_report", lang):
        # Individual student report
        student_options = [f"{s['anonymous_id']} - {s['name']}" for s in students]
        selected_idx = st.selectbox(
            get_text("select_student", lang),
            range(len(students)),
            format_func=lambda x: student_options[x]
        )
        
        selected_student = students[selected_idx]
        
        if selected_student.get('analyses'):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(get_text("generate_pdf", lang)):
                    latest_analysis = selected_student['analyses'][-1]['data']
                    pdf_path = components['report_generator'].generate_individual_pdf_report(
                        selected_student, latest_analysis, lang
                    )
                    
                    if pdf_path:
                        with open(pdf_path, 'rb') as f:
                            st.download_button(
                                get_text("download_pdf", lang),
                                f.read(),
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf"
                            )
                        st.success(get_text("report_generated", lang))
            
            with col2:
                if st.button(get_text("generate_excel", lang)):
                    excel_path = components['report_generator'].generate_class_excel_report(
                        user, [selected_student], lang
                    )
                    
                    if excel_path:
                        with open(excel_path, 'rb') as f:
                            st.download_button(
                                get_text("download_excel", lang),
                                f.read(),
                                file_name=os.path.basename(excel_path),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.success(get_text("report_generated", lang))
        else:
            st.info(get_text("no_analyses_for_student", lang))
    
    else:
        # Class report
        students_with_data = [s for s in students if s.get('analyses')]
        
        if students_with_data:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(get_text("generate_class_pdf", lang)):
                    pdf_path = components['report_generator'].generate_class_pdf_report(
                        user, students_with_data, lang
                    )
                    
                    if pdf_path:
                        with open(pdf_path, 'rb') as f:
                            st.download_button(
                                get_text("download_pdf", lang),
                                f.read(),
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf"
                            )
                        st.success(get_text("report_generated", lang))
            
            with col2:
                if st.button(get_text("generate_class_excel", lang)):
                    excel_path = components['report_generator'].generate_class_excel_report(
                        user, students_with_data, lang
                    )
                    
                    if excel_path:
                        with open(excel_path, 'rb') as f:
                            st.download_button(
                                get_text("download_excel", lang),
                                f.read(),
                                file_name=os.path.basename(excel_path),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.success(get_text("report_generated", lang))
        else:
            st.info(get_text("no_analyses_for_class", lang))

def show_settings_interface(components, lang, user):
    """Show settings interface"""
    
    st.header(get_text("settings", lang))
    
    with st.form("settings_form"):
        # Video size limit
        max_size = st.number_input(
            get_text("video_size_limit", lang),
            min_value=50,
            max_value=500,
            value=user.get('settings', {}).get('max_video_size_mb', 350),
            step=50
        )
        
        # Institution
        institution = st.text_input(
            get_text("institution", lang),
            value=user.get('institution', '')
        )
        
        if st.form_submit_button(get_text("save_settings", lang)):
            # Update user settings
            result = components['user_manager'].update_user_settings(
                user['username'],
                {
                    'max_video_size_mb': max_size,
                    'institution': institution
                }
            )
            
            if result:
                st.success(get_text("settings_saved", lang))
                st.rerun()
            else:
                st.error(get_text("error_saving_settings", lang))

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

def analyze_presentation_advanced(uploaded_file, selected_student, components, 
                                script_text, rubric_text, lang, user):
    """Advanced analysis with content and rubric evaluation"""
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name
        
        # Step 1: Process video
        status_text.text(get_text("processing_video", lang))
        progress_bar.progress(10)
        
        video_info = components['video_processor'].process_video(video_path)
        if not video_info['success']:
            st.error(f"Error procesando video: {video_info['error']}")
            return
        
        # Step 2: Voice analysis
        status_text.text(get_text("analyzing_voice", lang))
        progress_bar.progress(25)
        
        voice_results = components['voice_analyzer'].analyze(video_path)
        
        # Step 3: Body language analysis
        status_text.text(get_text("analyzing_body", lang))
        progress_bar.progress(45)
        
        body_results = components['body_analyzer'].analyze(video_path)
        
        # Step 4: Facial expression analysis
        status_text.text(get_text("analyzing_facial", lang))
        progress_bar.progress(65)
        
        facial_results = components['facial_analyzer'].analyze(video_path)
        
        # Step 5: Content analysis (Advanced model)
        content_results = None
        rubric_evaluation = None
        
        if st.session_state.model_version == 'advanced':
            if script_text:
                status_text.text(get_text("analyzing_content", lang))
                progress_bar.progress(80)
                
                content_results = components['content_analyzer'].analyze_script(
                    script_text, lang
                )
                
                if rubric_text:
                    rubric_evaluation = components['content_analyzer'].evaluate_with_rubric(
                        content_results, rubric_text
                    )
        
        # Step 6: Compile results
        status_text.text(get_text("compiling_results", lang))
        progress_bar.progress(90)
        
        # Combine all results
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'student_id': selected_student['anonymous_id'],
            'student_dni': selected_student['dni'],
            'video_duration': video_info['duration'],
            'voice_analysis': voice_results,
            'body_analysis': body_results,
            'facial_analysis': facial_results,
            'content_analysis': content_results,
            'rubric_evaluation': rubric_evaluation,
            'model_version': st.session_state.model_version,
            'overall_score': calculate_overall_score_advanced(
                voice_results, body_results, facial_results, content_results
            )
        }
        
        # Save results to user system
        components['user_manager'].add_student_analysis(
            user['username'], 
            selected_student['dni'], 
            analysis_results
        )
        
        # Display results
        progress_bar.progress(100)
        status_text.text(get_text("analysis_complete", lang))
        
        display_analysis_results_advanced(analysis_results, components, lang)
        
        # Clean up
        os.unlink(video_path)
        
    except Exception as e:
        st.error(f"Error durante el análisis: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def calculate_overall_score_advanced(voice_results, body_results, facial_results, content_results):
    """Calculate overall score including content analysis"""
    voice_score = voice_results.get('score', 0)
    body_score = body_results.get('score', 0)
    facial_score = facial_results.get('score', 0)
    
    if content_results:
        content_score = content_results.get('content_score', 0)
        # With content: voice 30%, body 25%, facial 20%, content 25%
        overall = (voice_score * 0.3) + (body_score * 0.25) + (facial_score * 0.2) + (content_score * 0.25)
    else:
        # Without content: voice 40%, body 35%, facial 25%
        overall = (voice_score * 0.4) + (body_score * 0.35) + (facial_score * 0.25)
    
    return round(overall, 1)

def display_analysis_results_advanced(results, components, lang):
    """Display advanced analysis results"""
    
    st.header(get_text("detailed_feedback", lang))
    
    # Create tabs based on model version
    if st.session_state.model_version == 'advanced':
        tabs = st.tabs([
            get_text("voice_analysis", lang),
            get_text("body_analysis", lang), 
            get_text("facial_analysis", lang),
            get_text("content_analysis", lang),
            get_text("charts", lang)
        ])
    else:
        tabs = st.tabs([
            get_text("voice_analysis", lang),
            get_text("body_analysis", lang),
            get_text("facial_analysis", lang),
            get_text("charts", lang)
        ])
    
    # Voice analysis tab
    with tabs[0]:
        display_voice_analysis(results['voice_analysis'], lang)
    
    # Body analysis tab  
    with tabs[1]:
        display_body_analysis(results['body_analysis'], lang)
    
    # Facial analysis tab
    with tabs[2]:
        display_facial_analysis(results['facial_analysis'], lang)
    
    # Content analysis tab (advanced only)
    if st.session_state.model_version == 'advanced' and results.get('content_analysis'):
        with tabs[3]:
            display_content_analysis(results['content_analysis'], results.get('rubric_evaluation'), lang)
        
        # Charts tab
        with tabs[4]:
            display_advanced_charts(results, components['chart_generator'], lang)
    else:
        # Charts tab
        with tabs[3]:
            display_advanced_charts(results, components['chart_generator'], lang)

def display_voice_analysis(voice_analysis, lang):
    """Display voice analysis results"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(get_text("voice_score", lang), f"{voice_analysis.get('score', 0)}/10")
    with col2:
        st.metric(get_text("clarity", lang), f"{voice_analysis.get('clarity_score', 0)}/10")
    with col3:
        st.metric(get_text("speaking_rate", lang), f"{voice_analysis.get('speaking_rate', 0)} ppm")
    
    st.subheader(get_text("detailed_feedback", lang))
    for feedback in voice_analysis.get('feedback', []):
        st.write(f"• {feedback}")

def display_body_analysis(body_analysis, lang):
    """Display body language analysis results"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(get_text("body_score", lang), f"{body_analysis.get('score', 0)}/10")
    with col2:
        st.metric(get_text("posture_stability", lang), f"{body_analysis.get('posture_stability', 0)}/10")
    with col3:
        st.metric(get_text("gestures_detected", lang), body_analysis.get('gesture_count', 0))
    
    st.subheader(get_text("detailed_feedback", lang))
    for feedback in body_analysis.get('feedback', []):
        st.write(f"• {feedback}")

def display_facial_analysis(facial_analysis, lang):
    """Display facial expression analysis results"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(get_text("facial_score", lang), f"{facial_analysis.get('score', 0)}/10")
    with col2:
        st.metric(get_text("eye_contact", lang), f"{facial_analysis.get('eye_contact_score', 0)}/10")
    with col3:
        st.metric(get_text("smiles_detected", lang), facial_analysis.get('smile_count', 0))
    
    st.subheader(get_text("detailed_feedback", lang))
    for feedback in facial_analysis.get('feedback', []):
        st.write(f"• {feedback}")

def display_content_analysis(content_analysis, rubric_evaluation, lang):
    """Display content analysis results"""
    
    if content_analysis:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Puntuación de Contenido", f"{content_analysis.get('content_score', 0)}/10")
        with col2:
            st.metric("Palabras", content_analysis.get('word_count', 0))
        with col3:
            st.metric("Tiempo Estimado", f"{content_analysis.get('detailed_metrics', {}).get('time_estimation', 0)} min")
        
        st.subheader("Estructura de Presentación")
        structure = content_analysis.get('structure_analysis', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"✓ Introducción: {'Sí' if structure.get('has_introduction') else 'No'}")
            st.write(f"✓ Objetivos: {'Sí' if structure.get('has_objectives') else 'No'}")
        with col2:
            st.write(f"✓ Conclusión: {'Sí' if structure.get('has_conclusion') else 'No'}")
            st.write(f"✓ Transiciones: {structure.get('transition_count', 0)}")
        
        st.subheader("Feedback de Contenido")
        for feedback in content_analysis.get('feedback', []):
            st.write(f"• {feedback}")
    
    if rubric_evaluation:
        st.subheader("Evaluación según Rúbrica")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Puntuación Total", f"{rubric_evaluation.get('overall_score', 0)}/{rubric_evaluation.get('max_possible_score', 0)}")
        with col2:
            st.metric("Porcentaje", f"{rubric_evaluation.get('percentage', 0):.1f}%")
        
        st.subheader("Recomendaciones")
        for rec in rubric_evaluation.get('recommendations', []):
            st.write(f"• {rec}")

def display_advanced_charts(results, chart_generator, lang):
    """Display advanced charts and visualizations"""
    
    # Overall scores comparison
    scores = {
        get_text("voice_score", lang): results['voice_analysis'].get('score', 0),
        get_text("body_score", lang): results['body_analysis'].get('score', 0),
        get_text("facial_score", lang): results['facial_analysis'].get('score', 0)
    }
    
    if results.get('content_analysis'):
        scores[get_text("content_score", lang)] = results['content_analysis'].get('content_score', 0)
    
    st.subheader(get_text("overall_score", lang))
    fig = chart_generator.create_score_bar_chart(scores)
    st.pyplot(fig)

def display_student_progress(student, components, lang):
    """Display individual student progress"""
    
    if not student.get('analyses'):
        st.info(get_text("no_historical_data", lang))
        return
    
    # Student statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(get_text("total_analyses", lang), student['total_sessions'])
    
    with col2:
        if student['analyses']:
            last_score = student['analyses'][-1]['data']['overall_score']
            st.metric(get_text("last_score", lang), f"{last_score}/10")
    
    # Progress trend
    if len(student['analyses']) > 1:
        scores = [analysis['data']['overall_score'] for analysis in student['analyses']]
        dates = [analysis['timestamp'][:10] for analysis in student['analyses']]
        
        progress_data = pd.DataFrame({
            'Fecha': dates,
            'Puntuación': scores
        })
        
        st.subheader(get_text("progress_trend", lang))
        st.line_chart(progress_data.set_index('Fecha'))

if __name__ == "__main__":
    main()

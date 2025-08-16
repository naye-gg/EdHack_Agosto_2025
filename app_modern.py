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
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
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
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .analysis-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .analysis-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress styling */
    .progress-container {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(102, 126, 234, 0.05);
        border-radius: 15px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 10px;
        color: #667eea;
        font-weight: 600;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
        .analysis-card {
            padding: 1.5rem;
        }
    }
    
    /* Hide unnecessary elements */
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK, footer, .css-164nlkn {
        display: none;
    }
    
    /* Score styling */
    .score-excellent { color: #28a745; font-weight: bold; }
    .score-good { color: #17a2b8; font-weight: bold; }
    .score-average { color: #ffc107; font-weight: bold; }
    .score-poor { color: #dc3545; font-weight: bold; }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        background: rgba(102, 126, 234, 0.05);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
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
        <p style="font-size: 1.1rem; margin-top: 1rem; opacity: 0.9;">
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
    <div class="analysis-card">
        <h3 style="text-align: center; margin-bottom: 2rem; color: #667eea;">
            Bienvenido de vuelta
        </h3>
    </div>
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
        <h3 style="text-align: center; margin-bottom: 2rem; color: #667eea;">
            Crear Nueva Cuenta
        </h3>
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
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"""
        <div class="header-container">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; font-size: 2rem;">👋 Hola, {user['full_name']}</h2>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 1.1rem;">
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
                <h3 style="color: #667eea; margin-bottom: 0.5rem; font-size: 1rem;">👥 Estudiantes</h3>
                <h2 style="margin: 0; color: #333; font-size: 2.5rem;">{stats['total_students']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">Total registrados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #28a745; margin-bottom: 0.5rem; font-size: 1rem;">✅ Activos</h3>
                <h2 style="margin: 0; color: #333; font-size: 2.5rem;">{stats['active_students']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">Este mes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #17a2b8; margin-bottom: 0.5rem; font-size: 1rem;">🎥 Análisis</h3>
                <h2 style="margin: 0; color: #333; font-size: 2.5rem;">{stats['total_analyses']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">Videos analizados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if stats['total_analyses'] > 0:
                avg_score = stats.get('average_score', 0)
                score_color = "#28a745" if avg_score >= 7 else "#ffc107" if avg_score >= 5 else "#dc3545"
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: {score_color}; margin-bottom: 0.5rem; font-size: 1rem;">📈 Promedio</h3>
                    <h2 style="margin: 0; color: #333; font-size: 2.5rem;">{avg_score:.1f}/10</h2>
                    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">Clase general</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #6c757d; margin-bottom: 0.5rem; font-size: 1rem;">📈 Promedio</h3>
                    <h2 style="margin: 0; color: #333; font-size: 2.5rem;">--</h2>
                    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">Sin datos</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent activity
        if stats.get('recent_activity'):
            st.markdown("### 📋 Actividad Reciente")
            
            activity_data = []
            for activity in stats['recent_activity']:
                score = activity.get('score', 0)
                
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
                <h3 style="color: #667eea;">🚀 ¡Comienza tu primera clase!</h3>
                <p style="color: #666; font-size: 1.1rem;">Registra estudiantes y comienza a analizar presentaciones</p>
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
                <h3 style="color: #667eea;">👥 No hay estudiantes registrados</h3>
                <p style="color: #666; font-size: 1.1rem;">Ve a la pestaña "Estudiantes" para registrar tu primer estudiante</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Modern student selector
    st.markdown("### 👤 Seleccionar Estudiante")
    student_options = [f"{s['anonymous_id']} - {s.get('name', 'Sin nombre')}" for s in students]
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
            <h3 style="margin-bottom: 1.5rem; color: #667eea;">📁 Subir Video de Presentación</h3>
            <p style="margin-bottom: 1rem; color: #666; font-size: 1.1rem;">
                Analizando para: <strong style="color: #667eea;">{selected_student['anonymous_id']}</strong>
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
        <h3 style="margin-bottom: 1.5rem; color: #667eea;">✨ Registrar Nuevo Estudiante</h3>
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
                <h4 style="color: #667eea;">📝 No hay estudiantes registrados</h4>
                <p style="color: #666;">Registra tu primer estudiante usando el formulario de arriba</p>
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
                <h3 style="color: #667eea;">👥 No hay estudiantes para reportes</h3>
                <p style="color: #666; font-size: 1.1rem;">Registra estudiantes y realiza análisis para generar reportes</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Report type selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="analysis-card">
            <h3 style="margin-bottom: 1.5rem; color: #667eea;">👤 Reporte Individual</h3>
            <p style="color: #666;">Genera un reporte detallado para un estudiante específico</p>
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
            <h3 style="margin-bottom: 1.5rem; color: #667eea;">👥 Reporte de Clase</h3>
            <p style="color: #666;">Genera un reporte consolidado de todos los estudiantes</p>
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
            <h3 style="color: #667eea;">🔄 Analizando Presentación</h3>
            <p style="color: #666; font-size: 1.1rem;">Procesando tu video con inteligencia artificial...</p>
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
                <h4 style="color: #667eea;">📊 Sin datos históricos</h4>
                <p style="color: #666;">Los gráficos de progreso aparecerán después del primer análisis</p>
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
            <h2 style="color: {score_color}; margin-bottom: 1rem; font-size: 2.5rem;">
                🏆 Puntuación General: {overall_score}/10
            </h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗣️ Análisis de Voz", "🕴️ Lenguaje Corporal", "😊 Expresión Facial", "📊 Gráficos"])
    
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
            <h4 style="color: {score_color}; margin-bottom: 0.5rem;">🗣️ Puntuación Vocal</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        clarity = voice_analysis.get('clarity_score', 0)
        clarity_color = "#28a745" if clarity >= 7 else "#ffc107" if clarity >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {clarity_color}; margin-bottom: 0.5rem;">🎯 Claridad</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{clarity}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rate = voice_analysis.get('speaking_rate', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8; margin-bottom: 0.5rem;">⚡ Velocidad</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{rate}</h2>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">palabras/min</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown("#### 💬 Retroalimentación Detallada")
    feedback_container = st.container()
    with feedback_container:
        for i, feedback in enumerate(voice_analysis.get('feedback', [])):
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; border-left: 4px solid #667eea;">
                <p style="margin: 0; color: #333;">• {feedback}</p>
            </div>
            """, unsafe_allow_html=True)

def display_body_results_modern(body_analysis):
    """Display body language analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = body_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color}; margin-bottom: 0.5rem;">🕴️ Puntuación Corporal</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        posture = body_analysis.get('posture_stability', 0)
        posture_color = "#28a745" if posture >= 7 else "#ffc107" if posture >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {posture_color}; margin-bottom: 0.5rem;">🧍 Postura</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{posture}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        gestures = body_analysis.get('gesture_count', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8; margin-bottom: 0.5rem;">👋 Gestos</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{gestures}</h2>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">detectados</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown("#### 💬 Retroalimentación Detallada")
    for feedback in body_analysis.get('feedback', []):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; border-left: 4px solid #667eea;">
            <p style="margin: 0; color: #333;">• {feedback}</p>
        </div>
        """, unsafe_allow_html=True)

def display_facial_results_modern(facial_analysis):
    """Display facial expression analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = facial_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color}; margin-bottom: 0.5rem;">😊 Puntuación Facial</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        eye_contact = facial_analysis.get('eye_contact_score', 0)
        eye_color = "#28a745" if eye_contact >= 7 else "#ffc107" if eye_contact >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {eye_color}; margin-bottom: 0.5rem;">👁️ Contacto Visual</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{eye_contact}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        smiles = facial_analysis.get('smile_count', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #28a745; margin-bottom: 0.5rem;">😄 Sonrisas</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{smiles}</h2>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">detectadas</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown("#### 💬 Retroalimentación Detallada")
    for feedback in facial_analysis.get('feedback', []):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; border-left: 4px solid #667eea;">
            <p style="margin: 0; color: #333;">• {feedback}</p>
        </div>
        """, unsafe_allow_html=True)

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
        # Fallback to simple bar chart using Streamlit
        st.markdown("### 📊 Comparación de Puntuaciones")
        df = pd.DataFrame([scores])
        st.bar_chart(df.T)

def calculate_overall_score(voice_results, body_results, facial_results):
    """Calculate overall presentation score"""
    voice_score = voice_results.get('score', 0)
    body_score = body_results.get('score', 0)
    facial_score = facial_results.get('score', 0)
    
    # Weighted average (voice 40%, body 35%, facial 25%)
    overall = (voice_score * 0.4) + (body_score * 0.35) + (facial_score * 0.25)
    return round(overall, 1)

if __name__ == "__main__":
    main()

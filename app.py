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

# Configure page with dynamic title based on language
if 'language' not in st.session_state:
    st.session_state.language = 'es'

st.set_page_config(
    page_title=get_text("app_title", st.session_state.language),
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    """Main application function with authentication and multi-model support"""
    
    # Initialize session state and components
    initialize_session_state()
    components = initialize_components()
    
    # Check authentication
    if not st.session_state.authenticated:
        show_auth_interface(components['user_manager'])
        return
    
    # Show main application
    show_main_interface(components)

def show_auth_interface(user_manager):
    """Show authentication interface"""
    
    lang = st.session_state.language
    
    # Language selector in top right
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        languages = get_available_languages()
        lang_options = [f"{flag} {name}" for code, name, flag in languages]
        lang_codes = [code for code, name, flag in languages]
        
        current_index = lang_codes.index(st.session_state.language) if st.session_state.language in lang_codes else 0
        selected_lang = st.selectbox(
            "🌐", 
            options=lang_options,
            index=current_index,
            key="lang_selector"
        )
        
        if selected_lang:
            st.session_state.language = lang_codes[lang_options.index(selected_lang)]
            lang = st.session_state.language
    
    st.title(get_text("app_title", lang))
    st.markdown(f"### {get_text('app_subtitle', lang)}")
    
    # Authentication tabs
    tab1, tab2 = st.tabs([get_text("login", lang), get_text("register", lang)])
    
    with tab1:
        show_login_form(user_manager, lang)
    
    with tab2:
        show_register_form(user_manager, lang)

def show_login_form(user_manager, lang):
    """Show login form"""
    
    st.subheader(get_text("login", lang))
    
    with st.form("login_form"):
        username = st.text_input(get_text("username", lang))
        password = st.text_input(get_text("password", lang), type="password")
        
        if st.form_submit_button(get_text("login", lang)):
            if username and password:
                result = user_manager.authenticate(username, password)
                
                if result["success"]:
                    st.session_state.authenticated = True
                    st.session_state.user = result["user"]
                    
                    # Load user settings
                    settings = result["user"].get("settings", {})
                    st.session_state.language = settings.get("language", "es")
                    st.session_state.model_version = settings.get("model_version", "basic")
                    
                    st.success(get_text("success", lang))
                    st.rerun()
                else:
                    st.error(result["message"])
            else:
                st.warning(get_text("fill_all_fields", lang))

def show_register_form(user_manager, lang):
    """Show registration form"""
    
    st.subheader(get_text("register_teacher", lang))
    
    with st.form("register_form"):
        username = st.text_input(get_text("username", lang))
        password = st.text_input(get_text("password", lang), type="password")
        full_name = st.text_input(get_text("full_name", lang))
        institution = st.text_input(get_text("institution", lang))
        
        if st.form_submit_button(get_text("register", lang)):
            if username and password and full_name:
                result = user_manager.register_teacher(username, password, full_name, institution)
                
                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])
            else:
                st.warning(get_text("fill_required_fields", lang))

def show_main_interface(components):
    """Show main application interface for authenticated users"""
    
    lang = st.session_state.language
    user = st.session_state.user
    
    # Header with user info and logout
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title(get_text("app_title", lang))
        st.markdown(f"### {get_text('welcome', lang)} {user['full_name']}")
    
    with col3:
        if st.button(get_text("logout", lang)):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Sidebar for navigation and settings
    with st.sidebar:
        show_sidebar_content(components, lang, user)
    
    # Main content based on page selection
    page = st.session_state.get('current_page', 'dashboard')
    
    if page == 'dashboard':
        show_dashboard(components, lang, user)
    elif page == 'analysis':
        show_analysis_interface(components, lang, user)
    elif page == 'students':
        show_student_management(components, lang, user)
    elif page == 'reports':
        show_reports_interface(components, lang, user)
    elif page == 'settings':
        show_settings_interface(components, lang, user)

def show_sidebar_content(components, lang, user):
    """Show sidebar navigation and settings"""
    
    st.header(get_text("teacher_info", lang))
    st.info(f"**{user['full_name']}**\n{user.get('institution', '')}")
    
    # Navigation
    st.header(get_text("navigation", lang))
    
    pages = {
        'dashboard': f"📊 {get_text('dashboard', lang)}",
        'analysis': f"🎥 {get_text('video_analysis', lang)}",
        'students': f"👥 {get_text('student_management', lang)}",
        'reports': f"📄 {get_text('reports', lang)}",
        'settings': f"⚙️ {get_text('settings', lang)}"
    }
    
    for page_key, page_name in pages.items():
        if st.button(page_name, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()
    
    # Model version selector
    st.header(get_text("model_version", lang))
    
    model_options = [
        get_text("basic_model", lang),
        get_text("advanced_model", lang)
    ]
    
    current_model = 0 if st.session_state.model_version == 'basic' else 1
    
    selected_model = st.radio(
        "",
        options=model_options,
        index=current_model,
        key="model_selector"
    )
    
    new_model = 'basic' if selected_model == model_options[0] else 'advanced'
    if new_model != st.session_state.model_version:
        st.session_state.model_version = new_model
        # Update user settings
        components['user_manager'].update_user_settings(
            user['username'], 
            {'model_version': new_model}
        )
    
    # Model description
    if st.session_state.model_version == 'basic':
        st.info(get_text("basic_description", lang))
    else:
        st.info(get_text("advanced_description", lang))
    
    # Language selector
    st.header(get_text("language_setting", lang))
    
    languages = get_available_languages()
    lang_options = [f"{flag} {name}" for code, name, flag in languages]
    lang_codes = [code for code, name, flag in languages]
    
    current_index = lang_codes.index(st.session_state.language)
    
    selected_lang = st.selectbox(
        "",
        options=lang_options,
        index=current_index,
        key="sidebar_lang_selector"
    )
    
    new_lang = lang_codes[lang_options.index(selected_lang)]
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        # Update user settings
        components['user_manager'].update_user_settings(
            user['username'], 
            {'language': new_lang}
        )
        st.rerun()

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

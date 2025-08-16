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

# Initialize session state for theme and language
if 'language' not in st.session_state:
    st.session_state.language = 'es'
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Load images as base64
import base64

def load_image_as_base64(image_path):
    """Load image and convert to base64"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Load background and logo
background_b64 = load_image_as_base64("utils/media/Background.jpeg")
logo_b64 = load_image_as_base64("utils/media/logo.jpeg")

# Dynamic CSS based on theme
def get_dynamic_css(dark_mode=False):
    if dark_mode:
        # Dark mode colors - Professional palette
        bg_primary = "#0F1419"
        bg_secondary = "#1C2128"
        bg_card = "#21262D"
        text_primary = "#F0F6FC"
        text_secondary = "#8B949E"
        border_color = "#30363D"
        accent_primary = "#238636"
        accent_secondary = "#2EA043"
        shadow_color = "rgba(0, 0, 0, 0.6)"
        input_bg = "#21262D"
    else:
        # Light mode colors - Professional palette
        bg_primary = "#F6F8FA"
        bg_secondary = "#FFFFFF"
        bg_card = "#FFFFFF"
        text_primary = "#24292F"
        text_secondary = "#656D76"
        border_color = "#D0D7DE"
        accent_primary = "#0969DA"
        accent_secondary = "#0550AE"
        shadow_color = "rgba(0, 0, 0, 0.15)"
        input_bg = "#FFFFFF"
    
    background_image = f"data:image/jpeg;base64,{background_b64}" if background_b64 else ""
    logo_image = f"data:image/jpeg;base64,{logo_b64}" if logo_b64 else ""
    
    return f"""
    <style>
        /* Root variables */
        :root {{
            --bg-primary: {bg_primary};
            --bg-secondary: {bg_secondary};
            --bg-card: {bg_card};
            --text-primary: {text_primary};
            --text-secondary: {text_secondary};
            --border-color: {border_color};
            --accent-primary: {accent_primary};
            --accent-secondary: {accent_secondary};
            --shadow-color: {shadow_color};
            --input-bg: {input_bg};
        }}
        
        /* Main app background */
        .stApp {{
            background-color: var(--bg-primary);
            transition: all 0.3s ease;
        }}
        
        /* Main container */
        .main .block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 100%;
            background-color: var(--bg-primary);
        }}
        
        /* Fixed controls container */
        .controls-container {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        /* Theme toggle */
        .theme-toggle {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            padding: 0.5rem 1rem;
            box-shadow: 0 4px 20px var(--shadow-color);
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px var(--shadow-color);
        }}
        
        /* Language selector */
        .language-selector {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 25px;
            padding: 0.3rem 0.8rem;
            box-shadow: 0 4px 20px var(--shadow-color);
            min-width: 120px;
        }}
        
        /* Header with logo and background */
        .header-container {{
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
            padding: 3rem;
            border-radius: 25px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 15px 50px var(--shadow-color);
            position: relative;
            overflow: hidden;
        }}
        
        .header-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image: url('{background_image}');
            background-size: cover;
            background-position: center;
            opacity: 0.15;
            z-index: 1;
        }}
        
        .header-content {{
            position: relative;
            z-index: 2;
        }}
        
        .logo-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }}
        
        .logo-image {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid rgba(255, 255, 255, 0.3);
            margin-right: 1.5rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
        }}
        
        .logo-image:hover {{
            transform: scale(1.05);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
        }}
        
        .header-title {{
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.4);
            letter-spacing: -2px;
        }}
        
        .header-subtitle {{
            font-size: 1.4rem;
            opacity: 0.9;
            margin-bottom: 1rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }}
        
        /* Auth background overlay */
        .auth-background {{
            background-image: url('{background_image}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            position: relative;
        }}
        
        .auth-background::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: {'rgba(15, 20, 25, 0.85)' if dark_mode else 'rgba(246, 248, 250, 0.9)'};
            backdrop-filter: blur(15px);
        }}
        
        .auth-card {{
            position: relative;
            z-index: 2;
            background: var(--bg-card);
            border: 2px solid var(--border-color);
            backdrop-filter: blur(25px);
            box-shadow: 0 25px 80px var(--shadow-color);
        }}
        
        /* Card styling */
        .metric-card {{
            background: var(--bg-card);
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px var(--shadow-color);
            margin-bottom: 1.5rem;
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        }}
        
        .metric-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 60px var(--shadow-color);
        }}
        
        .analysis-card {{
            background: var(--bg-card);
            padding: 3.5rem;
            border-radius: 25px;
            box-shadow: 0 15px 50px var(--shadow-color);
            margin-bottom: 2rem;
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;
            color: var(--text-primary);
        }}
        
        .analysis-card:hover {{
            transform: translateY(-12px);
            box-shadow: 0 25px 80px var(--shadow-color);
        }}
        
        /* Button styling */
        .stButton > button {{
            background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
            color: white;
            border: none;
            padding: 1rem 3rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(9, 105, 218, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(9, 105, 218, 0.5);
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 12px;
            background: var(--bg-secondary);
            border-radius: 25px;
            padding: 0.75rem;
            border: 2px solid var(--border-color);
            box-shadow: 0 8px 30px var(--shadow-color);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: transparent;
            border-radius: 20px;
            color: var(--text-secondary);
            font-weight: 700;
            padding: 1rem 2.5rem;
            transition: all 0.3s ease;
            border: none;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: white !important;
            box-shadow: 0 6px 25px rgba(9, 105, 218, 0.4);
            transform: translateY(-2px);
        }}
        
        /* Input styling */
        .stTextInput > div > div > input {{
            background: var(--input-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            color: var(--text-primary);
            padding: 1.2rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px var(--shadow-color);
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 4px rgba(9, 105, 218, 0.2);
            background: var(--input-bg);
            outline: none;
        }}
        
        .stSelectbox > div > div > div {{
            background: var(--input-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            color: var(--text-primary);
            box-shadow: 0 4px 15px var(--shadow-color);
        }}
        
        /* File uploader styling */
        .stFileUploader > div > div {{
            border: 3px dashed var(--border-color);
            border-radius: 25px;
            background: var(--bg-secondary);
            padding: 3rem;
            transition: all 0.3s ease;
        }}
        
        .stFileUploader > div > div:hover {{
            border-color: var(--accent-primary);
            background: var(--bg-card);
            transform: translateY(-3px);
        }}
        
        /* Progress styling */
        .progress-container {{
            background: var(--bg-card);
            padding: 4rem;
            border-radius: 30px;
            box-shadow: 0 15px 50px var(--shadow-color);
            text-align: center;
            border: 2px solid var(--border-color);
            color: var(--text-primary);
        }}
        
        /* Dataframe styling */
        .stDataFrame {{
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 40px var(--shadow-color);
            border: 2px solid var(--border-color);
        }}
        
        /* Text colors */
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
        }}
        
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: var(--text-primary) !important;
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background: var(--bg-secondary);
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .header-title {{
                font-size: 2.5rem;
            }}
            .header-subtitle {{
                font-size: 1.1rem;
            }}
            .main .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}
            .analysis-card {{
                padding: 2rem;
            }}
            .controls-container {{
                position: relative;
                top: auto;
                right: auto;
                margin-bottom: 1rem;
                justify-content: center;
            }}
            .logo-image {{
                width: 80px;
                height: 80px;
                margin-bottom: 1rem;
            }}
            .logo-container {{
                flex-direction: column;
            }}
        }}
        
        /* Hide unnecessary elements */
        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
        .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK, footer, .css-164nlkn {{
            display: none;
        }}
        
        /* Score styling with theme awareness */
        .score-excellent {{ color: #238636; font-weight: bold; }}
        .score-good {{ color: #0969DA; font-weight: bold; }}
        .score-average {{ color: #D1242F; font-weight: bold; }}
        .score-poor {{ color: #CF222E; font-weight: bold; }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-secondary);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--accent-primary);
            border-radius: 5px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent-secondary);
        }}
        
        /* Loading animation */
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .loading {{
            animation: pulse 2s infinite;
        }}
    </style>
    """

# Apply dynamic CSS will be done in main function, not at module level

def configure_theme_and_css():
    """Configure theme and apply CSS styling"""
    dark_mode = st.session_state.get('dark_mode', False)
    st.markdown(get_dynamic_css(dark_mode), unsafe_allow_html=True)

# Global controls (theme toggle and language selector)
def show_global_controls():
    """Show theme toggle and language selector"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col3:
        subcol1, subcol2 = st.columns(2)
        
        with subcol1:
            # Language selector
            languages = get_available_languages()
            lang_options = [f"{flag} {name}" for code, name, flag in languages]
            lang_codes = [code for code, name, flag in languages]
            
            current_index = lang_codes.index(st.session_state.language) if st.session_state.language in lang_codes else 0
            selected_lang = st.selectbox(
                "🌐",
                options=lang_options,
                index=current_index,
                key="header_lang_selector",
                label_visibility="collapsed"
            )
            
            new_lang = lang_codes[lang_options.index(selected_lang)]
            if new_lang != st.session_state.language:
                st.session_state.language = new_lang
                st.rerun()
        
        with subcol2:
            # Theme toggle
            theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
            if st.button(theme_icon, key="theme_toggle", help="Cambiar tema"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()

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
    
    # Configure theme and CSS with dynamic updates
    configure_theme_and_css()
    
    # Show global controls at the top
    show_global_controls()
    
    # Update language if changed
    lang = st.session_state.get('language', 'es')
    
    # Check authentication
    if not st.session_state.authenticated:
        show_modern_auth_interface(components['user_manager'])
        return
    
    # Show main application
    show_modern_main_interface(components)

def show_modern_auth_interface(user_manager):
    """Show modern authentication interface with background image"""
    
    lang = st.session_state.language
    
    # Create auth background
    st.markdown('<div class="auth-background">', unsafe_allow_html=True)
    
    # Header with logo
    logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" class="logo-image">' if logo_b64 else ""
    
    st.markdown(f"""
    <div class="header-container">
        <div class="header-content">
            <div class="logo-container">
                {logo_html}
                <div>
                    <div class="header-title">🎯 HablaPRO AI</div>
                    <div class="header-subtitle">{get_text("app_subtitle", lang)}</div>
                </div>
            </div>
            <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.0; max-width: 600px; margin-left: auto; margin-right: auto;">
                {get_text("app_description", lang)}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the authentication form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Authentication tabs with modern styling
        tab1, tab2 = st.tabs([f"🔑 {get_text('login', lang)}", f"📝 {get_text('register', lang)}"])
        
        with tab1:
            show_modern_login_form(user_manager, lang)
        
        with tab2:
            show_modern_register_form(user_manager, lang)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_modern_login_form(user_manager, lang):
    """Show modern login form"""
    
    st.markdown(f"""
    <div class="analysis-card auth-card">
        <h3 style="text-align: center; margin-bottom: 2rem; color: var(--accent-primary); font-size: 1.8rem;">
            {get_text("welcome_back", lang)}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(f"👤 {get_text('username', lang)}", placeholder=get_text("enter_username", lang))
        password = st.text_input(f"🔒 {get_text('password', lang)}", type="password", placeholder=get_text("enter_password", lang))
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_button = st.form_submit_button(f"🚀 {get_text('login', lang)}", use_container_width=True)
        
        if login_button:
            if username and password:
                result = user_manager.authenticate(username, password)
                
                if result["success"]:
                    st.session_state.authenticated = True
                    st.session_state.user = result["user"]
                    
                    # Load user settings
                    settings = result["user"].get("settings", {})
                    st.session_state.language = settings.get("language", "es")
                    
                    st.success(f"✅ {get_text('login_success', lang)}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning(f"⚠️ {get_text('fill_all_fields', lang)}")

def show_modern_register_form(user_manager, lang):
    """Show modern registration form"""
    
    st.markdown(f"""
    <div class="analysis-card auth-card">
        <h3 style="text-align: center; margin-bottom: 2rem; color: var(--accent-primary); font-size: 1.8rem;">
            {get_text("create_account", lang)}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form", clear_on_submit=True):
        username = st.text_input(f"👤 {get_text('username', lang)}", placeholder=get_text("choose_username", lang))
        password = st.text_input(f"🔒 {get_text('password', lang)}", type="password", placeholder=get_text("create_password", lang))
        full_name = st.text_input(f"🏷️ {get_text('full_name', lang)}", placeholder=get_text("enter_full_name", lang))
        institution = st.text_input(f"🏫 {get_text('institution', lang)}", placeholder=get_text("enter_institution", lang))
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            register_button = st.form_submit_button(f"✨ {get_text('create_account', lang)}", use_container_width=True)
        
        if register_button:
            if username and password and full_name:
                result = user_manager.register_teacher(username, password, full_name, institution)
                
                if result["success"]:
                    st.success(f"✅ {get_text('account_created', lang)}")
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning(f"⚠️ {get_text('fill_required_fields', lang)}")

def show_modern_main_interface(components):
    """Show modern main application interface"""
    
    user = st.session_state.user
    lang = st.session_state.language
    
    # Modern header with user info and logo
    logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" class="logo-image">' if logo_b64 else ""
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"""
        <div class="header-container">
            <div class="header-content">
                <div class="logo-container">
                    {logo_html}
                    <div>
                        <h2 style="margin: 0; font-size: 2.5rem;">👋 {get_text('hello', lang)}, {user['full_name']}</h2>
                        <p style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 1.2rem;">
                            {user.get('institution', get_text('dashboard_subtitle', lang))}
                        </p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button(f"🚪 {get_text('logout', lang)}", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
    
    # Navigation with modern tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        f"📊 {get_text('dashboard', lang)}", 
        f"🎥 {get_text('video_analysis', lang)}", 
        f"👥 {get_text('students', lang)}", 
        f"📄 {get_text('reports', lang)}"
    ])
    
    with tab1:
        show_modern_dashboard(components, user, lang)
    
    with tab2:
        show_modern_analysis_interface(components, user, lang)
    
    with tab3:
        show_modern_student_management(components, user, lang)
    
    with tab4:
        show_modern_reports_interface(components, user, lang)

def show_modern_dashboard(components, user, lang):
    """Show modern teacher dashboard"""
    
    st.markdown(f"## 📊 {get_text('dashboard', lang)}")
    
    # Get teacher statistics
    stats = components['user_manager'].get_teacher_stats(user['username'])
    
    if stats:
        # Statistics cards with modern design
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: var(--accent-primary); margin-bottom: 0.5rem; font-size: 1rem;">👥 {get_text('students', lang)}</h3>
                <h2 style="margin: 0; color: var(--text-primary); font-size: 2.5rem;">{stats['total_students']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">{get_text('total_registered', lang)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #238636; margin-bottom: 0.5rem; font-size: 1rem;">✅ {get_text('active', lang)}</h3>
                <h2 style="margin: 0; color: var(--text-primary); font-size: 2.5rem;">{stats['active_students']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">{get_text('this_month', lang)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #0969DA; margin-bottom: 0.5rem; font-size: 1rem;">🎥 {get_text('analyses', lang)}</h3>
                <h2 style="margin: 0; color: var(--text-primary); font-size: 2.5rem;">{stats['total_analyses']}</h2>
                <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">{get_text('videos_analyzed', lang)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if stats['total_analyses'] > 0:
                avg_score = stats.get('average_score', 0)
                score_color = "#238636" if avg_score >= 7 else "#D1242F" if avg_score >= 5 else "#CF222E"
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: {score_color}; margin-bottom: 0.5rem; font-size: 1rem;">📈 {get_text('average', lang)}</h3>
                    <h2 style="margin: 0; color: var(--text-primary); font-size: 2.5rem;">{avg_score:.1f}/10</h2>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">{get_text('class_general', lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: var(--text-secondary); margin-bottom: 0.5rem; font-size: 1rem;">📈 {get_text('average', lang)}</h3>
                    <h2 style="margin: 0; color: var(--text-primary); font-size: 2.5rem;">--</h2>
                    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary); font-size: 0.9rem;">{get_text('no_data', lang)}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent activity
        if stats.get('recent_activity'):
            st.markdown(f"### 📋 {get_text('recent_activity', lang)}")
            
            activity_data = []
            for activity in stats['recent_activity']:
                score = activity.get('score', 0)
                
                activity_data.append({
                    f"👤 {get_text('student', lang)}": activity['student_id'],
                    f"📅 {get_text('date', lang)}": activity['timestamp'][:10],
                    f"⭐ {get_text('score', lang)}": f"{score}/10"
                })
            
            df = pd.DataFrame(activity_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown(f"""
        <div class="analysis-card">
            <div style="text-align: center; padding: 2rem;">
                <h3 style="color: var(--accent-primary);">🚀 {get_text('start_first_class', lang)}</h3>
                <p style="color: var(--text-secondary); font-size: 1.1rem;">{get_text('register_students_start', lang)}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_modern_analysis_interface(components, user, lang):
    """Show modern video analysis interface"""
    
    st.markdown(f"## 🎥 {get_text('video_analysis', lang)}")
    
    # Student selection
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if not students:
        st.markdown(f"""
        <div class="analysis-card">
            <div style="text-align: center; padding: 3rem;">
                <h3 style="color: var(--accent-primary);">👥 {get_text('no_students_registered', lang)}</h3>
                <p style="color: var(--text-secondary); font-size: 1.1rem;">{get_text('go_to_students_tab', lang)}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Modern student selector
    st.markdown(f"### 👤 {get_text('select_student', lang)}")
    student_options = [f"{s['anonymous_id']} - {s.get('name', get_text('no_name', lang))}" for s in students]
    selected_student_idx = st.selectbox(
        f"{get_text('student', lang)}:",
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
            <h3 style="margin-bottom: 1.5rem; color: var(--accent-primary);">📁 {get_text('Sube el video del alumno', lang)}</h3>
            <p style="margin-bottom: 1rem; color: var(--text-secondary); font-size: 1.1rem;">
                {get_text('analyzing_for', lang)}: <strong style="color: var(--accent-primary);">{selected_student['anonymous_id']}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Video upload with modern styling
        uploaded_file = st.file_uploader(
            f"{get_text('select_video', lang)}:",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help=f"{get_text('supported_formats', lang)}: MP4, AVI, MOV, MKV (Max: 300MB)",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Show video preview
            st.video(uploaded_file)
            
            # Analysis button with modern styling
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button(f"🚀 {get_text('analyze_presentation', lang)}", type="primary", use_container_width=True):
                    analyze_presentation_modern(
                        uploaded_file, selected_student, components, user, lang
                    )
    
    with col2:
        st.markdown(f"### 📊 {get_text('student_progress', lang)}")
        display_student_progress_modern(selected_student, components, lang)

def show_modern_student_management(components, user, lang):
    """Show modern student management interface"""
    
    st.markdown(f"## 👥 {get_text('student_management', lang)}")
    
    # Register new student with modern card
    st.markdown(f"""
    <div class="analysis-card">
        <h3 style="margin-bottom: 1.5rem; color: var(--accent-primary);">✨ {get_text('register_new_student', lang)}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            dni = st.text_input(f"🆔 {get_text('student_dni', lang)}", placeholder=get_text('enter_unique_id', lang))
        
        with col2:
            name = st.text_input(f"👤 {get_text('student_name', lang)}", placeholder=get_text('full_name_optional', lang))
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            register_button = st.form_submit_button(f"➕ {get_text('register_student', lang)}", use_container_width=True)
        
        if register_button:
            if dni:
                result = components['user_manager'].register_student(
                    user['username'], dni, name
                )
                
                if result["success"]:
                    st.success(f"✅ {get_text('student_registered_successfully', lang)} - ID: {result['anonymous_id']}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning(f"⚠️ {get_text('dni_required', lang)}")
    
    # Display existing students
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if students:
        st.markdown(f"### 📋 {get_text('registered_students', lang)}")
        
        # Create modern table display
        student_data = []
        for student in students:
            student_data.append({
                f"🏷️ {get_text('anonymous_id', lang)}": student['anonymous_id'],
                f"👤 {get_text('name', lang)}": student.get('name', get_text('no_name', lang)),
                f"📅 {get_text('registration_date', lang)}": student['registered_at'][:10],
                f"📊 {get_text('sessions', lang)}": student.get('total_sessions', 0)
            })
        
        df = pd.DataFrame(student_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown(f"""
        <div class="analysis-card">
            <div style="text-align: center; padding: 2rem;">
                <h4 style="color: var(--accent-primary);">📝 {get_text('no_students_registered', lang)}</h4>
                <p style="color: var(--text-secondary);">{get_text('register_first_student', lang)}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_modern_reports_interface(components, user, lang):
    """Show modern reports interface"""
    
    st.markdown(f"## 📄 {get_text('report_generation', lang)}")
    
    students = components['user_manager'].get_teacher_students(user['username'])
    
    if not students:
        st.markdown(f"""
        <div class="analysis-card">
            <div style="text-align: center; padding: 3rem;">
                <h3 style="color: var(--accent-primary);">👥 {get_text('no_students_for_reports', lang)}</h3>
                <p style="color: var(--text-secondary); font-size: 1.1rem;">{get_text('register_students_analyze', lang)}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Report type selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--accent-primary);">👤 {get_text('individual_report', lang)}</h3>
            <p style="color: var(--text-secondary);">{get_text('generate_detailed_report', lang)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        student_options = [f"{s['anonymous_id']} - {s.get('name', get_text('no_name', lang))}" for s in students]
        selected_idx = st.selectbox(
            f"{get_text('select_student', lang)}:",
            range(len(students)),
            format_func=lambda x: student_options[x],
            key="individual_report"
        )
        
        selected_student = students[selected_idx]
        
        if selected_student.get('analyses'):
            col_pdf, col_excel = st.columns(2)
            
            with col_pdf:
                if st.button(f"📄 {get_text('generate_pdf', lang)}", use_container_width=True):
                    generate_individual_report(selected_student, components, "pdf", lang)
            
            with col_excel:
                if st.button(f"📊 {get_text('generate_excel', lang)}", use_container_width=True):
                    generate_individual_report(selected_student, components, "excel", lang)
        else:
            st.info(f"⚠️ {get_text('no_analyses_available', lang)}")
    
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--accent-primary);">👥 {get_text('class_report', lang)}</h3>
            <p style="color: var(--text-secondary);">{get_text('generate_consolidated_report', lang)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        students_with_data = [s for s in students if s.get('analyses')]
        
        if students_with_data:
            st.info(f"📊 {len(students_with_data)} {get_text('students_with_data', lang)}")
            
            col_pdf2, col_excel2 = st.columns(2)
            
            with col_pdf2:
                if st.button(f"📄 {get_text('class_pdf', lang)}", use_container_width=True, key="class_pdf"):
                    generate_class_report(students_with_data, components, user, "pdf", lang)
            
            with col_excel2:
                if st.button(f"📊 {get_text('class_excel', lang)}", use_container_width=True, key="class_excel"):
                    generate_class_report(students_with_data, components, user, "excel", lang)
        else:
            st.info(f"⚠️ {get_text('no_students_with_analyses', lang)}")

def analyze_presentation_modern(uploaded_file, student, components, user, lang):
    """Modern analysis interface with enhanced UX"""
    
    # Create modern progress container
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown(f"""
        <div class="progress-container">
            <h3 style="color: var(--accent-primary);">🔄 {get_text('analyzing_presentation', lang)}</h3>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">{get_text('processing_with_ai', lang)}...</p>
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
        status_text.text(f"🎬 {get_text('processing_video', lang)}...")
        progress_bar.progress(20)
        
        video_info = components['video_processor'].process_video(video_path)
        if not video_info['success']:
            st.error(f"❌ {get_text('video_processing_error', lang)}: {video_info['error']}")
            return
        
        # Step 2: Voice analysis
        status_text.text(f"🗣️ {get_text('analyzing_voice_prosody', lang)}...")
        progress_bar.progress(40)
        
        voice_results = components['voice_analyzer'].analyze(video_path)
        
        # Step 3: Body language analysis
        status_text.text(f"🕴️ {get_text('analyzing_body_language', lang)}...")
        progress_bar.progress(70)
        
        body_results = components['body_analyzer'].analyze(video_path)
        
        # Step 4: Facial expression analysis
        status_text.text(f"😊 {get_text('analyzing_facial_expressions', lang)}...")
        progress_bar.progress(90)
        
        facial_results = components['facial_analyzer'].analyze(video_path)
        
        # Step 5: Compile results
        status_text.text(f"📊 {get_text('compiling_results', lang)}...")
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
        
        st.success(f"✅ {get_text('analysis_completed_successfully', lang)}!")
        display_modern_results(analysis_results, components, lang)
        
        # Clean up
        os.unlink(video_path)
        
    except Exception as e:
        progress_container.empty()
        st.error(f"❌ {get_text('analysis_error', lang)}: {str(e)}")

def display_student_progress_modern(student, components, lang):
    """Display modern student progress"""
    
    if not student.get('analyses'):
        st.markdown(f"""
        <div class="analysis-card">
            <div style="text-align: center; padding: 2rem;">
                <h4 style="color: var(--accent-primary);">📊 {get_text('no_historical_data', lang)}</h4>
                <p style="color: var(--text-secondary);">{get_text('progress_charts_appear_after_first_analysis', lang)}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Student statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: var(--accent-primary); margin-bottom: 0.5rem;">📊 {get_text('analyses', lang)}</h4>
            <h3 style="margin: 0; color: var(--text-primary);">{student.get('total_sessions', 0)}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if student['analyses']:
            last_score = student['analyses'][-1]['data']['overall_score']
            score_color = "#238636" if last_score >= 7 else "#D1242F" if last_score >= 5 else "#CF222E"
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="color: {score_color}; margin-bottom: 0.5rem;">⭐ {get_text('last', lang)}</h4>
                <h3 style="margin: 0; color: var(--text-primary);">{last_score}/10</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Progress trend
    if len(student['analyses']) > 1:
        scores = [analysis['data']['overall_score'] for analysis in student['analyses']]
        dates = [analysis['timestamp'][:10] for analysis in student['analyses']]
        
        progress_data = pd.DataFrame({
            f"{get_text('date', lang)}": dates,
            f"{get_text('score', lang)}": scores
        })
        
        st.markdown(f"#### 📈 {get_text('trend', lang)}")
        st.line_chart(progress_data.set_index(f"{get_text('date', lang)}"), height=200)

def generate_individual_report(student, components, report_type, lang):
    """Generate individual student report"""
    try:
        if report_type == "pdf":
            latest_analysis = student['analyses'][-1]['data']
            pdf_path = components['report_generator'].generate_individual_pdf_report(
                student, latest_analysis, lang
            )
            
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    st.download_button(
                        f"📥 {get_text('download_pdf', lang)}",
                        f.read(),
                        file_name=f"reporte_{student['anonymous_id']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.success(f"✅ {get_text('pdf_report_generated_successfully', lang)}")
            else:
                st.error(f"❌ {get_text('error_generating_pdf_report', lang)}")
        
        elif report_type == "excel":
            excel_path = components['report_generator'].generate_class_excel_report(
                {'username': 'teacher'}, [student], lang
            )
            
            if excel_path and os.path.exists(excel_path):
                with open(excel_path, 'rb') as f:
                    st.download_button(
                        f"📥 {get_text('download_excel', lang)}",
                        f.read(),
                        file_name=f"reporte_{student['anonymous_id']}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                st.success(f"✅ {get_text('excel_report_generated_successfully', lang)}")
            else:
                st.error(f"❌ {get_text('error_generating_excel_report', lang)}")
                
    except Exception as e:
        st.error(f"❌ {get_text('report_generation_error', lang)}: {str(e)}")

def generate_class_report(students, components, user, report_type, lang):
    """Generate class report"""
    try:
        if report_type == "pdf":
            pdf_path = components['report_generator'].generate_class_pdf_report(
                user, students, lang
            )
            
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    st.download_button(
                        f"📥 {get_text('download_class_pdf', lang)}",
                        f.read(),
                        file_name="reporte_clase.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                st.success(f"✅ {get_text('class_pdf_report_generated_successfully', lang)}")
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

def display_modern_results(results, components, lang='es'):
    """Display analysis results with modern interface"""
    
    # Overall score card
    overall_score = results['overall_score']
    score_color = "#28a745" if overall_score >= 7 else "#ffc107" if overall_score >= 5 else "#dc3545"
    
    st.markdown(f"""
    <div class="analysis-card">
        <div style="text-align: center;">
            <h2 style="color: {score_color}; margin-bottom: 1rem; font-size: 2.5rem;">
                🏆 {get_text('overall_score', lang)}: {overall_score}/10
            </h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed results in tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        f"🗣️ {get_text('voice_analysis', lang)}", 
        f"🕴️ {get_text('body_language', lang)}", 
        f"😊 {get_text('facial_expression', lang)}", 
        f"📊 {get_text('charts', lang)}"
    ])
    
    with tab1:
        display_voice_results_modern(results['voice_analysis'], lang)
    
    with tab2:
        display_body_results_modern(results['body_analysis'], lang)
    
    with tab3:
        display_facial_results_modern(results['facial_analysis'], lang)
    
    with tab4:
        display_charts_modern(results, components, lang)

def display_voice_results_modern(voice_analysis, lang='es'):
    """Display voice analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = voice_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color}; margin-bottom: 0.5rem;">🗣️ {get_text('voice_score', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        clarity = voice_analysis.get('clarity_score', 0)
        clarity_color = "#28a745" if clarity >= 7 else "#ffc107" if clarity >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {clarity_color}; margin-bottom: 0.5rem;">🎯 {get_text('clarity', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{clarity}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        rate = voice_analysis.get('speaking_rate', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8; margin-bottom: 0.5rem;">⚡ {get_text('speed', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{rate}</h2>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">{get_text('words_per_minute', lang)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown(f"#### 💬 {get_text('detailed_feedback', lang)}")
    feedback_container = st.container()
    with feedback_container:
        for i, feedback in enumerate(voice_analysis.get('feedback', [])):
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; border-left: 4px solid #667eea;">
                <p style="margin: 0; color: #333;">• {feedback}</p>
            </div>
            """, unsafe_allow_html=True)

def display_body_results_modern(body_analysis, lang='es'):
    """Display body language analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = body_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color}; margin-bottom: 0.5rem;">🕴️ {get_text('body_score', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        posture = body_analysis.get('posture_stability', 0)
        posture_color = "#28a745" if posture >= 7 else "#ffc107" if posture >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {posture_color}; margin-bottom: 0.5rem;">🧍 {get_text('posture', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{posture}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        gestures = body_analysis.get('gesture_count', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #17a2b8; margin-bottom: 0.5rem;">👋 {get_text('gestures', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{gestures}</h2>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">{get_text('detected', lang)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown(f"#### 💬 {get_text('detailed_feedback', lang)}")
    for feedback in body_analysis.get('feedback', []):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; border-left: 4px solid #667eea;">
            <p style="margin: 0; color: #333;">• {feedback}</p>
        </div>
        """, unsafe_allow_html=True)

def display_facial_results_modern(facial_analysis, lang='es'):
    """Display facial expression analysis with modern design"""
    
    col1, col2, col3 = st.columns(3)
    
    score = facial_analysis.get('score', 0)
    score_color = "#28a745" if score >= 7 else "#ffc107" if score >= 5 else "#dc3545"
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {score_color}; margin-bottom: 0.5rem;">😊 {get_text('facial_score', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{score}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        eye_contact = facial_analysis.get('eye_contact_score', 0)
        eye_color = "#28a745" if eye_contact >= 7 else "#ffc107" if eye_contact >= 5 else "#dc3545"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {eye_color}; margin-bottom: 0.5rem;">👁️ {get_text('eye_contact', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{eye_contact}/10</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        smiles = facial_analysis.get('smile_count', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: #28a745; margin-bottom: 0.5rem;">😄 {get_text('smiles', lang)}</h4>
            <h2 style="color: #333; margin: 0.5rem 0; font-size: 2.2rem;">{smiles}</h2>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">{get_text('detected', lang)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback
    st.markdown(f"#### 💬 {get_text('detailed_feedback', lang)}")
    for feedback in facial_analysis.get('feedback', []):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 10px; border-left: 4px solid #667eea;">
            <p style="margin: 0; color: #333;">• {feedback}</p>
        </div>
        """, unsafe_allow_html=True)

def display_charts_modern(results, components, lang='es'):
    """Display modern charts"""
    
    # Scores comparison
    scores = {
        get_text('voice', lang): results['voice_analysis'].get('score', 0),
        get_text('body', lang): results['body_analysis'].get('score', 0),
        get_text('facial', lang): results['facial_analysis'].get('score', 0)
    }
    
    # Create chart
    try:
        fig = components['chart_generator'].create_score_bar_chart(scores)
        st.pyplot(fig)
    except Exception as e:
        # Fallback to simple bar chart using Streamlit
        st.markdown(f"### 📊 {get_text('score_comparison', lang)}")
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

def get_score_description(score, lang):
    """Get score description based on value"""
    if score >= 8.5:
        return get_text('excellent', lang)
    elif score >= 7:
        return get_text('very_good', lang)
    elif score >= 5.5:
        return get_text('good', lang)
    elif score >= 4:
        return get_text('needs_improvement', lang)
    else:
        return get_text('needs_significant_improvement', lang)

def generate_recommendations_modern(results, lang):
    """Generate modern recommendations based on analysis"""
    
    recommendations = []
    
    # Voice recommendations
    voice_score = results.get('voice', {}).get('overall_score', 0)
    if voice_score < 6:
        recommendations.append({
            'title': get_text('improve_voice', lang),
            'description': get_text('practice_speaking_clearly', lang)
        })
    
    # Body language recommendations
    body_score = results.get('body_language', {}).get('overall_score', 0)
    if body_score < 6:
        recommendations.append({
            'title': get_text('improve_posture', lang),
            'description': get_text('work_on_confident_posture', lang)
        })
    
    # Facial recommendations
    facial_score = results.get('facial_expressions', {}).get('overall_score', 0)
    if facial_score < 6:
        recommendations.append({
            'title': get_text('improve_expressions', lang),
            'description': get_text('practice_natural_expressions', lang)
        })
    
    # If everything is good, add general recommendations
    if not recommendations:
        recommendations = [
            {
                'title': get_text('maintain_excellence', lang),
                'description': get_text('continue_good_work', lang)
            },
            {
                'title': get_text('add_dynamics', lang),
                'description': get_text('vary_tone_and_pace', lang)
            },
            {
                'title': get_text('connect_audience', lang),
                'description': get_text('focus_on_engagement', lang)
            }
        ]
    
    return recommendations

if __name__ == "__main__":
    main()

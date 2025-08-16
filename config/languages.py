"""Multi-language support for PresentAI"""

LANGUAGES = {
    "es": {
        "name": "Español",
        "flag": "🇪🇸",
        "translations": {
            # Navigation and Header
            "app_title": "PresentAI - Analizador de Habilidades de Presentación",
            "app_subtitle": "Mejora tus habilidades de presentación con análisis IA",
            "login": "Iniciar Sesión",
            "register": "Registrarse",
            "logout": "Cerrar Sesión",
            "dashboard": "Panel de Control",
            "settings": "Configuraciones",
            
            # User Management
            "teacher_info": "Información del Profesor",
            "student_info": "Información del Estudiante",
            "username": "Usuario",
            "password": "Contraseña",
            "full_name": "Nombre Completo",
            "institution": "Institución",
            "register_teacher": "Registrar Profesor",
            "register_student": "Registrar Estudiante",
            "student_dni": "DNI del Estudiante",
            "student_name": "Nombre del Estudiante (Opcional)",
            "anonymous_id": "ID Anónimo",
            
            # Analysis Interface
            "upload_video": "Subir Video de Práctica",
            "select_video": "Selecciona tu video de presentación",
            "video_help": "Sube un video de tu práctica de presentación para recibir feedback personalizado",
            "analyze_presentation": "Analizar Presentación",
            "processing_video": "Procesando video...",
            "analyzing_voice": "Analizando voz y prosodia...",
            "analyzing_body": "Analizando lenguaje corporal...",
            "analyzing_facial": "Analizando expresiones faciales...",
            "compiling_results": "Compilando resultados...",
            "analysis_complete": "¡Análisis completado!",
            
            # Content Analysis
            "upload_script": "Subir Guión (Opcional)",
            "script_help": "Sube el texto de tu presentación para análisis de contenido",
            "upload_rubric": "Subir Rúbrica (Opcional)",
            "rubric_help": "Sube la rúbrica de evaluación para criterios específicos",
            "content_analysis": "Análisis de Contenido",
            "rubric_evaluation": "Evaluación según Rúbrica",
            
            # Results
            "detailed_feedback": "Feedback Detallado",
            "charts": "Gráficos",
            "diagrams": "Diagramas",
            "overall_score": "Puntuación General",
            "voice_analysis": "Análisis de Voz y Prosodia",
            "body_analysis": "Análisis de Lenguaje Corporal",
            "facial_analysis": "Análisis de Expresiones Faciales",
            "voice_score": "Puntuación de Voz",
            "clarity": "Claridad",
            "speaking_rate": "Velocidad (ppm)",
            "filler_words": "Muletillas detectadas",
            "body_score": "Puntuación Corporal",
            "posture_stability": "Estabilidad de Postura",
            "gestures_detected": "Gestos Detectados",
            "general_movement": "Movimiento General",
            "facial_score": "Puntuación Facial",
            "eye_contact": "Contacto Visual",
            "average_confidence": "Confianza Promedio",
            "smiles_detected": "Sonrisas Detectadas",
            
            # Progress and History
            "historical_progress": "Progreso Histórico",
            "no_historical_data": "No hay datos históricos disponibles. ¡Sube tu primer video para comenzar!",
            "total_analyses": "Total de Análisis",
            "last_score": "Última Puntuación",
            "general_average": "Promedio General",
            "recent_improvement": "Mejora Reciente",
            
            # Export and Reports
            "export_pdf": "Exportar PDF",
            "export_excel": "Exportar Excel",
            "generate_report": "Generar Reporte",
            "individual_report": "Reporte Individual",
            "general_report": "Reporte General",
            "download_report": "Descargar Reporte",
            
            # Model Selection
            "model_version": "Versión del Modelo",
            "basic_model": "Modelo Básico",
            "advanced_model": "Modelo Avanzado",
            "basic_description": "Análisis de voz, lenguaje corporal y expresiones faciales",
            "advanced_description": "Incluye análisis de contenido, evaluación con rúbrica y reportes avanzados",
            
            # Settings
            "language_setting": "Idioma",
            "video_size_limit": "Límite de tamaño de video (MB)",
            "save_settings": "Guardar Configuraciones",
            "settings_saved": "Configuraciones guardadas exitosamente",
            
            # Messages
            "success": "Éxito",
            "error": "Error",
            "warning": "Advertencia",
            "info": "Información",
            "loading": "Cargando...",
            "please_wait": "Por favor espera...",
            "file_uploaded": "Archivo subido exitosamente",
            "analysis_error": "Error durante el análisis",
            "login_required": "Debes iniciar sesión para continuar",
            "insufficient_permissions": "Permisos insuficientes",
            
            # Feedback Messages
            "excellent_work": "¡Excelente trabajo!",
            "good_performance": "Buen desempeño general",
            "needs_improvement": "Necesitas trabajar en",
            "speaking_too_fast": "Hablas muy rápido",
            "speaking_too_slow": "Hablas muy lento",
            "good_speed": "Tu velocidad de habla es adecuada",
            "too_many_fillers": "Usas demasiadas muletillas",
            "good_clarity": "Tu claridad vocal es buena",
            "improve_posture": "Trabaja en mantener una postura más erguida",
            "good_eye_contact": "Mantuviste excelente contacto visual",
            "smile_more": "Sonríe más durante tu presentación",
            
            # Additional interface translations
            "welcome": "Bienvenido",
            "navigation": "Navegación",
            "video_analysis": "Análisis de Video",
            "student_management": "Gestión de Estudiantes",
            "reports": "Reportes",
            "fill_all_fields": "Completa todos los campos",
            "fill_required_fields": "Completa los campos requeridos",
            "analyzing_for": "Analizando para",
            "additional_content": "Contenido Adicional",
            "presentation_script": "Guión de Presentación",
            "no_script": "Sin guión",
            "type_script": "Escribir guión",
            "student_progress": "Progreso del Estudiante",
            "register_new_student": "Registrar Nuevo Estudiante",
            "register_student": "Registrar Estudiante",
            "dni_required": "DNI es requerido",
            "registered_students": "Estudiantes Registrados",
            "registration_date": "Fecha de Registro",
            "no_students_for_reports": "No hay estudiantes para generar reportes",
            "report_type": "Tipo de Reporte",
            "class_report": "Reporte de Clase",
            "select_student": "Seleccionar Estudiante",
            "generate_pdf": "Generar PDF",
            "download_pdf": "Descargar PDF",
            "generate_excel": "Generar Excel",
            "download_excel": "Descargar Excel",
            "report_generated": "Reporte generado",
            "no_analyses_for_student": "No hay análisis para este estudiante",
            "generate_class_pdf": "Generar PDF de Clase",
            "generate_class_excel": "Generar Excel de Clase",
            "no_analyses_for_class": "No hay análisis para la clase",
            "error_saving_settings": "Error al guardar configuraciones",
            "active_students": "Estudiantes Activos",
            "class_average": "Promedio de Clase",
            "recent_activity": "Actividad Reciente",
            "no_data_available": "No hay datos disponibles",
            "no_students_registered": "No hay estudiantes registrados",
            "register_students_first": "Registra estudiantes primero",
            "student": "Estudiante",
            "date": "Fecha",
            "name": "Nombre",
            "analyzing_content": "Analizando contenido...",
            "content_score": "Puntuación de Contenido",
            "progress_trend": "Tendencia de Progreso"
        }
    },
    "en": {
        "name": "English",
        "flag": "🇺🇸",
        "translations": {
            # Navigation and Header
            "app_title": "PresentAI - Presentation Skills Analyzer",
            "app_subtitle": "Improve your presentation skills with AI analysis",
            "login": "Login",
            "register": "Register",
            "logout": "Logout",
            "dashboard": "Dashboard",
            "settings": "Settings",
            
            # User Management
            "teacher_info": "Teacher Information",
            "student_info": "Student Information",
            "username": "Username",
            "password": "Password",
            "full_name": "Full Name",
            "institution": "Institution",
            "register_teacher": "Register Teacher",
            "register_student": "Register Student",
            "student_dni": "Student ID",
            "student_name": "Student Name (Optional)",
            "anonymous_id": "Anonymous ID",
            
            # Analysis Interface
            "upload_video": "Upload Practice Video",
            "select_video": "Select your presentation video",
            "video_help": "Upload a video of your presentation practice for personalized feedback",
            "analyze_presentation": "Analyze Presentation",
            "processing_video": "Processing video...",
            "analyzing_voice": "Analyzing voice and prosody...",
            "analyzing_body": "Analyzing body language...",
            "analyzing_facial": "Analyzing facial expressions...",
            "compiling_results": "Compiling results...",
            "analysis_complete": "Analysis completed!",
            
            # Content Analysis
            "upload_script": "Upload Script (Optional)",
            "script_help": "Upload your presentation text for content analysis",
            "upload_rubric": "Upload Rubric (Optional)",
            "rubric_help": "Upload evaluation rubric for specific criteria",
            "content_analysis": "Content Analysis",
            "rubric_evaluation": "Rubric-based Evaluation",
            
            # Results
            "detailed_feedback": "Detailed Feedback",
            "charts": "Charts",
            "diagrams": "Diagrams",
            "overall_score": "Overall Score",
            "voice_analysis": "Voice and Prosody Analysis",
            "body_analysis": "Body Language Analysis",
            "facial_analysis": "Facial Expression Analysis",
            "voice_score": "Voice Score",
            "clarity": "Clarity",
            "speaking_rate": "Speaking Rate (wpm)",
            "filler_words": "Filler words detected",
            "body_score": "Body Score",
            "posture_stability": "Posture Stability",
            "gestures_detected": "Gestures Detected",
            "general_movement": "General Movement",
            "facial_score": "Facial Score",
            "eye_contact": "Eye Contact",
            "average_confidence": "Average Confidence",
            "smiles_detected": "Smiles Detected",
            
            # Progress and History
            "historical_progress": "Historical Progress",
            "no_historical_data": "No historical data available. Upload your first video to get started!",
            "total_analyses": "Total Analyses",
            "last_score": "Last Score",
            "general_average": "General Average",
            "recent_improvement": "Recent Improvement",
            
            # Export and Reports
            "export_pdf": "Export PDF",
            "export_excel": "Export Excel",
            "generate_report": "Generate Report",
            "individual_report": "Individual Report",
            "general_report": "General Report",
            "download_report": "Download Report",
            
            # Model Selection
            "model_version": "Model Version",
            "basic_model": "Basic Model",
            "advanced_model": "Advanced Model",
            "basic_description": "Analysis of voice, body language and facial expressions",
            "advanced_description": "Includes content analysis, rubric evaluation and advanced reports",
            
            # Settings
            "language_setting": "Language",
            "video_size_limit": "Video size limit (MB)",
            "save_settings": "Save Settings",
            "settings_saved": "Settings saved successfully",
            
            # Messages
            "success": "Success",
            "error": "Error",
            "warning": "Warning",
            "info": "Information",
            "loading": "Loading...",
            "please_wait": "Please wait...",
            "file_uploaded": "File uploaded successfully",
            "analysis_error": "Error during analysis",
            "login_required": "You must log in to continue",
            "insufficient_permissions": "Insufficient permissions",
            
            # Feedback Messages
            "excellent_work": "Excellent work!",
            "good_performance": "Good overall performance",
            "needs_improvement": "You need to work on",
            "speaking_too_fast": "You speak too fast",
            "speaking_too_slow": "You speak too slow",
            "good_speed": "Your speaking speed is appropriate",
            "too_many_fillers": "You use too many filler words",
            "good_clarity": "Your vocal clarity is good",
            "improve_posture": "Work on maintaining better posture",
            "good_eye_contact": "You maintained excellent eye contact",
            "smile_more": "Smile more during your presentation"
        }
    },
    "qu": {
        "name": "Quechua",
        "flag": "🏔️",
        "translations": {
            # Navigation and Header
            "app_title": "PresentAI - Rimana Yachaykunata Qhawaq",
            "app_subtitle": "Rimana yachayniykita allinchaspa AI qhawaywan",
            "login": "Yaykuy",
            "register": "Qillqakuy",
            "logout": "Lluqsiy",
            "dashboard": "Kamachiy Panel",
            "settings": "Churaykunapaq",
            
            # User Management
            "teacher_info": "Yachachiqpa Willakuynin",
            "student_info": "Yachaqpa Willakuynin",
            "username": "Ruraqpa Sutin",
            "password": "Yaykuna Rima",
            "full_name": "Hunt'a Suti",
            "institution": "Yachana Wasi",
            "register_teacher": "Yachachiqta Qillqakuy",
            "register_student": "Yachaqta Qillqakuy",
            "student_dni": "Yachaqpa DNI",
            "student_name": "Yachaqpa Sutin (Akllanalla)",
            "anonymous_id": "Pakana ID",
            
            # Analysis Interface
            "upload_video": "Ruraykuna Videota Wichay",
            "select_video": "Rimayniykipa videonta akllay",
            "video_help": "Rimayniykipa ruraykuna videonta wichay allin yanapaykuna chaskinapaq",
            "analyze_presentation": "Rimayta Qhaway",
            "processing_video": "Videota ruraspa...",
            "analyzing_voice": "Kunkata hinaspa takita qhawaspa...",
            "analyzing_body": "Kurku rimayta qhawaspa...",
            "analyzing_facial": "Uyapa rimakunata qhawaspa...",
            "compiling_results": "Ruwaykunata huñuspa...",
            "analysis_complete": "¡Qhaway tukusqa!",
            
            # Content Analysis
            "upload_script": "Qillqata Wichay (Akllanalla)",
            "script_help": "Rimayniykipa qillqanta wichay contenidota qhawanapaq",
            "upload_rubric": "Chaninchayta Wichay (Akllanalla)",
            "rubric_help": "Chaninchaypaq kamachiykunata wichay",
            "content_analysis": "Contenido Qhaway",
            "rubric_evaluation": "Rúbrica nisqanman hina Chaninchaykuy",
            
            # Results
            "detailed_feedback": "Sut'i Yanapaykuna",
            "charts": "Qillqakuna",
            "diagrams": "Rikuchiykunapaq",
            "overall_score": "Tukuypaq Puntuacion",
            "voice_analysis": "Kunka hinaspa Taki Qhaway",
            "body_analysis": "Kurku Rimay Qhaway",
            "facial_analysis": "Uya Rimaykunapa Qhawaynin",
            "voice_score": "Kunka Puntuacion",
            "clarity": "Sut'inchaykuy",
            "speaking_rate": "Rimay Usqhay (ppm)",
            "filler_words": "Hunt'asqa rimakuna tarisqa",
            "body_score": "Kurku Puntuacion",
            "posture_stability": "Sayasqapa Takyay",
            "gestures_detected": "Sañakuna Tarisqa",
            "general_movement": "Llapanpaq Kuyuy",
            "facial_score": "Uya Puntuacion",
            "eye_contact": "Ñawi Tupanakuy",
            "average_confidence": "Chawpi Confianza",
            "smiles_detected": "Asikuna Tarisqa",
            
            # Progress and History
            "historical_progress": "Ñawpaq Ñanpi Puriy",
            "no_historical_data": "Mana ñawpaq willaykuna kanchu. ¡Ñawpaq videota wichay qallariyniykipaq!",
            "total_analyses": "Tukuy Qhawaykunapaq",
            "last_score": "Qhipa Puntuacion",
            "general_average": "Llapanpaq Chawpi",
            "recent_improvement": "Kunan Allinchaykuy",
            
            # Export and Reports
            "export_pdf": "PDF Lluqsichiy",
            "export_excel": "Excel Lluqsichiy",
            "generate_report": "Willakuyta Ruray",
            "individual_report": "Sapanka Willakuy",
            "general_report": "Llapanpaq Willakuy",
            "download_report": "Willakuyta Urquy",
            
            # Model Selection
            "model_version": "Modelo Rikuy",
            "basic_model": "Hatun Modelo",
            "advanced_model": "Ñawpaqman Puriq Modelo",
            "basic_description": "Kunka, kurku rimay hinaspa uya rimakunapa qhawaynin",
            "advanced_description": "Contenido qhaway, rúbrica chaninchaykuy hinaspa ñawpaqman puriq willakuykunayuq",
            
            # Settings
            "language_setting": "Rimay",
            "video_size_limit": "Video hatunkaynin limitasqa (MB)",
            "save_settings": "Churaykunata Waqaychay",
            "settings_saved": "Churaykunaqa allinta waqaychasqa",
            
            # Messages
            "success": "Allin Ruway",
            "error": "Pantay",
            "warning": "Yuyaychay",
            "info": "Willay",
            "loading": "Kargaspa...",
            "please_wait": "Ama hina kaspa suyay...",
            "file_uploaded": "Archivo allinta wichasqa",
            "analysis_error": "Qhawaypi pantay",
            "login_required": "Yaykuy tiyan purinapaq",
            "insufficient_permissions": "Mana allin atiykuna",
            
            # Feedback Messages
            "excellent_work": "¡Ancha allin ruway!",
            "good_performance": "Allin llapan ruway",
            "needs_improvement": "Llamkay tiyan",
            "speaking_too_fast": "Ancha usqhaylla rimanki",
            "speaking_too_slow": "Ancha pisi rimaylla rimanki",
            "good_speed": "Rimayniykipa usqhayninqa allin",
            "too_many_fillers": "Ancha achka hunt'ana rimakunata llamkanki",
            "good_clarity": "Kunkaykipa sut'inchaynin allin",
            "improve_posture": "Aswan allin sayasqata llamkay",
            "good_eye_contact": "Ancha allin ñawi tupanakuyta ruwarqanki",
            "smile_more": "Aswan achka asikapuy rimayniykipi"
        }
    }
}

def get_text(key, language="es"):
    """Get translated text for given key and language"""
    return LANGUAGES.get(language, LANGUAGES["es"])["translations"].get(key, key)

def get_available_languages():
    """Get list of available languages"""
    return [(code, lang["name"], lang["flag"]) for code, lang in LANGUAGES.items()]
#!/usr/bin/env python3
"""
Script de verificación para Coach AI v2
Verifica que todas las dependencias estén correctamente instaladas
"""

import sys
import importlib
from pathlib import Path

def check_package(package_name, import_name=None):
    """Verificar si un paquete está instalado e importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - Error: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔍 Coach AI v2 - Verificación de Instalación")
    print("=" * 50)
    
    # Verificar versión de Python
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.11+")
        return False
    
    print("\n📦 Verificando dependencias principales:")
    
    # Lista de dependencias críticas
    critical_packages = [
        ("streamlit", "streamlit"),
        ("whisper", "whisper"),
        ("mediapipe", "mediapipe"),
        ("opencv-python", "cv2"),
        ("librosa", "librosa"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("pillow", "PIL"),
        ("soundfile", "soundfile"),
        ("bcrypt", "bcrypt"),
        ("fpdf2", "fpdf"),
        ("reportlab", "reportlab"),
        ("openpyxl", "openpyxl"),
    ]
    
    all_good = True
    for package_name, import_name in critical_packages:
        if not check_package(package_name, import_name):
            all_good = False
    
    print("\n🔧 Verificando archivos del proyecto:")
    
    # Verificar archivos críticos
    critical_files = [
        "app.py",
        "requirements.txt",
        "pyproject.toml",
        "analysis/voice_analyzer.py",
        "analysis/body_language_analyzer.py",
        "analysis/facial_analyzer.py",
        "analysis/content_analyzer.py",
        "utils/video_processor.py",
        "auth/user_manager.py"
    ]
    
    for file_path in critical_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Archivo no encontrado")
            all_good = False
    
    print("\n🧪 Verificando funcionalidad básica:")
    
    # Test básico de importación de módulos del proyecto
    try:
        sys.path.append('.')
        from analysis.voice_analyzer import VoiceAnalyzer
        from analysis.body_language_analyzer import BodyLanguageAnalyzer
        from analysis.facial_analyzer import FacialAnalyzer
        from analysis.content_analyzer import ContentAnalyzer
        print("✅ Módulos de análisis importados correctamente")
    except Exception as e:
        print(f"❌ Error importando módulos de análisis: {e}")
        all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 ¡Instalación verificada correctamente!")
        print("\n🚀 Para iniciar la aplicación:")
        print("   streamlit run app.py")
        print("\n🌐 La aplicación estará disponible en:")
        print("   http://localhost:8501")
    else:
        print("❌ Se encontraron problemas en la instalación")
        print("\n🔧 Soluciones recomendadas:")
        print("1. Reinstalar dependencias: pip install -r requirements.txt")
        print("2. Verificar Python 3.11+: python --version")
        print("3. Verificar FFmpeg: ffmpeg -version")
        print("4. Consultar README.md para más detalles")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

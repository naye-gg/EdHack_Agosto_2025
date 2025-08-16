#!/usr/bin/env python3
"""
Script de instalación automática para Coach AI v2
Verifica requisitos del sistema e instala dependencias
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major != 3 or version.minor < 11:
        print("❌ Error: Se requiere Python 3.11 o superior")
        print(f"Versión actual: Python {version.major}.{version.minor}.{version.micro}")
        print("Por favor instala Python 3.11+ desde https://python.org")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def check_system_dependencies():
    """Verificar dependencias del sistema"""
    system = platform.system().lower()
    
    print(f"🔍 Detectado sistema: {platform.system()}")
    
    # Verificar FFmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL, 
                      check=True)
        print("✅ FFmpeg encontrado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  FFmpeg no encontrado")
        print_ffmpeg_install_instructions(system)
        return False
    
    return True

def print_ffmpeg_install_instructions(system):
    """Mostrar instrucciones de instalación de FFmpeg"""
    if system == "linux":
        print("Instala FFmpeg con:")
        print("sudo apt-get update && sudo apt-get install ffmpeg libsndfile1 libsndfile1-dev")
    elif system == "darwin":  # macOS
        print("Instala FFmpeg con Homebrew:")
        print("brew install ffmpeg libsndfile")
    elif system == "windows":
        print("Descarga FFmpeg desde: https://ffmpeg.org/download.html")
        print("Y agrégalo al PATH del sistema")

def create_virtual_environment():
    """Crear entorno virtual"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📁 Entorno virtual existente encontrado")
        return True
    
    print("🔧 Creando entorno virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Entorno virtual creado en ./venv")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error creando entorno virtual")
        return False

def get_pip_command():
    """Obtener comando pip correcto para el entorno virtual"""
    system = platform.system().lower()
    if system == "windows":
        return str(Path("venv") / "Scripts" / "pip")
    else:
        return str(Path("venv") / "bin" / "pip")

def install_dependencies():
    """Instalar dependencias de Python"""
    pip_cmd = get_pip_command()
    
    print("📦 Instalando dependencias...")
    print("Esto puede tomar varios minutos...")
    
    try:
        # Actualizar pip
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Instalar dependencias
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias")
        print("Intenta manualmente: pip install -r requirements.txt")
        return False

def verify_installation():
    """Verificar que las dependencias principales están instaladas"""
    pip_cmd = get_pip_command()
    
    key_packages = [
        "streamlit", "whisper", "mediapipe", 
        "opencv-python", "librosa", "numpy"
    ]
    
    print("🔍 Verificando instalación...")
    
    for package in key_packages:
        try:
            result = subprocess.run(
                [pip_cmd, "show", package], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                check=True
            )
            print(f"✅ {package}")
        except subprocess.CalledProcessError:
            print(f"❌ {package} no instalado")
            return False
    
    return True

def create_directories():
    """Crear directorios necesarios"""
    dirs = ["data/students", "auth"]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("📁 Directorios creados")

def print_usage_instructions():
    """Mostrar instrucciones de uso"""
    system = platform.system().lower()
    
    print("\n🎉 ¡Instalación completada!")
    print("\n📝 Para usar Coach AI v2:")
    print("1. Activar entorno virtual:")
    
    if system == "windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("2. Iniciar aplicación:")
    print("   streamlit run app.py")
    print("3. Abrir navegador en: http://localhost:8501")
    print("\n💡 Crear primer usuario profesor en la interfaz web")

def main():
    """Función principal"""
    print("🚀 Coach AI v2 - Script de Instalación")
    print("=" * 40)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Verificar que estamos en el directorio correcto
    if not Path("requirements.txt").exists():
        print("❌ Error: requirements.txt no encontrado")
        print("Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Verificar dependencias del sistema
    if not check_system_dependencies():
        print("\n⚠️  Instala las dependencias del sistema antes de continuar")
        choice = input("\n¿Continuar de todos modos? (y/N): ").lower()
        if choice not in ['y', 'yes', 'sí', 's']:
            sys.exit(1)
    
    # Crear entorno virtual
    if not create_virtual_environment():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Verificar instalación
    if not verify_installation():
        print("⚠️  Algunas dependencias pueden no haberse instalado correctamente")
    
    # Crear directorios
    create_directories()
    
    # Mostrar instrucciones
    print_usage_instructions()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para configurar y gestionar entorno virtual para Coach AI v2
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
        print("❌ Error: Se requiere Python 3.11 - 3.12")
        print(f"Versión actual: Python {version.major}.{version.minor}.{version.micro}")
        return False
    
    if version.minor >= 13:
        print("⚠️  Advertencia: Python 3.13+ puede tener problemas de compatibilidad con MediaPipe")
        print("Se recomienda usar Python 3.11 o 3.12")
        choice = input("¿Continuar de todos modos? (y/N): ").lower()
        if choice not in ['y', 'yes', 'sí', 's']:
            return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def create_venv():
    """Crear entorno virtual"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📁 Entorno virtual ya existe en ./venv")
        choice = input("¿Deseas recrearlo? (y/N): ").lower()
        if choice in ['y', 'yes', 'sí', 's']:
            print("🗑️  Eliminando entorno virtual existente...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            return True
    
    print("🔧 Creando entorno virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Entorno virtual creado en ./venv")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False

def get_activation_command():
    """Obtener comando de activación según el sistema operativo"""
    system = platform.system().lower()
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def get_pip_command():
    """Obtener comando pip del entorno virtual"""
    system = platform.system().lower()
    if system == "windows":
        return str(Path("venv") / "Scripts" / "pip")
    else:
        return str(Path("venv") / "bin" / "pip")

def get_python_command():
    """Obtener comando python del entorno virtual"""
    system = platform.system().lower()
    if system == "windows":
        return str(Path("venv") / "Scripts" / "python")
    else:
        return str(Path("venv") / "bin" / "python")

def install_dependencies():
    """Instalar dependencias en el entorno virtual"""
    pip_cmd = get_pip_command()
    
    print("📦 Instalando dependencias en el entorno virtual...")
    
    try:
        # Actualizar pip
        print("⬆️  Actualizando pip...")
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Instalar wheel para compilaciones más rápidas
        subprocess.run([pip_cmd, "install", "wheel"], check=True)
        
        # Instalar dependencias
        print("📦 Instalando dependencias del proyecto...")
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_activation_scripts():
    """Crear scripts de activación personalizados"""
    system = platform.system().lower()
    
    # Script para Unix/Linux/macOS
    if system != "windows":
        activate_script = """#!/bin/bash
# Script de activación para Coach AI v2

# Colores para output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo -e "${GREEN}🚀 Activando entorno virtual Coach AI v2${NC}"

# Verificar que existe el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
    echo -e "${YELLOW}Ejecuta: python setup_venv.py${NC}"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar activación
if [ "$VIRTUAL_ENV" != "" ]; then
    echo -e "${GREEN}✅ Entorno virtual activado${NC}"
    echo -e "${GREEN}📍 Ubicación: $VIRTUAL_ENV${NC}"
    
    # Mostrar versión de Python
    echo -e "${GREEN}🐍 Python: $(python --version)${NC}"
    
    # Mostrar comandos útiles
    echo ""
    echo -e "${YELLOW}Comandos útiles:${NC}"
    echo -e "  ${GREEN}streamlit run app.py${NC}     - Iniciar aplicación"
    echo -e "  ${GREEN}python verify_installation.py${NC} - Verificar instalación"
    echo -e "  ${GREEN}deactivate${NC}               - Desactivar entorno virtual"
    echo ""
else
    echo -e "${RED}❌ Error activando entorno virtual${NC}"
    exit 1
fi
"""
        
        with open("activate_venv.sh", "w") as f:
            f.write(activate_script)
        
        # Dar permisos de ejecución
        os.chmod("activate_venv.sh", 0o755)
        print("✅ Creado: activate_venv.sh")
    
    # Script para Windows
    activate_script_win = """@echo off
REM Script de activación para Coach AI v2

echo 🚀 Activando entorno virtual Coach AI v2

REM Verificar que existe el entorno virtual
if not exist "venv" (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta: python setup_venv.py
    exit /b 1
)

REM Activar entorno virtual
call venv\\Scripts\\activate.bat

REM Verificar activación
if defined VIRTUAL_ENV (
    echo ✅ Entorno virtual activado
    echo 📍 Ubicación: %VIRTUAL_ENV%
    
    REM Mostrar versión de Python
    echo 🐍 Python:
    python --version
    
    REM Mostrar comandos útiles
    echo.
    echo Comandos útiles:
    echo   streamlit run app.py        - Iniciar aplicación
    echo   python verify_installation.py - Verificar instalación
    echo   deactivate                  - Desactivar entorno virtual
    echo.
) else (
    echo ❌ Error activando entorno virtual
    exit /b 1
)
"""
    
    with open("activate_venv.bat", "w") as f:
        f.write(activate_script_win)
    
    print("✅ Creado: activate_venv.bat")

def create_run_script():
    """Crear script para ejecutar la aplicación"""
    system = platform.system().lower()
    
    # Script para Unix/Linux/macOS
    if system != "windows":
        run_script = """#!/bin/bash
# Script para ejecutar Coach AI v2

# Colores
GREEN='\\033[0;32m'
RED='\\033[0;31m'
NC='\\033[0m'

echo -e "${GREEN}🚀 Iniciando Coach AI v2${NC}"

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
    echo "Ejecuta: python setup_venv.py"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar que streamlit está instalado
if ! command -v streamlit &> /dev/null; then
    echo -e "${RED}❌ Streamlit no encontrado${NC}"
    echo "Ejecuta: pip install -r requirements.txt"
    exit 1
fi

# Ejecutar aplicación
echo -e "${GREEN}🌐 Abriendo aplicación en http://localhost:8501${NC}"
streamlit run app.py
"""
        
        with open("run.sh", "w") as f:
            f.write(run_script)
        
        os.chmod("run.sh", 0o755)
        print("✅ Creado: run.sh")
    
    # Script para Windows
    run_script_win = """@echo off
REM Script para ejecutar Coach AI v2

echo 🚀 Iniciando Coach AI v2

REM Verificar entorno virtual
if not exist "venv" (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta: python setup_venv.py
    exit /b 1
)

REM Activar entorno virtual
call venv\\Scripts\\activate.bat

REM Verificar que streamlit está instalado
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit no encontrado
    echo Ejecuta: pip install -r requirements.txt
    exit /b 1
)

REM Ejecutar aplicación
echo 🌐 Abriendo aplicación en http://localhost:8501
streamlit run app.py
"""
    
    with open("run.bat", "w") as f:
        f.write(run_script_win)
    
    print("✅ Creado: run.bat")

def create_requirements_dev():
    """Crear requirements-dev.txt para dependencias de desarrollo"""
    dev_requirements = """# Dependencias de desarrollo para Coach AI v2

# Herramientas de testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Herramientas de código
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0
mypy>=1.0.0

# Documentación
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0

# Jupyter para análisis
jupyter>=1.0.0
notebook>=6.5.0

# Profiling y debugging
memory-profiler>=0.60.0
line-profiler>=4.0.0

# Herramientas de build
build>=0.10.0
twine>=4.0.0
"""
    
    with open("requirements-dev.txt", "w") as f:
        f.write(dev_requirements)
    
    print("✅ Creado: requirements-dev.txt")

def print_instructions():
    """Mostrar instrucciones finales"""
    system = platform.system().lower()
    
    print("\n" + "="*60)
    print("🎉 ¡Entorno virtual configurado correctamente!")
    print("="*60)
    
    print("\n📝 Para usar Coach AI v2:")
    
    if system == "windows":
        print("\n🟢 Opción 1: Usar script de activación")
        print("   activate_venv.bat")
        print("\n🟢 Opción 2: Activación manual")
        print("   venv\\Scripts\\activate")
        print("   streamlit run app.py")
        print("\n🟢 Opción 3: Ejecutar directamente")
        print("   run.bat")
    else:
        print("\n🟢 Opción 1: Usar script de activación")
        print("   ./activate_venv.sh")
        print("\n🟢 Opción 2: Activación manual")
        print("   source venv/bin/activate")
        print("   streamlit run app.py")
        print("\n🟢 Opción 3: Ejecutar directamente")
        print("   ./run.sh")
    
    print("\n🌐 La aplicación estará disponible en:")
    print("   http://localhost:8501")
    
    print("\n🔧 Comandos útiles:")
    print("   python verify_installation.py  - Verificar instalación")
    print("   deactivate                     - Desactivar entorno virtual")
    
    print("\n💡 Consejos:")
    print("   • Siempre activa el entorno virtual antes de trabajar")
    print("   • Usa 'deactivate' para salir del entorno virtual")
    print("   • Los scripts de activación muestran comandos útiles")

def main():
    """Función principal"""
    print("🔧 Coach AI v2 - Configuración de Entorno Virtual")
    print("="*55)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Verificar que estamos en el directorio correcto
    if not Path("requirements.txt").exists():
        print("❌ Error: requirements.txt no encontrado")
        print("Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Crear entorno virtual
    if not create_venv():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        sys.exit(1)
    
    # Crear scripts auxiliares
    create_activation_scripts()
    create_run_script()
    create_requirements_dev()
    
    # Mostrar instrucciones
    print_instructions()

if __name__ == "__main__":
    main()

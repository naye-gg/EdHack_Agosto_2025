@echo off
REM Script de ayuda para Windows - Coach AI v2

echo.
echo ==========================================
echo      Coach AI v2 - Ayuda Windows
echo ==========================================
echo.

echo 📋 COMANDOS PRINCIPALES:
echo.
echo   setup.bat        - Configurar entorno virtual e instalar dependencias
echo   run.bat          - Ejecutar la aplicación Coach AI v2
echo   activate.bat     - Activar entorno virtual manualmente
echo   verify.bat       - Verificar que todo esté instalado correctamente
echo   clean.bat        - Limpiar archivos temporales y cache
echo   update.bat       - Actualizar dependencias
echo.

echo 📋 COMANDOS POWERSHELL (más avanzados):
echo.
echo   .\setup.ps1      - Configuración con PowerShell
echo   .\run.ps1        - Ejecutar con PowerShell
echo   .\clean.ps1      - Limpieza con PowerShell
echo.

echo 📋 COMANDOS PYTHON DIRECTOS:
echo.
echo   python setup_venv.py           - Configuración automática
echo   python verify_installation.py  - Verificar instalación
echo   python clean.py --help         - Ver opciones de limpieza
echo.

echo 🔧 SOLUCIÓN DE PROBLEMAS COMUNES:
echo.
echo   ❌ "Python no encontrado"
echo      → Instalar Python desde python.org
echo      → Asegurarse de marcar "Add Python to PATH"
echo.
echo   ❌ "Error instalando dependencias"  
echo      → Ejecutar como administrador
echo      → Instalar Visual Studio Build Tools
echo      → Verificar conexión a internet
echo.
echo   ❌ "MediaPipe no funciona"
echo      → Usar Python 3.11 o 3.12 (no 3.13+)
echo      → Ejecutar: setup.bat
echo.
echo   ❌ "Puerto 8501 ocupado"
echo      → Cambiar puerto: streamlit run app.py --server.port 8080
echo      → O cerrar otras aplicaciones Streamlit
echo.

echo 📁 ESTRUCTURA DE ARCHIVOS:
echo.
echo   app.py                    - Aplicación principal
echo   requirements.txt          - Dependencias Python 3.11-3.12
echo   requirements-python313.txt - Dependencias Python 3.13+
echo   venv\                     - Entorno virtual
echo   data\students\            - Datos de estudiantes
echo   auth\                     - Archivos de autenticación
echo   reports\                  - Reportes generados
echo.

echo 🌐 ACCESO A LA APLICACIÓN:
echo.
echo   URL Local:     http://localhost:8501
echo   URL Red:       http://[tu-ip]:8501
echo.
echo   Para acceso desde red, ejecutar:
echo   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
echo.

echo 📞 SOPORTE:
echo.
echo   📖 Documentación completa: README.md
echo   🚀 Guía rápida: GETTING_STARTED.md
echo   🔧 Compatibilidad: COMPATIBILITY.md
echo.

echo Presiona cualquier tecla para continuar...
pause >nul

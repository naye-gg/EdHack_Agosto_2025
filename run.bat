@echo off
REM Script para ejecutar Coach AI v2 en Windows
setlocal

echo.
echo ==========================================
echo     🚀 Iniciando Coach AI v2
echo ==========================================

REM Verificar entorno virtual
if not exist "venv\" (
    echo ❌ Entorno virtual no encontrado
    echo.
    echo Ejecuta primero: setup.bat
    pause
    exit /b 1
)

REM Verificar que app.py existe
if not exist "app.py" (
    echo ❌ app.py no encontrado
    echo Asegurate de estar en el directorio correcto del proyecto
    pause
    exit /b 1
)

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar que streamlit está instalado
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Streamlit no encontrado
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)

echo ✅ Entorno listo
echo.
echo 🌐 Abriendo Coach AI v2 en: http://localhost:8501
echo.
echo 💡 Para detener la aplicación: Ctrl+C
echo 💡 Para cerrar esta ventana: Ctrl+C y luego cerrar
echo.

REM Intentar abrir en navegador (opcional)
start "" "http://localhost:8501" 2>nul

REM Ejecutar aplicación
streamlit run app.py --server.port 8501

echo.
echo 👋 Coach AI v2 finalizado
pause

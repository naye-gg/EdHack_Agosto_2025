@echo off
REM Script de verificación para Windows

echo.
echo ==========================================
echo   Coach AI v2 - Verificación Windows
echo ==========================================
echo.

REM Verificar Python
echo 🐍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    echo Instala Python desde: https://python.org/downloads/
    goto :end
) else (
    for /f "tokens=2" %%i in ('python --version') do echo ✅ %%i detectado
)

REM Verificar entorno virtual
echo.
echo 📁 Verificando entorno virtual...
if exist "venv\" (
    echo ✅ Entorno virtual encontrado
) else (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta: setup.bat
    goto :end
)

REM Activar entorno virtual para verificaciones
call venv\Scripts\activate.bat

REM Verificar aplicación principal
echo.
echo 📄 Verificando archivos del proyecto...
if exist "app.py" (
    echo ✅ app.py encontrado
) else (
    echo ❌ app.py no encontrado
)

if exist "requirements.txt" (
    echo ✅ requirements.txt encontrado
) else (
    echo ❌ requirements.txt no encontrado
)

REM Verificar dependencias principales
echo.
echo 📦 Verificando dependencias principales...

python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit no instalado
) else (
    echo ✅ Streamlit OK
)

python -c "import whisper" 2>nul
if errorlevel 1 (
    echo ❌ Whisper no instalado
) else (
    echo ✅ Whisper OK
)

python -c "import cv2" 2>nul
if errorlevel 1 (
    echo ❌ OpenCV no instalado
) else (
    echo ✅ OpenCV OK
)

python -c "import mediapipe" 2>nul
if errorlevel 1 (
    echo ⚠️ MediaPipe no disponible (normal en Python 3.13+)
) else (
    echo ✅ MediaPipe OK
)

python -c "import numpy" 2>nul
if errorlevel 1 (
    echo ❌ NumPy no instalado
) else (
    echo ✅ NumPy OK
)

python -c "import pandas" 2>nul
if errorlevel 1 (
    echo ❌ Pandas no instalado
) else (
    echo ✅ Pandas OK
)

REM Verificar directorios
echo.
echo 📁 Verificando directorios...
if exist "data\students\" (
    echo ✅ data\students
) else (
    echo ❌ data\students no encontrado
    mkdir "data\students" 2>nul
    echo ✅ data\students creado
)

if exist "auth\" (
    echo ✅ auth
) else (
    echo ❌ auth no encontrado
    mkdir "auth" 2>nul
    echo ✅ auth creado
)

REM Verificación completa con script Python
echo.
echo 🔍 Ejecutando verificación completa...
python verify_installation.py

echo.
echo ==========================================
if errorlevel 1 (
    echo    ⚠️ Verificación completada con advertencias
) else (
    echo    ✅ Verificación exitosa
)
echo ==========================================
echo.
echo Para ejecutar la aplicación: run.bat
echo Para más ayuda: help.bat
echo.

:end
pause

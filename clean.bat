@echo off
REM Script de limpieza para Windows
setlocal enabledelayedexpansion

echo.
echo ==========================================
echo     Coach AI v2 - Limpieza Windows
echo ==========================================
echo.

echo Selecciona qué limpiar:
echo.
echo 1. Limpieza básica (cache, temporales)
echo 2. Limpiar entorno virtual
echo 3. Limpiar todo (incluye datos de usuarios)
echo 4. Solo cache de Python
echo 5. Solo archivos temporales
echo 6. Cancelar
echo.

set /p CHOICE="Elige una opción (1-6): "

if "%CHOICE%"=="1" goto :basic_clean
if "%CHOICE%"=="2" goto :clean_venv
if "%CHOICE%"=="3" goto :clean_all
if "%CHOICE%"=="4" goto :clean_cache
if "%CHOICE%"=="5" goto :clean_temp
if "%CHOICE%"=="6" goto :cancel
echo Opción no válida
goto :end

:basic_clean
echo.
echo 🧹 Limpieza básica iniciada...
goto :clean_cache_impl

:clean_venv
echo.
echo 🗑️ Eliminando entorno virtual...
if exist "venv\" (
    rmdir /s /q venv
    echo ✅ Entorno virtual eliminado
) else (
    echo ℹ️ No hay entorno virtual que eliminar
)
goto :end

:clean_all
echo.
echo ⚠️ ADVERTENCIA: Esto eliminará TODOS los datos incluyendo:
echo   - Entorno virtual
echo   - Datos de estudiantes
echo   - Usuarios registrados
echo   - Cache y temporales
echo.
set /p CONFIRM="¿Estás seguro? Escribe 'SI' para confirmar: "
if not "%CONFIRM%"=="SI" (
    echo Operación cancelada
    goto :end
)
echo.
echo 🧹 Limpieza completa iniciada...
goto :clean_all_impl

:clean_cache
echo.
echo 🧹 Limpiando cache de Python...
goto :clean_cache_impl

:clean_temp
echo.
echo 🧹 Limpiando archivos temporales...
goto :clean_temp_impl

:clean_cache_impl
echo 🔍 Buscando archivos de cache...
for /r %%i in (__pycache__) do (
    if exist "%%i" (
        echo Eliminando: %%i
        rmdir /s /q "%%i" 2>nul
    )
)

for /r %%i in (*.pyc) do (
    if exist "%%i" (
        echo Eliminando: %%i
        del /q "%%i" 2>nul
    )
)

for /r %%i in (*.pyo) do (
    if exist "%%i" (
        echo Eliminando: %%i
        del /q "%%i" 2>nul
    )
)

echo ✅ Cache de Python limpiado

if "%CHOICE%"=="1" goto :clean_temp_impl
goto :end

:clean_temp_impl
echo 🔍 Buscando archivos temporales...

REM Archivos temporales comunes
for %%i in (*.tmp *.temp *.log Thumbs.db .DS_Store) do (
    if exist "%%i" (
        echo Eliminando: %%i
        del /q "%%i" 2>nul
    )
)

REM Directorios temporales
if exist "temp\" (
    echo Eliminando directorio: temp\
    rmdir /s /q temp 2>nul
)

if exist "tmp\" (
    echo Eliminando directorio: tmp\
    rmdir /s /q tmp 2>nul
)

echo ✅ Archivos temporales limpiados
goto :end

:clean_all_impl
REM Entorno virtual
if exist "venv\" (
    echo 🗑️ Eliminando entorno virtual...
    rmdir /s /q venv
)

REM Datos de estudiantes
if exist "data\students\" (
    echo 🗑️ Eliminando datos de estudiantes...
    rmdir /s /q "data\students"
    mkdir "data\students" 2>nul
)

REM Usuarios
if exist "auth\users.json" (
    echo 🗑️ Eliminando usuarios...
    del /q "auth\users.json"
)

REM Reports
if exist "reports\" (
    echo 🗑️ Eliminando reportes...
    for /r "reports\" %%i in (*.*) do del /q "%%i" 2>nul
)

REM Logs
if exist "logs\" (
    echo 🗑️ Eliminando logs...
    for /r "logs\" %%i in (*.log) do del /q "%%i" 2>nul
)

REM Cache y temporales
goto :clean_cache_impl

:cancel
echo Operación cancelada
goto :end

:end
echo.
echo ==========================================
echo     🎉 Limpieza completada
echo ==========================================
echo.
echo Para reconfigurar el proyecto: setup.bat
echo Para más ayuda: help.bat
echo.
pause

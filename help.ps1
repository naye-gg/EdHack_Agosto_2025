# Script de ayuda PowerShell para Coach AI v2

param(
    [string]$Topic = ""
)

function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "    $Title" -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host ""
}

function Show-MainHelp {
    Write-Header "Coach AI v2 - Ayuda PowerShell"
    
    Write-ColorText "📋 SCRIPTS PRINCIPALES:" "Green"
    Write-Host ""
    Write-Host "   .\setup.ps1          - Configurar entorno virtual e instalar dependencias"
    Write-Host "   .\run.ps1            - Ejecutar la aplicación Coach AI v2"
    Write-Host "   .\activate.ps1       - Activar entorno virtual manualmente"
    Write-Host "   .\verify.ps1         - Verificar que todo esté instalado correctamente"
    Write-Host "   .\clean.ps1          - Limpiar archivos temporales y cache"
    Write-Host "   .\help.ps1           - Mostrar esta ayuda"
    Write-Host ""
    
    Write-ColorText "📋 SCRIPTS ALTERNATIVOS (.bat):" "Cyan"
    Write-Host ""
    Write-Host "   setup.bat            - Configuración (Símbolo del sistema)"
    Write-Host "   run.bat              - Ejecutar aplicación (Símbolo del sistema)"
    Write-Host "   activate.bat         - Activar entorno virtual (Símbolo del sistema)"
    Write-Host "   verify.bat           - Verificar instalación (Símbolo del sistema)"
    Write-Host "   clean.bat            - Limpieza (Símbolo del sistema)"
    Write-Host "   help.bat             - Ayuda (Símbolo del sistema)"
    Write-Host ""
    
    Write-ColorText "💡 COMANDOS CON PARÁMETROS:" "Yellow"
    Write-Host ""
    Write-Host "   .\setup.ps1 -Force               - Recrear entorno virtual"
    Write-Host "   .\setup.ps1 -Dev                 - Incluir dependencias de desarrollo"
    Write-Host "   .\run.ps1 -Port 8080             - Ejecutar en puerto específico"
    Write-Host "   .\run.ps1 -OpenBrowser           - Abrir navegador automáticamente"
    Write-Host "   .\run.ps1 -Debug                 - Ejecutar en modo debug"
    Write-Host "   .\clean.ps1 -All                 - Limpieza completa"
    Write-Host "   .\clean.ps1 -Venv                - Solo eliminar entorno virtual"
    Write-Host ""
    
    Write-ColorText "🔧 AYUDA POR TEMAS:" "Green"
    Write-Host ""
    Write-Host "   .\help.ps1 setup                 - Ayuda de configuración"
    Write-Host "   .\help.ps1 run                   - Ayuda de ejecución"
    Write-Host "   .\help.ps1 troubleshooting       - Solución de problemas"
    Write-Host "   .\help.ps1 python                - Información sobre Python"
    Write-Host "   .\help.ps1 examples              - Ejemplos de uso"
    Write-Host ""
}

function Show-SetupHelp {
    Write-Header "Ayuda de Configuración"
    
    Write-ColorText "🚀 CONFIGURACIÓN INICIAL:" "Green"
    Write-Host ""
    Write-Host "1. Configuración automática:"
    Write-Host "   .\setup.ps1"
    Write-Host ""
    Write-Host "2. Configuración forzada (recrear todo):"
    Write-Host "   .\setup.ps1 -Force"
    Write-Host ""
    Write-Host "3. Configuración para desarrollo:"
    Write-Host "   .\setup.ps1 -Dev"
    Write-Host ""
    
    Write-ColorText "📋 REQUISITOS PREVIOS:" "Cyan"
    Write-Host ""
    Write-Host "• Python 3.11 - 3.12 instalado"
    Write-Host "• PowerShell 5.0 o superior"
    Write-Host "• Conexión a internet"
    Write-Host "• Al menos 2GB de espacio libre"
    Write-Host ""
    
    Write-ColorText "⚙️ CONFIGURACIÓN DE POWERSHELL:" "Yellow"
    Write-Host ""
    Write-Host "Si hay errores de permisos, ejecutar:"
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host ""
}

function Show-RunHelp {
    Write-Header "Ayuda de Ejecución"
    
    Write-ColorText "🚀 FORMAS DE EJECUTAR:" "Green"
    Write-Host ""
    Write-Host "1. Ejecución básica:"
    Write-Host "   .\run.ps1"
    Write-Host ""
    Write-Host "2. En puerto específico:"
    Write-Host "   .\run.ps1 -Port 8080"
    Write-Host ""
    Write-Host "3. Acceso desde red:"
    Write-Host "   .\run.ps1 -Address 0.0.0.0"
    Write-Host ""
    Write-Host "4. Con navegador automático:"
    Write-Host "   .\run.ps1 -OpenBrowser"
    Write-Host ""
    Write-Host "5. Modo debug:"
    Write-Host "   .\run.ps1 -Debug"
    Write-Host ""
    Write-Host "6. Combinado:"
    Write-Host "   .\run.ps1 -Port 8080 -OpenBrowser -Debug"
    Write-Host ""
    
    Write-ColorText "🌐 ACCESO A LA APLICACIÓN:" "Cyan"
    Write-Host ""
    Write-Host "• Local: http://localhost:8501"
    Write-Host "• Red: http://[tu-ip]:8501"
    Write-Host "• Puerto personalizado: http://localhost:[puerto]"
    Write-Host ""
    
    Write-ColorText "⏹️ DETENER LA APLICACIÓN:" "Yellow"
    Write-Host ""
    Write-Host "• Ctrl+C en la ventana de PowerShell"
    Write-Host "• Cerrar la ventana de PowerShell"
    Write-Host "• Ctrl+Break para forzar cierre"
    Write-Host ""
}

function Show-TroubleshootingHelp {
    Write-Header "Solución de Problemas"
    
    Write-ColorText "❌ PROBLEMAS COMUNES:" "Red"
    Write-Host ""
    
    Write-ColorText "1. 'Python no encontrado'" "Yellow"
    Write-Host "   Solución:"
    Write-Host "   • Instalar Python desde python.org"
    Write-Host "   • Marcar 'Add Python to PATH' durante instalación"
    Write-Host "   • Reiniciar PowerShell después de instalar"
    Write-Host ""
    
    Write-ColorText "2. 'Error de permisos PowerShell'" "Yellow"
    Write-Host "   Solución:"
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host ""
    
    Write-ColorText "3. 'MediaPipe no funciona'" "Yellow"
    Write-Host "   Solución:"
    Write-Host "   • Usar Python 3.11 o 3.12 (no 3.13+)"
    Write-Host "   • Ejecutar: .\setup.ps1 -Force"
    Write-Host ""
    
    Write-ColorText "4. 'Puerto 8501 ocupado'" "Yellow"
    Write-Host "   Solución:"
    Write-Host "   • .\run.ps1 -Port 8080"
    Write-Host "   • Cerrar otras aplicaciones Streamlit"
    Write-Host ""
    
    Write-ColorText "5. 'Error instalando dependencias'" "Yellow"
    Write-Host "   Solución:"
    Write-Host "   • Ejecutar PowerShell como administrador"
    Write-Host "   • Verificar conexión a internet"
    Write-Host "   • Instalar Visual Studio Build Tools"
    Write-Host ""
    
    Write-ColorText "🔧 COMANDOS DE DIAGNÓSTICO:" "Green"
    Write-Host ""
    Write-Host "   .\verify.ps1                     - Verificar instalación"
    Write-Host "   python --version                 - Ver versión Python"
    Write-Host "   Get-ExecutionPolicy              - Ver política PowerShell"
    Write-Host "   .\clean.ps1 -All                 - Limpiar y reinstalar"
    Write-Host ""
}

function Show-PythonHelp {
    Write-Header "Información sobre Python"
    
    Write-ColorText "🐍 VERSIONES COMPATIBLES:" "Green"
    Write-Host ""
    Write-Host "✅ Python 3.11 - Totalmente compatible"
    Write-Host "✅ Python 3.12 - Totalmente compatible"
    Write-Host "⚠️  Python 3.13+ - Funcionalidad limitada (sin MediaPipe)"
    Write-Host ""
    
    Write-ColorText "📦 FUNCIONALIDADES POR VERSIÓN:" "Cyan"
    Write-Host ""
    Write-Host "Python 3.11-3.12 (Completo):"
    Write-Host "• ✅ Análisis de voz"
    Write-Host "• ✅ Análisis corporal"
    Write-Host "• ✅ Análisis facial"
    Write-Host "• ✅ Análisis de contenido"
    Write-Host "• ✅ Reportes PDF/Excel"
    Write-Host ""
    Write-Host "Python 3.13+ (Limitado):"
    Write-Host "• ✅ Análisis de voz"
    Write-Host "• ❌ Análisis corporal"
    Write-Host "• ❌ Análisis facial"
    Write-Host "• ✅ Análisis de contenido"
    Write-Host "• ✅ Reportes PDF/Excel"
    Write-Host ""
    
    Write-ColorText "🔄 CAMBIAR VERSIÓN DE PYTHON:" "Yellow"
    Write-Host ""
    Write-Host "1. Con pyenv (recomendado):"
    Write-Host "   pyenv install 3.12.7"
    Write-Host "   pyenv local 3.12.7"
    Write-Host ""
    Write-Host "2. Instalación manual:"
    Write-Host "   • Descargar desde python.org"
    Write-Host "   • Instalar versión específica"
    Write-Host "   • Usar python3.12 en lugar de python"
    Write-Host ""
}

function Show-ExamplesHelp {
    Write-Header "Ejemplos de Uso"
    
    Write-ColorText "🎯 ESCENARIOS TÍPICOS:" "Green"
    Write-Host ""
    
    Write-ColorText "1. Primera instalación:" "Cyan"
    Write-Host "   .\setup.ps1"
    Write-Host "   .\run.ps1 -OpenBrowser"
    Write-Host ""
    
    Write-ColorText "2. Desarrollo:" "Cyan"
    Write-Host "   .\setup.ps1 -Dev"
    Write-Host "   .\run.ps1 -Debug"
    Write-Host ""
    
    Write-ColorText "3. Servidor en red:" "Cyan"
    Write-Host "   .\run.ps1 -Address 0.0.0.0 -Port 8501"
    Write-Host ""
    
    Write-ColorText "4. Solución de problemas:" "Cyan"
    Write-Host "   .\verify.ps1"
    Write-Host "   .\clean.ps1 -All"
    Write-Host "   .\setup.ps1 -Force"
    Write-Host ""
    
    Write-ColorText "5. Actualización:" "Cyan"
    Write-Host "   git pull"
    Write-Host "   .\setup.ps1 -Force"
    Write-Host ""
    
    Write-ColorText "🔗 FLUJO COMPLETO:" "Yellow"
    Write-Host ""
    Write-Host "# Configuración inicial"
    Write-Host "git clone <repository-url>"
    Write-Host "cd coach-ai-v2"
    Write-Host ".\setup.ps1"
    Write-Host ""
    Write-Host "# Ejecutar aplicación"
    Write-Host ".\run.ps1 -OpenBrowser"
    Write-Host ""
    Write-Host "# Verificar si hay problemas"
    Write-Host ".\verify.ps1"
    Write-Host ""
    Write-Host "# Limpiar cuando sea necesario"
    Write-Host ".\clean.ps1"
    Write-Host ""
}

# Script principal
switch ($Topic.ToLower()) {
    "setup" { Show-SetupHelp }
    "run" { Show-RunHelp }
    "troubleshooting" { Show-TroubleshootingHelp }
    "python" { Show-PythonHelp }
    "examples" { Show-ExamplesHelp }
    default { Show-MainHelp }
}

Write-ColorText "📞 SOPORTE ADICIONAL:" "Green"
Write-Host ""
Write-Host "📖 Documentación completa: README.md"
Write-Host "🚀 Guía rápida: GETTING_STARTED.md"
Write-Host "🔧 Compatibilidad: COMPATIBILITY.md"
Write-Host ""

Read-Host "Presiona Enter para continuar"

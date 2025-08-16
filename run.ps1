# Script PowerShell para ejecutar Coach AI v2

param(
    [int]$Port = 8501,
    [string]$Address = "localhost",
    [switch]$OpenBrowser,
    [switch]$Debug
)

$Host.UI.RawUI.WindowTitle = "Coach AI v2 - Ejecutando"

function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "=" * 50 -ForegroundColor Cyan
    Write-Host "    $Title" -ForegroundColor Yellow
    Write-Host "=" * 50 -ForegroundColor Cyan
    Write-Host ""
}

function Test-Prerequisites {
    # Verificar entorno virtual
    if (-not (Test-Path "venv")) {
        Write-ColorText "❌ Entorno virtual no encontrado" "Red"
        Write-Host ""
        Write-ColorText "Ejecuta primero:" "Yellow"
        Write-Host "   .\setup.ps1    (PowerShell)"
        Write-Host "   setup.bat      (Símbolo del sistema)"
        return $false
    }
    
    # Verificar app.py
    if (-not (Test-Path "app.py")) {
        Write-ColorText "❌ app.py no encontrado" "Red"
        Write-ColorText "Asegúrate de estar en el directorio correcto del proyecto" "Yellow"
        return $false
    }
    
    return $true
}

function Test-StreamlitInstallation {
    try {
        & "venv\Scripts\streamlit" --version | Out-Null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

function Start-Application {
    param([int]$Port, [string]$Address, [bool]$Debug)
    
    Write-ColorText "🔧 Activando entorno virtual..." "Cyan"
    
    # Verificar Streamlit
    if (-not (Test-StreamlitInstallation)) {
        Write-ColorText "❌ Streamlit no encontrado" "Red"
        Write-ColorText "📦 Instalando dependencias..." "Cyan"
        
        & "venv\Scripts\pip" install -r requirements.txt
        
        if ($LASTEXITCODE -ne 0) {
            Write-ColorText "❌ Error instalando dependencias" "Red"
            return $false
        }
    }
    
    Write-ColorText "✅ Entorno listo" "Green"
    Write-Host ""
    
    $url = "http://${Address}:${Port}"
    Write-ColorText "🌐 Iniciando Coach AI v2 en: $url" "Green"
    Write-Host ""
    
    Write-ColorText "💡 Controles:" "Cyan"
    Write-Host "   Ctrl+C        - Detener aplicación"
    Write-Host "   Ctrl+Break    - Forzar cierre"
    Write-Host ""
    
    # Abrir navegador si se solicita
    if ($OpenBrowser) {
        Write-ColorText "🔗 Abriendo navegador..." "Cyan"
        Start-Process $url
    }
    
    # Configurar argumentos de Streamlit
    $streamlitArgs = @("run", "app.py", "--server.port", $Port, "--server.address", $Address)
    
    if ($Debug) {
        $streamlitArgs += @("--logger.level", "debug")
        Write-ColorText "🐛 Modo debug activado" "Yellow"
    }
    
    # Ejecutar aplicación
    try {
        & "venv\Scripts\streamlit" @streamlitArgs
    }
    catch {
        Write-ColorText "❌ Error ejecutando aplicación: $_" "Red"
        return $false
    }
    
    return $true
}

function Test-Port {
    param([int]$Port)
    
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.Start()
        $listener.Stop()
        return $true
    }
    catch {
        return $false
    }
}

# Script principal
try {
    Write-Header "Coach AI v2 - Ejecutar Aplicación"
    
    # Verificar prerequisitos
    if (-not (Test-Prerequisites)) {
        Read-Host "Presiona Enter para continuar"
        exit 1
    }
    
    # Verificar puerto
    if (-not (Test-Port -Port $Port)) {
        Write-ColorText "⚠️  Puerto $Port parece estar ocupado" "Yellow"
        $newPort = Read-Host "Ingresa un puerto alternativo (ej: 8080) o presiona Enter para continuar"
        if ($newPort -and $newPort -match '^\d+$') {
            $Port = [int]$newPort
        }
    }
    
    # Mostrar configuración
    Write-ColorText "📋 Configuración:" "Cyan"
    Write-Host "   Puerto: $Port"
    Write-Host "   Dirección: $Address"
    Write-Host "   Debug: $Debug"
    Write-Host "   Abrir navegador: $OpenBrowser"
    Write-Host ""
    
    # Iniciar aplicación
    if (-not (Start-Application -Port $Port -Address $Address -Debug $Debug)) {
        throw "Error iniciando aplicación"
    }
    
}
catch {
    Write-ColorText "❌ Error: $_" "Red"
    Write-Host ""
    
    Write-ColorText "💡 Soluciones comunes:" "Yellow"
    Write-Host "   - Verificar que el entorno virtual está configurado"
    Write-Host "   - Cambiar puerto si está ocupado: .\run.ps1 -Port 8080"
    Write-Host "   - Reinstalar dependencias: .\setup.ps1 -Force"
    Write-Host "   - Consultar help.ps1 para más opciones"
    Write-Host ""
}
finally {
    Write-Host ""
    Write-ColorText "👋 Coach AI v2 finalizado" "Green"
    Read-Host "Presiona Enter para continuar"
}

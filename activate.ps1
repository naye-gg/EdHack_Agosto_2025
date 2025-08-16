# Script de activación PowerShell para Coach AI v2

param(
    [switch]$ShowInfo
)

function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Show-EnvironmentInfo {
    Write-Host ""
    Write-ColorText "🚀 Entorno Virtual Coach AI v2 Activado" "Green"
    Write-Host ""
    
    # Información del entorno
    Write-ColorText "📍 Información del Entorno:" "Cyan"
    Write-Host "   Ubicación: $env:VIRTUAL_ENV"
    Write-Host "   Python: " -NoNewline
    & python --version
    Write-Host "   Pip: " -NoNewline
    & pip --version | Select-String "pip" | ForEach-Object { $_.ToString().Split()[0,1] -join " " }
    Write-Host ""
    
    # Comandos útiles
    Write-ColorText "💡 Comandos útiles:" "Yellow"
    Write-Host "   streamlit run app.py          - Iniciar aplicación"
    Write-Host "   python verify_installation.py - Verificar instalación"
    Write-Host "   pip list                      - Ver paquetes instalados"
    Write-Host "   deactivate                    - Desactivar entorno virtual"
    Write-Host ""
    Write-Host "   .\run.ps1                     - Ejecutar aplicación (PowerShell)"
    Write-Host "   run.bat                       - Ejecutar aplicación (CMD)"
    Write-Host "   .\help.ps1                    - Ver más comandos"
    Write-Host ""
    
    # Estado de dependencias principales
    Write-ColorText "📦 Estado de Dependencias Principales:" "Cyan"
    
    $packages = @(
        @{Name="streamlit"; Import="streamlit"},
        @{Name="whisper"; Import="whisper"},
        @{Name="opencv"; Import="cv2"},
        @{Name="mediapipe"; Import="mediapipe"},
        @{Name="numpy"; Import="numpy"},
        @{Name="pandas"; Import="pandas"}
    )
    
    foreach ($pkg in $packages) {
        try {
            & python -c "import $($pkg.Import)" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-ColorText "   ✅ $($pkg.Name)" "Green"
            } else {
                Write-ColorText "   ❌ $($pkg.Name)" "Red"
            }
        }
        catch {
            Write-ColorText "   ❌ $($pkg.Name)" "Red"
        }
    }
    
    Write-Host ""
    Write-ColorText "🌐 Para acceder a la aplicación:" "Yellow"
    Write-Host "   http://localhost:8501"
    Write-Host ""
}

# Verificar que existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-ColorText "❌ Entorno virtual no encontrado" "Red"
    Write-Host ""
    Write-ColorText "Ejecuta primero:" "Yellow"
    Write-Host "   .\setup.ps1    (PowerShell)"
    Write-Host "   setup.bat      (Símbolo del sistema)"
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
    exit 1
}

# Verificar script de activación
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-ColorText "❌ Script de activación no encontrado" "Red"
    Write-ColorText "El entorno virtual puede estar corrupto" "Yellow"
    Write-Host ""
    Write-ColorText "Solución:" "Yellow"
    Write-Host "   .\setup.ps1 -Force"
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
    exit 1
}

try {
    # Activar entorno virtual
    & "venv\Scripts\Activate.ps1"
    
    if ($env:VIRTUAL_ENV) {
        if ($ShowInfo) {
            Show-EnvironmentInfo
        } else {
            Write-ColorText "✅ Entorno virtual activado" "Green"
            Write-ColorText "Usa 'deactivate' para salir" "Gray"
        }
    } else {
        Write-ColorText "❌ Error activando entorno virtual" "Red"
        exit 1
    }
}
catch {
    Write-ColorText "❌ Error: $_" "Red"
    Write-Host ""
    Write-ColorText "💡 Soluciones:" "Yellow"
    Write-Host "   - Verificar permisos de ejecución de PowerShell"
    Write-Host "   - Ejecutar: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host "   - Recrear entorno virtual: .\setup.ps1 -Force"
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
    exit 1
}

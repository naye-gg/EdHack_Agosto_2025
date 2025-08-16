# Script de configuración PowerShell para Coach AI v2
# Requiere PowerShell 5.0 o superior

param(
    [switch]$Force,
    [switch]$Dev,
    [string]$PythonPath = "python"
)

# Configuración de colores
$Host.UI.RawUI.WindowTitle = "Coach AI v2 - Configuración"

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

function Test-PythonVersion {
    try {
        $pythonVersion = & $PythonPath --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python no encontrado"
        }
        
        $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)"
        if (-not $versionMatch) {
            throw "No se pudo determinar la versión de Python"
        }
        
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        Write-ColorText "🐍 Python $($Matches[1]).$($Matches[2]).$($Matches[3]) detectado" "Green"
        
        if ($major -ne 3 -or $minor -lt 11) {
            throw "Se requiere Python 3.11 o superior"
        }
        
        if ($minor -ge 13) {
            Write-ColorText "⚠️  Advertencia: Python 3.13+ puede tener problemas con MediaPipe" "Yellow"
            $continue = Read-Host "¿Continuar de todos modos? (s/N)"
            if ($continue -notmatch "^[sS]$") {
                throw "Instalación cancelada por el usuario"
            }
        }
        
        return $true
    }
    catch {
        Write-ColorText "❌ Error: $_" "Red"
        return $false
    }
}

function New-VirtualEnvironment {
    param([bool]$Force)
    
    if (Test-Path "venv") {
        if ($Force) {
            Write-ColorText "🗑️  Eliminando entorno virtual existente..." "Yellow"
            Remove-Item -Recurse -Force "venv"
        }
        else {
            $recreate = Read-Host "Entorno virtual encontrado. ¿Recrear? (s/N)"
            if ($recreate -match "^[sS]$") {
                Remove-Item -Recurse -Force "venv"
            }
            else {
                Write-ColorText "✅ Usando entorno virtual existente" "Green"
                return $true
            }
        }
    }
    
    Write-ColorText "🔧 Creando entorno virtual..." "Cyan"
    & $PythonPath -m venv venv
    
    if ($LASTEXITCODE -ne 0) {
        Write-ColorText "❌ Error creando entorno virtual" "Red"
        return $false
    }
    
    Write-ColorText "✅ Entorno virtual creado" "Green"
    return $true
}

function Install-Dependencies {
    param([bool]$Dev)
    
    Write-ColorText "📦 Configurando dependencias..." "Cyan"
    
    # Activar entorno virtual
    & "venv\Scripts\Activate.ps1"
    
    # Actualizar pip
    Write-ColorText "⬆️  Actualizando pip..." "Cyan"
    & "venv\Scripts\python" -m pip install --upgrade pip wheel
    
    # Determinar archivo de requirements
    $requirementsFile = "requirements.txt"
    try {
        & "venv\Scripts\python" -c "import sys; exit(0 if sys.version_info < (3,13) else 1)"
        if ($LASTEXITCODE -ne 0) {
            $requirementsFile = "requirements-python313.txt"
            Write-ColorText "📦 Instalando dependencias para Python 3.13+ (funcionalidad limitada)" "Yellow"
        }
        else {
            Write-ColorText "📦 Instalando dependencias completas..." "Cyan"
        }
    }
    catch {
        Write-ColorText "⚠️  No se pudo determinar versión, usando requirements.txt" "Yellow"
    }
    
    & "venv\Scripts\pip" install -r $requirementsFile
    
    if ($LASTEXITCODE -ne 0) {
        Write-ColorText "❌ Error instalando dependencias principales" "Red"
        return $false
    }
    
    # Instalar dependencias de desarrollo si se solicita
    if ($Dev -and (Test-Path "requirements-dev.txt")) {
        Write-ColorText "🛠️  Instalando dependencias de desarrollo..." "Cyan"
        & "venv\Scripts\pip" install -r requirements-dev.txt
        
        if ($LASTEXITCODE -ne 0) {
            Write-ColorText "⚠️  Error instalando dependencias de desarrollo" "Yellow"
        }
    }
    
    Write-ColorText "✅ Dependencias instaladas correctamente" "Green"
    return $true
}

function New-ProjectDirectories {
    $directories = @("data\students", "auth", "reports", "logs", "backups")
    
    Write-ColorText "📁 Creando directorios del proyecto..." "Cyan"
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-ColorText "  ✅ $dir" "Green"
        }
        else {
            Write-ColorText "  📁 $dir (ya existe)" "Gray"
        }
    }
}

function Test-Installation {
    Write-ColorText "🔍 Verificando instalación..." "Cyan"
    
    if (Test-Path "verify_installation.py") {
        & "venv\Scripts\python" verify_installation.py
        return $LASTEXITCODE -eq 0
    }
    else {
        Write-ColorText "⚠️  Script de verificación no encontrado" "Yellow"
        return $true
    }
}

function Show-CompletionMessage {
    Write-Header "Configuración Completada"
    
    Write-ColorText "🎉 ¡Coach AI v2 está listo para usar!" "Green"
    Write-Host ""
    
    Write-ColorText "💡 Para ejecutar la aplicación:" "Cyan"
    Write-Host "   .\run.ps1              (PowerShell)"
    Write-Host "   run.bat                (Símbolo del sistema)"
    Write-Host ""
    
    Write-ColorText "💡 Para activar el entorno virtual:" "Cyan"
    Write-Host "   .\activate.ps1         (PowerShell)"
    Write-Host "   activate.bat           (Símbolo del sistema)"
    Write-Host ""
    
    Write-ColorText "💡 Para obtener ayuda:" "Cyan"
    Write-Host "   .\help.ps1             (PowerShell)"
    Write-Host "   help.bat               (Símbolo del sistema)"
    Write-Host ""
    
    Write-ColorText "🌐 La aplicación estará disponible en:" "Yellow"
    Write-Host "   http://localhost:8501"
    Write-Host ""
}

# Script principal
try {
    Write-Header "Coach AI v2 - Configuración PowerShell"
    
    # Verificar requisitos
    if (-not (Test-Path "requirements.txt")) {
        throw "requirements.txt no encontrado. Ejecuta desde el directorio raíz del proyecto."
    }
    
    # Verificar Python
    if (-not (Test-PythonVersion)) {
        throw "Python no válido o no encontrado"
    }
    
    # Crear entorno virtual
    if (-not (New-VirtualEnvironment -Force $Force)) {
        throw "Error creando entorno virtual"
    }
    
    # Instalar dependencias
    if (-not (Install-Dependencies -Dev $Dev)) {
        throw "Error instalando dependencias"
    }
    
    # Crear directorios
    New-ProjectDirectories
    
    # Verificar instalación
    if (-not (Test-Installation)) {
        Write-ColorText "⚠️  Verificación completada con advertencias" "Yellow"
    }
    
    # Mostrar mensaje de finalización
    Show-CompletionMessage
    
}
catch {
    Write-ColorText "❌ Error: $_" "Red"
    Write-Host ""
    Write-ColorText "💡 Soluciones:" "Yellow"
    Write-Host "   - Verificar que Python 3.11+ está instalado"
    Write-Host "   - Ejecutar como administrador si es necesario"
    Write-Host "   - Verificar conexión a internet"
    Write-Host "   - Consultar COMPATIBILITY.md para más ayuda"
    Write-Host ""
    
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Read-Host "Presiona Enter para continuar"

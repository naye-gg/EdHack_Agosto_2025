# Script de limpieza PowerShell para Coach AI v2

param(
    [switch]$All,
    [switch]$Venv,
    [switch]$Cache,
    [switch]$Temp,
    [switch]$Data,
    [switch]$Auth,
    [switch]$MLCache,
    [switch]$Force
)

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

function Remove-PythonCache {
    Write-ColorText "🧹 Limpiando cache de Python..." "Cyan"
    $count = 0
    
    # Buscar y eliminar directorios __pycache__
    Get-ChildItem -Recurse -Directory -Name "__pycache__" | ForEach-Object {
        try {
            Remove-Item -Recurse -Force $_
            Write-ColorText "   Eliminado: $_" "Gray"
            $count++
        }
        catch {
            Write-ColorText "   Error eliminando $_: $($_.Exception.Message)" "Red"
        }
    }
    
    # Buscar y eliminar archivos .pyc y .pyo
    Get-ChildItem -Recurse -File -Include "*.pyc", "*.pyo" | ForEach-Object {
        try {
            Remove-Item -Force $_
            Write-ColorText "   Eliminado: $($_.Name)" "Gray"
            $count++
        }
        catch {
            Write-ColorText "   Error eliminando $($_.Name): $($_.Exception.Message)" "Red"
        }
    }
    
    Write-ColorText "✅ Cache de Python limpiado ($count elementos)" "Green"
}

function Remove-TempFiles {
    Write-ColorText "🧹 Limpiando archivos temporales..." "Cyan"
    $count = 0
    
    $tempPatterns = @("*.tmp", "*.temp", "temp_*", "tmp_*", "*.log", ".DS_Store", "Thumbs.db")
    
    foreach ($pattern in $tempPatterns) {
        Get-ChildItem -Recurse -File -Include $pattern | ForEach-Object {
            try {
                Remove-Item -Force $_
                Write-ColorText "   Eliminado: $($_.Name)" "Gray"
                $count++
            }
            catch {
                Write-ColorText "   Error eliminando $($_.Name): $($_.Exception.Message)" "Red"
            }
        }
    }
    
    # Eliminar directorios temporales
    $tempDirs = @("temp", "tmp")
    foreach ($dir in $tempDirs) {
        if (Test-Path $dir) {
            try {
                Remove-Item -Recurse -Force $dir
                Write-ColorText "   Eliminado directorio: $dir" "Gray"
                $count++
            }
            catch {
                Write-ColorText "   Error eliminando directorio $dir`: $($_.Exception.Message)" "Red"
            }
        }
    }
    
    Write-ColorText "✅ Archivos temporales limpiados ($count elementos)" "Green"
}

function Remove-VirtualEnvironment {
    if (Test-Path "venv") {
        Write-ColorText "🗑️  Eliminando entorno virtual..." "Yellow"
        try {
            Remove-Item -Recurse -Force "venv"
            Write-ColorText "✅ Entorno virtual eliminado" "Green"
        }
        catch {
            Write-ColorText "❌ Error eliminando entorno virtual: $($_.Exception.Message)" "Red"
        }
    }
    else {
        Write-ColorText "ℹ️  No hay entorno virtual que eliminar" "Gray"
    }
}

function Remove-StreamlitCache {
    Write-ColorText "🧹 Limpiando cache de Streamlit..." "Cyan"
    $count = 0
    
    $streamlitDirs = @(
        "$env:USERPROFILE\.streamlit",
        ".streamlit"
    )
    
    foreach ($dir in $streamlitDirs) {
        if (Test-Path $dir) {
            # Solo limpiar archivos temporales, no toda la configuración
            Get-ChildItem -Path $dir -Include "*.tmp", "*.cache" -Recurse | ForEach-Object {
                try {
                    Remove-Item -Force $_
                    Write-ColorText "   Eliminado: $($_.Name)" "Gray"
                    $count++
                }
                catch {
                    Write-ColorText "   Error eliminando $($_.Name): $($_.Exception.Message)" "Red"
                }
            }
        }
    }
    
    if ($count -gt 0) {
        Write-ColorText "✅ Cache de Streamlit limpiado ($count archivos)" "Green"
    }
    else {
        Write-ColorText "ℹ️  No hay cache de Streamlit que limpiar" "Gray"
    }
}

function Remove-MLCache {
    Write-ColorText "🧹 Limpiando cache de modelos ML..." "Cyan"
    $count = 0
    
    $cacheDirs = @(
        "$env:USERPROFILE\.cache\whisper",
        "$env:USERPROFILE\.cache\torch",
        "$env:USERPROFILE\.cache\huggingface",
        ".cache",
        "models"
    )
    
    foreach ($dir in $cacheDirs) {
        if (Test-Path $dir) {
            try {
                Remove-Item -Recurse -Force $dir
                Write-ColorText "   Eliminado: $dir" "Gray"
                $count++
            }
            catch {
                Write-ColorText "   Error eliminando $dir`: $($_.Exception.Message)" "Red"
            }
        }
    }
    
    if ($count -gt 0) {
        Write-ColorText "✅ Cache de modelos ML limpiado ($count directorios)" "Green"
    }
    else {
        Write-ColorText "ℹ️  No hay cache de modelos ML que limpiar" "Gray"
    }
}

function Remove-DataFiles {
    Write-ColorText "⚠️  Limpiando datos de estudiantes..." "Yellow"
    
    if (Test-Path "data\students") {
        $fileCount = (Get-ChildItem -Recurse "data\students" -File).Count
        
        try {
            Remove-Item -Recurse -Force "data\students"
            New-Item -ItemType Directory -Path "data\students" -Force | Out-Null
            Write-ColorText "✅ Datos de estudiantes limpiados ($fileCount archivos)" "Green"
        }
        catch {
            Write-ColorText "❌ Error limpiando datos: $($_.Exception.Message)" "Red"
        }
    }
    else {
        Write-ColorText "ℹ️  No hay datos de estudiantes que limpiar" "Gray"
    }
}

function Remove-AuthFiles {
    Write-ColorText "⚠️  Limpiando archivos de autenticación..." "Yellow"
    
    if (Test-Path "auth\users.json") {
        try {
            Remove-Item -Force "auth\users.json"
            Write-ColorText "✅ Archivo de usuarios eliminado" "Green"
        }
        catch {
            Write-ColorText "❌ Error eliminando archivo de usuarios: $($_.Exception.Message)" "Red"
        }
    }
    else {
        Write-ColorText "ℹ️  No hay archivo de usuarios que limpiar" "Gray"
    }
}

function Show-Menu {
    Write-Header "Coach AI v2 - Limpieza PowerShell"
    
    Write-ColorText "Selecciona qué limpiar:" "Cyan"
    Write-Host ""
    Write-Host "1. Limpieza básica (cache, temporales)"
    Write-Host "2. Limpiar entorno virtual"
    Write-Host "3. Limpiar todo (incluye datos de usuarios) ⚠️"
    Write-Host "4. Solo cache de Python"
    Write-Host "5. Solo archivos temporales"
    Write-Host "6. Solo cache de modelos ML"
    Write-Host "7. Cancelar"
    Write-Host ""
    
    $choice = Read-Host "Elige una opción (1-7)"
    return $choice
}

function Confirm-DataDeletion {
    Write-Host ""
    Write-ColorText "⚠️  ADVERTENCIA: Esto eliminará permanentemente:" "Red"
    Write-Host "   - Entorno virtual"
    Write-Host "   - Datos de estudiantes"
    Write-Host "   - Usuarios registrados"
    Write-Host "   - Cache y archivos temporales"
    Write-Host ""
    
    $confirm = Read-Host "¿Estás seguro? Escribe 'SI' para confirmar"
    return $confirm -eq "SI"
}

# Script principal
try {
    # Si no se especificaron parámetros, mostrar menú
    if (-not ($All -or $Venv -or $Cache -or $Temp -or $Data -or $Auth -or $MLCache)) {
        $choice = Show-Menu
        
        switch ($choice) {
            "1" { $Cache = $true; $Temp = $true }
            "2" { $Venv = $true }
            "3" { $All = $true }
            "4" { $Cache = $true }
            "5" { $Temp = $true }
            "6" { $MLCache = $true }
            "7" { 
                Write-ColorText "Operación cancelada" "Yellow"
                exit 0
            }
            default {
                Write-ColorText "Opción no válida" "Red"
                exit 1
            }
        }
    }
    
    # Verificar directorio
    if (-not (Test-Path "app.py")) {
        Write-ColorText "❌ Error: Ejecutar desde el directorio raíz del proyecto" "Red"
        exit 1
    }
    
    # Confirmación para operaciones destructivas
    if (($All -or $Data -or $Auth) -and -not $Force) {
        if (-not (Confirm-DataDeletion)) {
            Write-ColorText "Operación cancelada" "Yellow"
            exit 0
        }
    }
    
    Write-Header "Ejecutando Limpieza"
    
    # Ejecutar limpiezas según parámetros
    if ($All) {
        Remove-PythonCache
        Remove-TempFiles
        Remove-StreamlitCache
        Remove-MLCache
        Remove-VirtualEnvironment
        Remove-DataFiles
        Remove-AuthFiles
    }
    else {
        if ($Cache) {
            Remove-PythonCache
            Remove-StreamlitCache
        }
        if ($Temp) {
            Remove-TempFiles
        }
        if ($Venv) {
            Remove-VirtualEnvironment
        }
        if ($MLCache) {
            Remove-MLCache
        }
        if ($Data) {
            Remove-DataFiles
        }
        if ($Auth) {
            Remove-AuthFiles
        }
    }
    
    Write-Header "Limpieza Completada"
    Write-ColorText "🎉 Limpieza finalizada correctamente" "Green"
    Write-Host ""
    Write-ColorText "Para reconfigurar el proyecto:" "Cyan"
    Write-Host "   .\setup.ps1"
    Write-Host ""
    
}
catch {
    Write-ColorText "❌ Error durante la limpieza: $_" "Red"
    exit 1
}

Read-Host "Presiona Enter para continuar"

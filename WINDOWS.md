# 🪟 Guía Específica para Windows - Coach AI v2

Esta guía te ayudará a configurar y ejecutar Coach AI v2 específicamente en Windows, con scripts optimizados para PowerShell y Símbolo del sistema.

## 🚀 Inicio Rápido

### Opción 1: PowerShell (Recomendado)
```powershell
# Configurar
.\setup.ps1

# Ejecutar
.\run.ps1 -OpenBrowser
```

### Opción 2: Símbolo del Sistema
```cmd
REM Configurar
setup.bat

REM Ejecutar
run.bat
```

## 📋 Requisitos de Windows

### Sistema Operativo
- Windows 10 o superior
- Windows Server 2016 o superior

### Software Requerido
- **Python 3.11 - 3.12** (no 3.13 por compatibilidad con MediaPipe)
- **PowerShell 5.0+** (incluido en Windows 10+)
- **Visual Studio Build Tools** (para algunas dependencias)

## 🔧 Configuración Inicial

### 1. Instalar Python
1. Descargar desde [python.org](https://python.org/downloads/)
2. ⚠️ **IMPORTANTE**: Marcar "Add Python to PATH"
3. Marcar "Install for all users" (recomendado)
4. Verificar instalación:
   ```powershell
   python --version
   ```

### 2. Configurar PowerShell (si es necesario)
```powershell
# Permitir ejecución de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instalar Visual Studio Build Tools (si es necesario)
Descargar desde [Microsoft Visual Studio](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)

## 📜 Scripts Disponibles

### PowerShell (.ps1) - Recomendado

| Script | Descripción | Ejemplo de Uso |
|--------|-------------|----------------|
| `setup.ps1` | Configuración completa | `.\setup.ps1 -Force` |
| `run.ps1` | Ejecutar aplicación | `.\run.ps1 -Port 8080` |
| `activate.ps1` | Activar entorno virtual | `.\activate.ps1 -ShowInfo` |
| `clean.ps1` | Limpieza del proyecto | `.\clean.ps1 -All` |
| `help.ps1` | Ayuda interactiva | `.\help.ps1 setup` |

### Símbolo del Sistema (.bat) - Compatibilidad

| Script | Descripción | Uso |
|--------|-------------|-----|
| `setup.bat` | Configuración básica | `setup.bat` |
| `run.bat` | Ejecutar aplicación | `run.bat` |
| `activate.bat` | Activar entorno virtual | `activate.bat` |
| `verify.bat` | Verificar instalación | `verify.bat` |
| `clean.bat` | Limpieza interactiva | `clean.bat` |
| `help.bat` | Ayuda básica | `help.bat` |
| `update.bat` | Actualizar dependencias | `update.bat` |

## 🎯 Comandos Avanzados

### Configuración con Parámetros
```powershell
# Configuración forzada (recrear entorno)
.\setup.ps1 -Force

# Incluir herramientas de desarrollo
.\setup.ps1 -Dev

# Configurar con Python específico
.\setup.ps1 -PythonPath "python3.12"
```

### Ejecución con Opciones
```powershell
# Puerto personalizado
.\run.ps1 -Port 8080

# Acceso desde red
.\run.ps1 -Address 0.0.0.0

# Abrir navegador automáticamente
.\run.ps1 -OpenBrowser

# Modo debug
.\run.ps1 -Debug

# Combinado
.\run.ps1 -Port 8080 -OpenBrowser -Debug
```

### Limpieza Selectiva
```powershell
# Limpieza básica
.\clean.ps1 -Cache -Temp

# Solo entorno virtual
.\clean.ps1 -Venv

# Limpieza completa (con confirmación)
.\clean.ps1 -All

# Forzar sin confirmación
.\clean.ps1 -All -Force
```

## 🔍 Solución de Problemas Windows

### Error: "Python no encontrado"
```powershell
# Verificar instalación
python --version
Get-Command python

# Si no funciona, reinstalar Python con "Add to PATH"
```

### Error: "No se pueden ejecutar scripts"
```powershell
# Cambiar política de ejecución
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar política actual
Get-ExecutionPolicy
```

### Error: "Error de compilación de paquetes"
```cmd
REM Instalar Visual Studio Build Tools
REM O usar versión precompilada:
pip install --only-binary=all mediapipe
```

### Error: "Puerto 8501 ocupado"
```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8501

# Usar puerto alternativo
.\run.ps1 -Port 8080
```

### Error: "MediaPipe no funciona"
```powershell
# Verificar versión de Python
python --version

# Si es 3.13+, usar requirements especial
pip install -r requirements-python313.txt

# O instalar Python 3.12
```

## 🔧 Configuración Avanzada Windows

### Variables de Entorno
```powershell
# Configurar variables permanentes
[System.Environment]::SetEnvironmentVariable("STREAMLIT_SERVER_PORT", "8501", "User")
[System.Environment]::SetEnvironmentVariable("MAX_UPLOAD_SIZE", "500", "User")
```

### Firewall (para acceso desde red)
```powershell
# Permitir Streamlit en firewall (como administrador)
New-NetFirewallRule -DisplayName "Streamlit Coach AI" -Direction Inbound -Protocol TCP -LocalPort 8501 -Action Allow
```

### Ejecutar como Servicio
```powershell
# Instalar NSSM (Non-Sucking Service Manager)
# Descargar desde: https://nssm.cc/download

# Configurar servicio
nssm install CoachAI "C:\path\to\coach-ai-v2\venv\Scripts\streamlit.exe"
nssm set CoachAI Arguments "run app.py --server.port 8501"
nssm set CoachAI AppDirectory "C:\path\to\coach-ai-v2"
nssm start CoachAI
```

## 📁 Estructura de Archivos Windows

```
coach-ai-v2\
│
├── Scripts PowerShell (.ps1)
│   ├── setup.ps1          # Configuración avanzada
│   ├── run.ps1             # Ejecución con parámetros
│   ├── activate.ps1        # Activación con información
│   ├── clean.ps1           # Limpieza selectiva
│   └── help.ps1            # Ayuda interactiva
│
├── Scripts Batch (.bat)
│   ├── setup.bat           # Configuración básica
│   ├── run.bat             # Ejecución simple
│   ├── activate.bat        # Activación básica
│   ├── verify.bat          # Verificación
│   ├── clean.bat           # Limpieza interactiva
│   ├── help.bat            # Ayuda básica
│   └── update.bat          # Actualización
│
├── venv\                   # Entorno virtual
├── data\students\          # Datos de estudiantes
├── auth\                   # Autenticación
├── reports\                # Reportes generados
└── logs\                   # Archivos de log
```

## 🔄 Flujo de Trabajo Recomendado

### Primera Vez
```powershell
# 1. Descargar proyecto
git clone <repository-url>
cd coach-ai-v2

# 2. Configurar entorno
.\setup.ps1

# 3. Ejecutar aplicación
.\run.ps1 -OpenBrowser

# 4. Verificar funcionamiento
.\verify.ps1
```

### Uso Diario
```powershell
# Activar entorno y ejecutar
.\run.ps1

# O activar manualmente
.\activate.ps1
streamlit run app.py
```

### Mantenimiento
```powershell
# Actualizar dependencias
git pull
.\update.bat

# Limpiar archivos temporales
.\clean.ps1 -Cache -Temp

# Verificar estado
.\verify.ps1
```

## 🎓 Trucos y Consejos Windows

### 1. Crear Acceso Directo
```powershell
# Crear acceso directo en escritorio
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Coach AI v2.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-WindowStyle Normal -Command `"cd 'C:\path\to\coach-ai-v2'; .\run.ps1 -OpenBrowser`""
$Shortcut.Save()
```

### 2. Configurar Alias
```powershell
# Agregar a perfil de PowerShell
echo "Set-Alias coach 'C:\path\to\coach-ai-v2\run.ps1'" >> $PROFILE

# Usar como: coach -OpenBrowser
```

### 3. Script de Backup
```powershell
# Backup automático de datos
$date = Get-Date -Format "yyyyMMdd_HHmmss"
Compress-Archive -Path "data", "auth" -DestinationPath "backup_$date.zip"
```

## 🆘 Soporte Windows

### Información del Sistema
```powershell
# Información completa del sistema
.\help.ps1
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
python --version
Get-ExecutionPolicy
```

### Logs de Error
```powershell
# Ver logs de aplicación
Get-Content logs\*.log -Tail 50

# Ver eventos de Windows relacionados
Get-EventLog Application -Source Python* -Newest 10
```

### Contacto
Para problemas específicos de Windows:
1. Ejecutar `.\verify.ps1` y compartir resultado
2. Incluir versión de Windows y Python
3. Describir pasos exactos que causan el error

---

**💡 Recomendación**: Usa PowerShell para mejor experiencia y más funciones. Los scripts .bat están disponibles para compatibilidad con sistemas más antiguos.

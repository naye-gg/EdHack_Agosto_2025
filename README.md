# Coach AI v2 - Análisis de Presentaciones con IA

Sistema de análisis inteligente de presentaciones que utiliza IA para evaluar habilidades de comunicación, lenguaje corporal y expresión vocal.

## 🎯 Características

- **Análisis de Voz**: Evaluación de claridad, velocidad, muletillas y prosodia
- **Análisis Corporal**: Detección de postura, gestos y movimientos
- **Análisis Facial**: Contacto visual, expresiones y confianza
- **Análisis de Contenido**: Evaluación de estructura y coherencia del discurso (modelo avanzado)
- **Reportes Detallados**: Generación de informes en PDF y Excel
- **Sistema Multiusuario**: Gestión de profesores y estudiantes
- **Progreso Histórico**: Seguimiento de mejoras a lo largo del tiempo

## 📋 Requisitos del Sistema

### Python
- **Python 3.11 - 3.12** (requerido)
- ⚠️ **Nota**: Python 3.13 no es compatible aún debido a MediaPipe

### Dependencias del Sistema

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ffmpeg libsndfile1 libsndfile1-dev python3-dev
```

#### macOS
```bash
# Instalar Homebrew si no está instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install ffmpeg libsndfile
```

#### Windows
1. Descargar e instalar FFmpeg desde [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Agregar FFmpeg al PATH del sistema

## 🚀 Instalación

### Opción 1: Instalación Automática (Recomendado) 🔥

```bash
# Clonar repositorio
git clone <repository-url>
cd coach-ai-v2

# Configurar entorno virtual automáticamente
python setup_venv.py
```

### Opción 2: Usando Makefile (Linux/macOS)

```bash
# Configuración completa
make setup

# Ejecutar aplicación
make run

# Ver todos los comandos disponibles
make help
```

### Opción 3: Instalación Manual

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd coach-ai-v2
```

2. **Crear entorno virtual**
```bash
python3.11 -m venv venv

# Activar entorno virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Opción 4: Scripts de Activación Rápida

Después de ejecutar `python setup_venv.py`, usa:

```bash
# Linux/macOS
./activate_venv.sh

# Windows
activate_venv.bat

# Ejecutar directamente
./run.sh          # Linux/macOS
run.bat           # Windows
```

### Opción 5: Usando uv (Más Rápido)

```bash
pip install uv
git clone <repository-url>
cd coach-ai-v2
uv sync
```

## 🔧 Configuración

### Verificación de Instalación

```bash
# Verificación automática completa
python verify_installation.py

# Verificación rápida manual
python -c "import streamlit, whisper, mediapipe, cv2; print('✅ Todas las dependencias instaladas correctamente')"
```

### Configuración de Variables de Entorno (Opcional)

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar configuración
nano .env  # o tu editor preferido
```

### Configuración de Directorios

Los directorios se crean automáticamente, pero puedes crearlos manualmente:

```bash
mkdir -p data/students auth reports logs backups
```

## 🏃‍♂️ Ejecución

### Métodos de Ejecución

#### 1. Usando Scripts de Activación (Recomendado)
```bash
# Linux/macOS
./run.sh

# Windows
run.bat
```

#### 2. Usando Makefile (Linux/macOS)
```bash
make run
```

#### 3. Con Entorno Virtual Activado
```bash
# Activar entorno virtual primero
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Ejecutar aplicación
streamlit run app.py
```

#### 4. Configuración Personalizada
```bash
# Puerto personalizado
streamlit run app.py --server.port 8080

# Acceso desde cualquier IP
streamlit run app.py --server.address 0.0.0.0

# Con configuración específica
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

La aplicación estará disponible en: `http://localhost:8501`

## 👥 Primer Uso

1. **Acceder a la aplicación** en el navegador
2. **Registrar un profesor** en la pestaña "Registro"
3. **Iniciar sesión** con las credenciales creadas
4. **Registrar estudiantes** desde el panel de gestión
5. **Subir videos** para análisis

## 📁 Estructura del Proyecto

```
coach-ai-v2/
├── app.py                          # Aplicación principal Streamlit
├── requirements.txt                # Dependencias Python
├── pyproject.toml                 # Configuración del proyecto
├── analysis/                      # Módulos de análisis
│   ├── voice_analyzer.py          # Análisis de voz
│   ├── body_language_analyzer.py  # Análisis corporal
│   ├── facial_analyzer.py         # Análisis facial
│   └── content_analyzer.py        # Análisis de contenido
├── auth/                          # Sistema de autenticación
│   ├── user_manager.py            # Gestión de usuarios
│   └── users.json                 # Base de datos de usuarios
├── utils/                         # Utilidades
│   ├── video_processor.py         # Procesamiento de video
│   ├── data_storage.py            # Almacenamiento de datos
│   └── report_generator.py        # Generación de reportes
├── visualization/                 # Visualizaciones
│   └── charts.py                  # Generación de gráficos
├── config/                        # Configuración
│   └── languages.py              # Soporte multiidioma
└── data/                          # Datos de la aplicación
    └── students/                  # Datos de estudiantes
```

## ⚙️ Configuración Avanzada

### Variables de Entorno (opcional)
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export MAX_UPLOAD_SIZE=500  # MB
```

### Configuración de Streamlit
Crear archivo `.streamlit/config.toml`:
```toml
[server]
port = 8501
maxUploadSize = 500

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

## 🔍 Solución de Problemas

### Problemas Comunes

#### Error: "No module named 'whisper'"
```bash
# Verificar que el entorno virtual está activado
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

#### Error: "ffmpeg not found"
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows: Descargar desde https://ffmpeg.org
```

#### Error de memoria con videos grandes
```bash
# Configurar límites en .env
MAX_UPLOAD_SIZE=200
VIDEO_QUALITY=low
ANALYSIS_FPS=3
```

#### Error: "MediaPipe not working"
```bash
pip uninstall mediapipe
pip install mediapipe==0.10.21
```

#### Entorno Virtual No Funciona
```bash
# Recrear entorno virtual
python clean.py --venv
python setup_venv.py
```

#### Cache Corrupto
```bash
# Limpiar todo el cache
python clean.py --cache --ml-cache
```

### Herramientas de Diagnóstico

```bash
# Verificación completa
python verify_installation.py

# Información del sistema
make info  # Linux/macOS

# Limpiar y reinstalar
python clean.py --all
python setup_venv.py
```

### Comandos de Limpieza

```bash
# Limpieza básica (cache, temporales)
python clean.py

# Limpieza completa (incluye datos)
python clean.py --all

# Limpiar solo entorno virtual
python clean.py --venv

# Ver opciones de limpieza
python clean.py --help
```

## 🚀 Despliegue en Producción

### Docker (Recomendado)
```dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    ffmpeg libsndfile1 libsndfile1-dev \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

### Usando Streamlit Cloud
1. Conectar repositorio a [share.streamlit.io](https://share.streamlit.io)
2. Configurar `requirements.txt` y `packages.txt` si es necesario

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para nueva característica
3. Commit cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver archivo LICENSE para detalles.

## 🆘 Soporte

Para problemas o preguntas:
- Crear un issue en GitHub
- Revisar la documentación de troubleshooting
- Verificar que todas las dependencias estén instaladas correctamente

## 🔄 Actualizaciones

Para actualizar a la última versión:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

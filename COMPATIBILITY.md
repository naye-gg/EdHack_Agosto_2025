# 🔧 Guía de Compatibilidad - Coach AI v2

## 🐍 Compatibilidad de Python

### ✅ Versiones Recomendadas (Funcionalidad Completa)
- **Python 3.11** - Totalmente compatible
- **Python 3.12** - Totalmente compatible

### ⚠️ Versiones con Limitaciones
- **Python 3.13+** - Funcionalidad limitada (sin MediaPipe)

## 📊 Matriz de Funcionalidades por Versión

| Funcionalidad | Python 3.11-3.12 | Python 3.13+ |
|---------------|-------------------|---------------|
| ✅ Análisis de Voz | ✅ | ✅ |
| ✅ Análisis de Contenido | ✅ | ✅ |
| ✅ Reportes PDF/Excel | ✅ | ✅ |
| ✅ Sistema Multiusuario | ✅ | ✅ |
| ❌ Análisis Corporal | ✅ | ❌ |
| ❌ Análisis Facial | ✅ | ❌ |
| ❌ Detección de Gestos | ✅ | ❌ |

## 🚀 Instalación según Versión de Python

### Para Python 3.11-3.12 (Recomendado)
```bash
# Instalación completa
python setup_venv.py

# O manual
pip install -r requirements.txt
```

### Para Python 3.13+
```bash
# Instalación con funcionalidad limitada
pip install -r requirements-python313.txt

# Advertencia mostrada automáticamente
python setup_venv.py
```

## 🔍 Verificar Compatibilidad

```bash
# Verificar versión de Python
python --version

# Verificar compatibilidad completa
python verify_installation.py

# Verificar MediaPipe específicamente
python -c "import mediapipe; print('MediaPipe OK')" 2>/dev/null || echo "MediaPipe no disponible"
```

## 🛠️ Soluciones por Versión

### Si usas Python 3.13+

#### Opción 1: Downgrade a Python 3.12 (Recomendado)
```bash
# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv
python3.12 setup_venv.py

# macOS con pyenv
pyenv install 3.12.7
pyenv local 3.12.7
python setup_venv.py

# Windows: Instalar desde python.org
```

#### Opción 2: Usar con Funcionalidad Limitada
```bash
# Aceptar limitaciones y continuar
python setup_venv.py
# Seleccionar 'y' cuando se pregunte sobre continuar
```

## 🐳 Docker (Solución Universal)

Si tienes problemas de compatibilidad, usa Docker:

```dockerfile
FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg libsndfile1 libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

```bash
# Ejecutar con Docker
docker build -t coach-ai-v2 .
docker run -p 8501:8501 coach-ai-v2
```

## 🔮 Futuro de MediaPipe

### Estado Actual
- MediaPipe 0.10.x soporta Python 3.11-3.12
- Python 3.13 requiere MediaPipe 0.11+ (en desarrollo)

### Cómo Monitorear
```bash
# Verificar nuevas versiones
pip index versions mediapipe

# Verificar compatibilidad futura
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}')"
```

### Migración Futura
Cuando MediaPipe soporte Python 3.13:

1. Actualizar `requirements.txt`
2. Remover restricción de versión
3. Actualizar documentación

## 📱 Alternativas sin MediaPipe

### Análisis Básico de Video
```python
# Usando solo OpenCV para análisis básico
import cv2
import numpy as np

# Detectar movimiento general
# Análisis de brillo/contraste
# Conteo de frames
```

### Servicios en la Nube
- **Google Cloud Video Intelligence API**
- **Amazon Rekognition Video**
- **Azure Video Analyzer**

## 🆘 Soporte y Troubleshooting

### Errores Comunes

#### `No module named 'mediapipe'`
```bash
# Verificar versión Python
python --version

# Si es 3.13+, usar requirements especial
pip install -r requirements-python313.txt
```

#### `Building wheel for mediapipe failed`
```bash
# Usar Python 3.11 o 3.12
pyenv install 3.12.7
pyenv local 3.12.7
pip install mediapipe
```

### Reportar Problemas
Si encuentras problemas de compatibilidad:

1. Incluir `python --version`
2. Incluir `pip list | grep mediapipe`
3. Incluir mensaje de error completo
4. Especificar sistema operativo

---

**💡 Recomendación**: Para mejor experiencia, usa Python 3.12 hasta que MediaPipe soporte oficialmente Python 3.13.

# 🚀 Guía de Inicio Rápido - Coach AI v2

Esta guía te ayudará a configurar y ejecutar Coach AI v2 en pocos minutos.

## ⚡ Inicio Ultra Rápido (1 comando)

```bash
# Configurar todo automáticamente
python setup_venv.py

# Ejecutar aplicación
./run.sh          # Linux/macOS
run.bat           # Windows
```

## 📋 Lista de Verificación Pre-instalación

- [ ] Python 3.11 o superior instalado
- [ ] FFmpeg instalado (para procesamiento de video)
- [ ] Al menos 2GB de RAM libre
- [ ] Conexión a internet (para descargar modelos)

## 🔧 Instalación Paso a Paso

### 1. Verificar Requisitos

```bash
# Verificar Python
python --version  # Debe ser 3.11+

# Verificar FFmpeg
ffmpeg -version
```

### 2. Configurar Proyecto

```bash
# Clonar repositorio
git clone <repository-url>
cd coach-ai-v2

# Configurar entorno virtual
python setup_venv.py
```

### 3. Ejecutar Aplicación

```bash
# Opción 1: Script directo
./run.sh

# Opción 2: Makefile (Linux/macOS)
make run

# Opción 3: Manual
source venv/bin/activate
streamlit run app.py
```

## 🌐 Acceder a la Aplicación

1. Abrir navegador en `http://localhost:8501`
2. Registrar un profesor en la pestaña "Registro"
3. Iniciar sesión con las credenciales creadas
4. ¡Comenzar a analizar presentaciones!

## 🎯 Primer Análisis de Prueba

1. **Registrar estudiante**: Ve a "Gestión de Estudiantes"
2. **Subir video**: Usa la sección "Análisis de Video"
3. **Ver resultados**: Revisa el feedback detallado
4. **Generar reporte**: Descarga PDF o Excel desde "Reportes"

## 🔧 Comandos Útiles

### Gestión del Entorno Virtual

```bash
# Activar entorno
./activate_venv.sh    # Linux/macOS
activate_venv.bat     # Windows

# Verificar instalación
python verify_installation.py

# Limpiar cache
python clean.py --cache
```

### Usando Makefile (Linux/macOS)

```bash
make help           # Ver todos los comandos
make setup          # Configurar entorno
make run           # Ejecutar aplicación
make verify        # Verificar instalación
make clean         # Limpiar entorno
```

## ❓ ¿Problemas?

### No encuentra Python 3.11
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv

# macOS
brew install python@3.11

# Windows: Descargar desde python.org
```

### FFmpeg no instalado
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows: Descargar desde ffmpeg.org
```

### Error de dependencias
```bash
# Recrear entorno completo
python clean.py --venv
python setup_venv.py
```

### La aplicación no abre
```bash
# Verificar puerto
netstat -tulpn | grep 8501

# Usar puerto diferente
streamlit run app.py --server.port 8080
```

## 🎓 Próximos Pasos

1. **Configurar usuarios**: Registra profesores y estudiantes
2. **Personalizar**: Edita `env.example` → `.env` para configuración avanzada
3. **Explorar**: Prueba el modelo básico y avanzado
4. **Reportes**: Genera informes para seguimiento de progreso

## 🆘 Soporte Adicional

- 📖 README completo: Ver `README.md`
- 🔧 Verificación: `python verify_installation.py`
- 🧹 Limpieza: `python clean.py --help`
- 📊 Información: `make info` (Linux/macOS)

---

**💡 Consejo**: Guarda esta página como referencia rápida para futuras configuraciones.

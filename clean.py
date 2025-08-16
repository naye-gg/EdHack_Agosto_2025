#!/usr/bin/env python3
"""
Script de limpieza para Coach AI v2
Limpia archivos temporales, cache y entorno virtual
"""

import os
import shutil
import sys
from pathlib import Path
import argparse

def clean_pycache():
    """Limpiar archivos __pycache__ y .pyc"""
    print("🧹 Limpiando cache de Python...")
    
    count = 0
    for root, dirs, files in os.walk('.'):
        # Remover directorios __pycache__
        if '__pycache__' in dirs:
            pycache_path = Path(root) / '__pycache__'
            try:
                shutil.rmtree(pycache_path)
                count += 1
                print(f"   Eliminado: {pycache_path}")
            except Exception as e:
                print(f"   Error eliminando {pycache_path}: {e}")
        
        # Remover archivos .pyc y .pyo
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                file_path = Path(root) / file
                try:
                    file_path.unlink()
                    count += 1
                    print(f"   Eliminado: {file_path}")
                except Exception as e:
                    print(f"   Error eliminando {file_path}: {e}")
    
    print(f"✅ Cache de Python limpiado ({count} elementos)")

def clean_venv():
    """Limpiar entorno virtual"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("🧹 Eliminando entorno virtual...")
        try:
            shutil.rmtree(venv_path)
            print("✅ Entorno virtual eliminado")
        except Exception as e:
            print(f"❌ Error eliminando entorno virtual: {e}")
    else:
        print("ℹ️  No hay entorno virtual que limpiar")

def clean_temp_files():
    """Limpiar archivos temporales"""
    print("🧹 Limpiando archivos temporales...")
    
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "temp_*",
        "tmp_*",
        "*.log",
        ".DS_Store",
        "Thumbs.db"
    ]
    
    count = 0
    for pattern in temp_patterns:
        for file_path in Path('.').rglob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                    count += 1
                    print(f"   Eliminado: {file_path}")
            except Exception as e:
                print(f"   Error eliminando {file_path}: {e}")
    
    print(f"✅ Archivos temporales limpiados ({count} archivos)")

def clean_streamlit_cache():
    """Limpiar cache de Streamlit"""
    cache_dirs = [
        Path.home() / ".streamlit",
        Path(".streamlit")
    ]
    
    print("🧹 Limpiando cache de Streamlit...")
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            # Solo limpiar archivos específicos, no toda la configuración
            temp_files = list(cache_dir.glob("*.tmp")) + list(cache_dir.glob("*.cache"))
            for temp_file in temp_files:
                try:
                    temp_file.unlink()
                    print(f"   Eliminado: {temp_file}")
                except Exception as e:
                    print(f"   Error eliminando {temp_file}: {e}")

def clean_ml_cache():
    """Limpiar cache de modelos de ML"""
    print("🧹 Limpiando cache de modelos ML...")
    
    cache_dirs = [
        Path.home() / ".cache" / "whisper",
        Path.home() / ".cache" / "torch",
        Path.home() / ".cache" / "huggingface",
        Path(".cache"),
        Path("models")
    ]
    
    count = 0
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            try:
                shutil.rmtree(cache_dir)
                count += 1
                print(f"   Eliminado: {cache_dir}")
            except Exception as e:
                print(f"   Error eliminando {cache_dir}: {e}")
    
    if count > 0:
        print(f"✅ Cache de modelos ML limpiado ({count} directorios)")
    else:
        print("ℹ️  No hay cache de modelos ML que limpiar")

def clean_data_files():
    """Limpiar datos de prueba (CUIDADO: esto elimina datos reales)"""
    print("⚠️  Limpiando datos de estudiantes...")
    
    data_dir = Path("data/students")
    if data_dir.exists():
        # Contar archivos antes de eliminar
        count = sum(1 for _ in data_dir.rglob("*") if _.is_file())
        
        try:
            shutil.rmtree(data_dir)
            data_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Datos de estudiantes limpiados ({count} archivos)")
        except Exception as e:
            print(f"❌ Error limpiando datos: {e}")
    else:
        print("ℹ️  No hay datos de estudiantes que limpiar")

def clean_auth_files():
    """Limpiar archivos de autenticación (CUIDADO: esto elimina usuarios)"""
    print("⚠️  Limpiando archivos de autenticación...")
    
    auth_file = Path("auth/users.json")
    if auth_file.exists():
        try:
            auth_file.unlink()
            print("✅ Archivo de usuarios eliminado")
        except Exception as e:
            print(f"❌ Error eliminando archivo de usuarios: {e}")
    else:
        print("ℹ️  No hay archivo de usuarios que limpiar")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Script de limpieza para Coach AI v2')
    parser.add_argument('--all', action='store_true', help='Limpiar todo (incluyendo datos)')
    parser.add_argument('--venv', action='store_true', help='Limpiar solo entorno virtual')
    parser.add_argument('--cache', action='store_true', help='Limpiar solo cache')
    parser.add_argument('--temp', action='store_true', help='Limpiar solo archivos temporales')
    parser.add_argument('--data', action='store_true', help='Limpiar datos de estudiantes (CUIDADO)')
    parser.add_argument('--auth', action='store_true', help='Limpiar usuarios (CUIDADO)')
    parser.add_argument('--ml-cache', action='store_true', help='Limpiar cache de modelos ML')
    
    args = parser.parse_args()
    
    print("🧹 Coach AI v2 - Script de Limpieza")
    print("=" * 40)
    
    # Si no se especifica ninguna opción, hacer limpieza básica
    if not any([args.all, args.venv, args.cache, args.temp, args.data, args.auth, args.ml_cache]):
        print("Ejecutando limpieza básica...")
        clean_pycache()
        clean_temp_files()
        clean_streamlit_cache()
        return
    
    # Verificar directorio
    if not Path("app.py").exists():
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Advertencia para operaciones destructivas
    if args.all or args.data or args.auth:
        print("⚠️  ADVERTENCIA: Esto eliminará datos permanentemente")
        choice = input("¿Continuar? (escriba 'SI' para confirmar): ")
        if choice != 'SI':
            print("Operación cancelada")
            return
    
    # Ejecutar limpiezas según argumentos
    if args.all:
        clean_pycache()
        clean_temp_files()
        clean_streamlit_cache()
        clean_ml_cache()
        clean_venv()
        clean_data_files()
        clean_auth_files()
    else:
        if args.cache:
            clean_pycache()
            clean_streamlit_cache()
        if args.temp:
            clean_temp_files()
        if args.venv:
            clean_venv()
        if args.ml_cache:
            clean_ml_cache()
        if args.data:
            clean_data_files()
        if args.auth:
            clean_auth_files()
    
    print("\n🎉 Limpieza completada")

if __name__ == "__main__":
    main()

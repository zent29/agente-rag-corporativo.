import subprocess
import sys
import os

def main():
    """Script para iniciar la aplicación Streamlit de forma sencilla."""
    # Asegurarnos de que el directorio actual sea el de este script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    app_path = os.path.join("src", "interface", "app.py")
    
    if not os.path.exists(app_path):
        print(f"Error: No se encontró la aplicación en {app_path}")
        sys.exit(1)
        
    print("Iniciando la aplicación del Agente RAG...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except KeyboardInterrupt:
        print("\nAplicación detenida por el usuario.")
    except FileNotFoundError:
        print("Error: No se encontró 'streamlit'. ¿Activaste el entorno virtual e instalaste los requirements?")

if __name__ == "__main__":
    main()

import subprocess
import sys

print("Iniciando la instalación forzada de NumPy...")
try:
    # Este comando instala numpy de forma directa usando el ejecutable actual de python
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "numpy==1.24.4", "--only-binary", ":all:", "--break-system-packages"
    ])
    print("\n¡Instalación completada con éxito!")
    
    # Comprobamos si ya se puede importar
    import numpy as np
    print("Verificación exitosa. Versión de NumPy instalada:", np.version)
except Exception as e:
    print("\nOcurrió un error durante la instalación:")
    print(e)
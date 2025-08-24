#!/usr/bin/env python3
"""
Pi Generator - Calculadora de dígitos de Pi
Archivo de ejecución alternativo
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pi_generator import PiApp
    import tkinter as tk
    
    if __name__ == "__main__":
        print("🥧 Iniciando Pi Generator...")
        root = tk.Tk()
        app = PiApp(root)
        print("✅ Aplicación cargada correctamente")
        root.mainloop()
        
except ImportError as e:
    print(f"❌ Error al importar dependencias: {e}")
    print("Asegúrate de que Python esté instalado correctamente")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error inesperado: {e}")
    sys.exit(1)
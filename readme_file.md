# Pi Generator 🥧

Una aplicación de escritorio moderna para calcular dígitos de Pi con alta precisión.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)

## ✨ Características

- 🚀 Cálculo hasta **100,000 dígitos** de Pi
- 🌙 **Modo oscuro/claro** intercambiable
- ⛶ **Pantalla completa** (F11)
- ⏹️ **Cancelación** de cálculos en progreso
- 📊 **Barra de progreso** en tiempo real
- 🎨 **Interfaz moderna** con Tkinter

## 🧮 Algoritmos

### Hasta 5,000 dígitos: **Fórmula de Machin**
```
π = 16×arctan(1/5) - 4×arctan(1/239)
```

### Más de 5,000 dígitos: **Algoritmo de Chudnovsky**
- Convergencia súper-rápida (~14 dígitos por iteración)
- El mismo algoritmo usado por récords mundiales

## ⚡ Rendimiento

| Dígitos  | Tiempo Estimado |
|----------|----------------|
| 1,000    | < 1 segundo    |
| 10,000   | 5-15 segundos  |
| 50,000   | 30-60 segundos |
| 100,000  | 2-3 minutos    |

*Probado en Ryzen 5 5600 - tu rendimiento puede variar*

## 🚀 Instalación y Uso

### Requisitos
- Python 3.7+
- Tkinter (incluido con Python)

### Ejecutar
```bash
python pi_generator.py
```

### Controles
- **F11**: Pantalla completa
- **Escape**: Salir de pantalla completa
- **⏹️ Stop**: Cancelar cálculo

## 🖥️ Sistema Recomendado

- **CPU**: Moderna (2015+) para mejor rendimiento
- **RAM**: 4GB+ para cálculos de 50K+ dígitos
- **OS**: Windows/macOS/Linux

## 📸 Capturas

### Modo Claro
![Modo Claro](screenshots/screenshot_light.png)

### Modo Oscuro
![Modo Oscuro](screenshots/screenshot_dark.png)

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Algunas ideas:

- [ ] Algoritmos adicionales (BBP, Ramanujan)
- [ ] Exportar resultados a archivo
- [ ] Comparación de velocidad entre algoritmos
- [ ] Visualización gráfica

## 📜 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🙏 Reconocimientos

- **David Chudnovsky** y **Gregory Chudnovsky** por su algoritmo revolucionario
- **John Machin** por su fórmula clásica del siglo XVIII
- La comunidad de Python por las herramientas increíbles

---

*¿Te gustó el proyecto? ¡Dale una ⭐ en GitHub!*
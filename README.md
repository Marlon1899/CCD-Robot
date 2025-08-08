# Simulación de Cinemática Inversa usando CCD para Robots Seriales

Este proyecto consiste en el desarrollo de una aplicación interactiva que simula la cinemática inversa de un robot manipulador con hasta 7 grados de libertad (DOF) utilizando el algoritmo **Cyclic Coordinate Descent (CCD)**. La aplicación está desarrollada en Python utilizando PyQt5 para la interfaz gráfica y `matplotlib` para la visualización dinámica.

## 🧠 Descripción

La cinemática inversa es el proceso mediante el cual se determinan los ángulos de las articulaciones de un robot para alcanzar una posición deseada en el espacio. El algoritmo **CCD** permite resolver este problema de forma iterativa, ajustando una articulación a la vez desde el efector final hacia la base.

El sistema permite:
- Seleccionar entre 2 a 7 grados de libertad.
- Configurar articulaciones **rotacionales** o **prismáticas**.
- Ajustar precisión y ángulo de convergencia del algoritmo.
- Visualizar gráficamente la trayectoria del robot y el punto objetivo.

## 🎯 Objetivos

### General
Desarrollar una aplicación de simulación interactiva para la cinemática inversa de manipuladores robóticos usando el algoritmo CCD.

### Específicos
- Diseñar una interfaz gráfica con PyQt5 para el control de parámetros.
- Implementar el algoritmo CCD con simulación visual en tiempo real.
- Optimizar la convergencia del algoritmo con parámetros configurables.
- Visualizar gráficamente la trayectoria, articulaciones, enlaces y objetivo.
- Validar la precisión del método con diferentes configuraciones.

## 🚀 Tecnologías Utilizadas

- `Python 3.9+`
- `PyQt5` – Interfaz gráfica
- `matplotlib` – Gráficos y visualización 2D/3D
- `numpy` – Operaciones matemáticas y vectoriales
- `QtDesigner` – Diseño de la UI

## 🧩 Estructura del Proyecto

```bash
.
├── main.py                # Archivo principal de ejecución
├── ui_mainwindow.ui      # Interfaz creada en QtDesigner
├── assets/               # Recursos visuales y figuras
├── docs/                 # Diagrama de flujo y documentación adicional
└── README.md             # Este archivo
```

## ⚙️ Funcionalidades Principales

- ✅ Interfaz intuitiva y responsiva
- ✅ Selección de GDL entre 2 y 7 mediante `QComboBox`
- ✅ Control de longitudes de eslabones vía `QSlider`
- ✅ Admite eslabones prismáticos y rotacionales
- ✅ Selección de punto objetivo con clic sobre la gráfica
- ✅ Visualización dinámica del robot y su trayectoria
- ✅ Parámetros ajustables: precisión y ángulo de cambio
- ✅ Simulación animada del método CCD

## 📌 Parámetros de Control

| Parámetro             | Descripción                                                   |
|----------------------|---------------------------------------------------------------|
| `GDL`                | Número de grados de libertad del robot (2 a 7)                |
| `Tipo de articulación` | Rotacional o prismático por cada articulación               |
| `Precisión`          | Error mínimo permitido entre posición actual y objetivo       |
| `Ángulo de cambio`   | Incremento angular usado en cada iteración (5° a 90°)         |
| `Mostrar trayectoria`| Opción para visualizar o no la trayectoria completa del robot |

## 🧪 Resultados

La simulación demuestra cómo varían las trayectorias del robot según el número de GDL, el tipo de eslabón, la precisión y el ángulo de cambio. Se logra visualizar la convergencia hacia el punto objetivo de forma clara y didáctica.

Algunas configuraciones probadas:

| GDL | Tipo | Precisión | Ángulo Cambio | Observación                         |
|-----|------|-----------|---------------|-------------------------------------|
| 5   | Rotacional | 0.2       | 5°            | Convergencia suave y precisa        |
| 4   | Mixto      | 0.5       | 45°           | Rápida pero menos precisa           |
| 3   | Prismático | 0.2       | 90°           | Cambios bruscos, buena convergencia |

![Imagen de WhatsApp 2025-07-17 a las 10 17 32_ad4813b9](https://github.com/user-attachments/assets/95b2287f-739c-4bfc-8f8e-97937f22e0f6)


## ✅ Conclusiones

- El método CCD es efectivo para resolver cinemática inversa de robots seriales de forma visual e interactiva.
- El sistema puede adaptarse a múltiples configuraciones de robots gracias a su modularidad.
- El uso de una GUI intuitiva permite comprender mejor el proceso iterativo de convergencia.

## 📚 Referencias

- Barrientos, A. (2017). *Fundamentos de robótica*. McGraw-Hill.
- Cinemática Inversa - K. Ramírez. [kramirez.net](https://www.kramirez.net/Robotica/Material/Presentaciones/CinematicaInversaRobot.pdf)
- Ortiz Sánchez, U. E. (2017). *Solucionador de cinemática inversa del Golem-II*. UNAM.
- Cerrillo Vacas, D. (2022). *Modelado de Robots Hiperredundantes*. UPM.

## 🧑‍💻 Autor

**Marlon Mayorga**  
Estudiante de Ingeniería Mecatrónica  
Universidad de las Fuerzas Armadas ESPE - Latacunga  
_Periodo 202450_

## 📄 Licencia

Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

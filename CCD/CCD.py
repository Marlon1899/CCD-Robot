import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QLabel, QComboBox, QCheckBox, QLineEdit, QMessageBox, QTextEdit
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from typing import List, Tuple, Optional
from matplotlib import patches

# Constantes
MAX_GDL = 7
RANGO_SLIDER = 20000
MULTI_SLIDER = 100
RADIO = 10
ITERACION = 1000

class CCD(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("CCD.ui", self)
        self.setFixedSize(1130, 820)
        self.move(400, 50)

        self.inicar_variables()
        self.setup_ui()
        self.plot_robot()

    def inicar_variables(self):
        self.gdl = 2
        self.point_selected = False
        self.target_point: Optional[Tuple[float, float]] = None
        self.precision = 0.2
        self.cid = None
        self.angulo = 5
        self.target_artist = None
        self.target_artist = None
        self.eslabones = [100] * MAX_GDL
        self.labels_eslabones = [getattr(self, f'd{i+1}') for i in range(MAX_GDL)]
        self.angle_labels = [getattr(self, f'df{i+1}') for i in range(MAX_GDL)]
        self.trayectoria: List[Tuple[float, float]] = []
        self.show_trayectoria = False
        self.tipo_art = [False] * MAX_GDL
        self.velocidades = {"Baja": 500, "Media": 200, "Alta": 10}  # en ms
        self.velocidad_actual = self.velocidades["Media"]
        self.current_link = self.gdl - 1  # Inicializamos current_link aquí

    def setup_ui(self):
        self.sliders = [getattr(self, f'ds{i+1}') for i in range(MAX_GDL)]
        for i, slider in enumerate(self.sliders):
            self.setup_slider(slider, lambda value, index=i: self.update_slider(value, index))

        self.DOF.setStyleSheet("background-color: white; border-radius: 8px; text-align: justify;")
        self.DOF.currentIndexChanged.connect(self.update_gdl)

        self.puntof.clicked.connect(self.toggle_point_selection)
        self.calcular.clicked.connect(self.calculate_kinematics)

        self.pres_input.setText(str(self.precision))
        self.pres_input.textChanged.connect(self.update_precision)

        self.angcambio.setText(str(self.angulo))
        self.angcambio.textChanged.connect(self.update_angulo)  # Solo conectamos la señal

        self.stop.clicked.connect(self.stop_simulacion)  # Conectar el botón "stop" al método stop_simulacion

        self.vel.currentIndexChanged.connect(self.update_vel)

        self.pr_checkboxes = [getattr(self, f'pr{i+1}') for i in range(MAX_GDL)]
        for i, checkbox in enumerate(self.pr_checkboxes):
            checkbox.stateChanged.connect(lambda state, index=i: self.update_tipo_art(state, index))

        self.setup_plot()

    def setup_plot(self):
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.figure.setLayout(QVBoxLayout())
        self.figure.layout().addWidget(self.canvas)

        self.checkbox_trayectoria = QCheckBox("Mostrar trayectoria", self)
        self.checkbox_trayectoria.setChecked(self.show_trayectoria)
        self.checkbox_trayectoria.stateChanged.connect(self.toggle_trayectoria)
        self.figure.layout().addWidget(self.checkbox_trayectoria)

    def setup_slider(self, slider: QSlider, slot):
        slider.setRange(0, RANGO_SLIDER)
        slider.setValue(RANGO_SLIDER // 2)
        slider.valueChanged.connect(slot)

    def update_slider(self, value: int, index: int):
        self.eslabones[index] = value / MULTI_SLIDER
        self.labels_eslabones[index].setText(f"{value / MULTI_SLIDER:.2f}")
        self.normalizar_eslabones()
        self.plot_robot()

    def normalizar_eslabones(self):
        total_length = sum(self.eslabones[:self.gdl])
        if total_length == 0:
            return
        scale_factor = (self.gdl * 100) / total_length
        for i in range(self.gdl):
            self.eslabones[i] *= scale_factor
            self.sliders[i].blockSignals(True)
            self.sliders[i].setValue(int(self.eslabones[i] * MULTI_SLIDER))
            self.sliders[i].blockSignals(False)
            self.labels_eslabones[i].setText(f"{self.eslabones[i]:.2f}")

    def update_gdl(self):
        self.gdl = self.DOF.currentIndex() + 2
        self.reset_sliders()
        self.normalizar_eslabones()
        for i, slider in enumerate(self.sliders):
            slider.setEnabled(i < self.gdl)
        for i, checkbox in enumerate(self.pr_checkboxes):
            checkbox.setEnabled(i < self.gdl)
        self.plot_robot()

    def reset_sliders(self):
        for i in range(MAX_GDL):
            self.eslabones[i] = 100
            self.sliders[i].blockSignals(True)
            self.sliders[i].setValue(RANGO_SLIDER // 2)
            self.sliders[i].blockSignals(False)
            self.labels_eslabones[i].setText("100.00")

    def toggle_point_selection(self):
        self.point_selected = not self.point_selected
        if self.point_selected:
            self.cid = self.canvas.mpl_connect('button_press_event', self.on_point_click)
            self.puntof.setText("Seleccionar punto (activo)")
        else:
            if self.cid is not None:
                self.canvas.mpl_disconnect(self.cid)
                self.cid = None
            self.puntof.setText("Seleccionar punto")

    def on_point_click(self, event):
        if event.button == 1 and event.inaxes == self.ax:
            if self.target_artist is not None:
                self.target_artist.remove()
                self.target_artist = None
            for text in self.ax.texts:
                text.remove()
            selected_x, selected_y = event.xdata, event.ydata
            
            if np.hypot(selected_x, selected_y) <= RADIO:
                self.target_point = (selected_x, selected_y)
                self.target_artist = self.ax.plot(selected_x, selected_y, 'bo', markersize=8)[0]
                self.ax.text(selected_x, selected_y, f'({selected_x:.2f}, {selected_y:.2f})', fontsize=12, ha='right')
                self.canvas.draw()
            else:
                self.show_warning("El punto seleccionado está fuera del área permitida.")
            
            self.toggle_point_selection()

    def show_warning(self, message: str):
        QMessageBox.warning(self, "Advertencia", message, QMessageBox.Ok)

    def calculate_kinematics(self):
        if self.target_point is not None:
            self.simulate_ccd_inverse_kinematics(*self.target_point)
        else:
            self.show_warning("No se ha seleccionado ningún punto objetivo.")

    def simulate_ccd_inverse_kinematics(self, target_x: float, target_y: float):
        angles = np.zeros(self.gdl)
        self.trayectoria = []
        self.current_link = self.gdl - 1  # Definimos current_link como atributo de la clase

        def update_simulation():
            nonlocal angles
            xR, yR, _ = self.cinematica_directa(angles)
            end_effector_x, end_effector_y = xR[-1], yR[-1]
            self.trayectoria.append((end_effector_x, end_effector_y))
            error = np.hypot(target_x - end_effector_x, target_y - end_effector_y) #Error calculado con sqrt[(xf-xi)^2+(yf-yi)^2]
            
            self.disobj.setText(f"Distancia: {error:.2f} cm")
            
            if error < self.precision:
                self.timer.stop()  # Usamos self.timer en lugar de timer
                self.plot_robot(angles)
                return

            # Movemos solo el eslabón actual
            pivot_x, pivot_y = xR[self.current_link], yR[self.current_link]
            to_end_effector = [end_effector_x - pivot_x, end_effector_y - pivot_y]
            to_target = [target_x - pivot_x, target_y - pivot_y]
            
            angle_to_end_effector = np.arctan2(to_end_effector[1], to_end_effector[0])
            angle_to_target = np.arctan2(to_target[1], to_target[0])
            
            angle_change = angle_to_target - angle_to_end_effector
            angle_change = np.clip(angle_change, -self.ANGULO_DE_CAMBIO, self.ANGULO_DE_CAMBIO)
            
            if self.tipo_art[self.current_link]:  # Si es prismático
                angles[self.current_link] += np.hypot(to_target[0], to_target[1])
            else:  # Si es rotacional
                angles[self.current_link] += angle_change
            
            self.plot_robot(angles)
            self.update_angle_labels(angles)
            
            # Pasamos al siguiente eslabón
            self.current_link -= 1
            if self.current_link < 0:
                self.current_link = self.gdl - 1  # Volvemos al último eslabón

        self.timer = QTimer(self)
        self.timer.timeout.connect(update_simulation)
        self.timer.start(self.velocidad_actual)

    def cinematica_directa(self, val_art: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        val_art = np.pad(val_art, (0, self.gdl - len(val_art)), 'constant')
        escala = RADIO / (self.gdl * 100)
        xR = np.zeros(self.gdl + 1)
        yR = np.zeros(self.gdl + 1)
        ang = np.zeros(self.gdl)
        suma_angulos = 0

        for i in range(self.gdl):
            if self.tipo_art[i]:
                xR[i+1] = xR[i] + (val_art[i] * escala) * np.cos(suma_angulos)
                yR[i+1] = yR[i] + (val_art[i] * escala) * np.sin(suma_angulos)
            else:
                xR[i+1] = xR[i] + (self.eslabones[i] * escala) * np.cos(val_art[i] + suma_angulos)
                yR[i+1] = yR[i] + (self.eslabones[i] * escala) * np.sin(val_art[i] + suma_angulos)
                suma_angulos += val_art[i]
            ang[i] = suma_angulos

        return xR, yR, ang

    def plot_robot(self, angles: Optional[np.ndarray] = None):
        if angles is None:
            angles = np.zeros(self.gdl)
        
        xR, yR, _ = self.cinematica_directa(angles)
        
        self.ax.clear()
        self.ax.set_xlim(-11, 11)
        self.ax.set_ylim(-11, 11)
        
        self.plot_workspace()
        self.plot_target()
        self.plot_trayectoria()
        
        # Graficar los enlaces del robot
        self.ax.plot(xR, yR, 'k-')
        
        # Graficar los joints
        for i in range(self.gdl):
            color = 'r' if hasattr(self, 'current_link') and i == self.current_link else 'b'
            marker = 's' if self.tipo_art[i] else 'o'
            self.ax.plot(xR[i], yR[i], color + marker, markersize=8)
        
        # Graficar la línea entrecortada desde el punto final hasta el último eslabón
        if self.target_point:
            self.ax.plot([self.target_point[0], xR[-1]], [self.target_point[1], yR[-1]], 'g--', linewidth=2)

        self.ax.set_xlabel('Coordenada X cm')
        self.ax.set_ylabel('Coordenada Y cm')
        self.ax.set_title('Representación del robot')
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.grid(True)

        self.canvas.draw()

    def plot_workspace(self):
        th = np.linspace(0, 2*np.pi, 100)
        xc, yc = RADIO*np.cos(th), RADIO*np.sin(th)
        self.ax.plot(xc, yc, color=[0.7,0.7,0.7])

    def plot_target(self):
        if self.target_point:
            self.ax.scatter(*self.target_point, c='r', marker='+')
            circle = plt.Circle(self.target_point, self.precision, fill=False, color='r')
            self.ax.add_artist(circle)

    def plot_trayectoria(self):
        if self.show_trayectoria and self.trayectoria:
            trayectoria = np.array(self.trayectoria)
            self.ax.plot(trayectoria[:,0], trayectoria[:,1], color=[0.9500, 0.3250, 0.0980])

    def plot_robot_links(self, angles: np.ndarray):
        xR, yR, _ = self.cinematica_directa(angles)
        
        # Graficar los enlaces del robot
        self.ax.plot(xR, yR, 'k-')
        
        # Graficar los joints
        for i in range(self.gdl):
            marker = 'bs' if self.tipo_art[i] else 'ro'
            self.ax.plot(xR[i], yR[i], marker, markersize=8)
        
        # Graficar la línea entrecortada desde el punto final hasta el último eslabón
        if self.target_point:
            self.ax.plot([self.target_point[0], xR[-1]], [self.target_point[1], yR[-1]], 'r--', linewidth=2)

    def toggle_trayectoria(self, state: int):
        self.show_trayectoria = state == 2
        self.plot_robot()
    
    def update_angle_labels(self, angles: np.ndarray):
        for i in range(self.gdl):
            if self.tipo_art[i]:  # Si es prismático
                self.angle_labels[i].setText(f"{angles[i]:.2f} cm")
            else:  # Si es rotacional
                self.angle_labels[i].setText(f"{np.degrees(angles[i]):.2f}°")

    def update_precision(self):
        try:
            new_precision = float(self.pres_input.toPlainText())
            if new_precision > 0:
                self.precision = new_precision
            else:
                raise ValueError("Precision must be positive")
        except ValueError:
            self.show_warning("Ingrese un valor numérico positivo válido para la precisión.")
            self.pres_input.setText(str(self.precision))
    
    def update_angulo(self):
        try:
            new_angulo = float(self.angcambio.toPlainText())
            if 5 <= new_angulo <= 90:
                self.angulo = new_angulo
                self.ANGULO_DE_CAMBIO = np.radians(self.angulo)
            else:
                raise ValueError("El ángulo debe estar entre 5 y 90 grados.")
        except ValueError as e:
            self.show_warning(str(e))
            self.angcambio.setText(str(self.angulo))  # Restablecer al valor anterior

    def update_vel(self):
        velocidad_seleccionada = self.vel.currentText()
        self.velocidad_actual = self.velocidades[velocidad_seleccionada]

    def update_tipo_art(self, state: int, index: int):
        self.tipo_art[index] = state == 2
        self.plot_robot()
    
    def stop_simulacion(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
            self.disobj.setText("Simulación detenida.")  # Puedes actualizar la UI o el texto según sea necesario
            self.current_link = self.gdl - 1  # Restablecer el eslabón actual si es necesario
            self.plot_robot()  # Volver a graficar el robot si quieres limpiar la visualización


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = CCD()
    GUI.show()
    sys.exit(app.exec_())
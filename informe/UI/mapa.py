from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from qgis.core import QgsApplication
from qgis.gui import QgsMapCanvas

# Configurar QGIS
QgsApplication.setPrefixPath("/path/to/qgisInstallationFolder", True)
app = QgsApplication([], True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Crear una ventana principal
        self.setWindowTitle("Aplicación con Mapa")
        self.setGeometry(100, 100, 800, 600)
        
        # Crear un contenedor para la interfaz
        container = QWidget()
        layout = QVBoxLayout()
        
        # Botones de ejemplo
        self.btnLoadLayer = QPushButton("Cargar Capa")
        self.btnZoomIn = QPushButton("Acercar")
        self.btnZoomOut = QPushButton("Alejar")
        
        # Añadir botones al layout
        layout.addWidget(self.btnLoadLayer)
        layout.addWidget(self.btnZoomIn)
        layout.addWidget(self.btnZoomOut)
        
        # Crear el widget del mapa de QGIS
        self.mapCanvas = QgsMapCanvas()
        layout.addWidget(self.mapCanvas)
        
        # Establecer el layout en la ventana principal
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Conectar botones a funciones (ejemplo básico)
        self.btnZoomIn.clicked.connect(self.zoomIn)
        self.btnZoomOut.clicked.connect(self.zoomOut)

    def zoomIn(self):
        self.mapCanvas.zoomIn()

    def zoomOut(self):
        self.mapCanvas.zoomOut()

# Iniciar la aplicación
if __name__ == "__main__":
    window = MainWindow()
    window.show()
    
    # Iniciar QGIS y comenzar la aplicación
    app.exec()
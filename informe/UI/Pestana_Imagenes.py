from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QGroupBox, QTabWidget, QScrollArea
)
from PyQt6.QtGui import (QPixmap,QTransform)
from PyQt6.QtCore import Qt


class PestañaImagenes(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_principal = QVBoxLayout(self)
        
        # Crear un área de desplazamiento
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout_principal.addWidget(self.scroll_area)
        
        # Contenedor interno para el contenido desplazable
        self.contenedor_scroll = QWidget()
        self.scroll_area.setWidget(self.contenedor_scroll)
        
        # Layout para el contenedor interno
        self.layout_scroll = QVBoxLayout(self.contenedor_scroll)
        
        # Lista para almacenar información de las imágenes
        self.lista_imagenes = []
        
        # Layout para organizar las imágenes en dos columnas
        self.grid_layout = QGridLayout()
        self.layout_scroll.addLayout(self.grid_layout)
        
        # Botón para cargar múltiples imágenes
        btn_cargar_imagenes = QPushButton("Cargar Imágenes")
        btn_cargar_imagenes.clicked.connect(self.cargar_imagenes)
        self.layout_principal.addWidget(btn_cargar_imagenes)
        
    
    def cargar_imagenes(self):
        # Abrir cuadro de diálogo para seleccionar múltiples imágenes
        rutas_imagenes, _ = QFileDialog.getOpenFileNames(
            self, 
            "Seleccionar Imágenes", 
            "./Resultados/Imagenes", 
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        for ruta in rutas_imagenes:
            self.agregar_imagen(ruta)
    
    def agregar_imagen(self, ruta_imagen):
        # Crear un contenedor para la imagen y sus controles
        contenedor = QWidget()
        layout_contenedor = QVBoxLayout(contenedor)
        
        # Mostrar la imagen
        label_imagen = QLabel()
        pixmap = QPixmap(ruta_imagen)
        #label_imagen.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        label_imagen.setPixmap(pixmap.scaled(label_imagen.width(), label_imagen.height(), Qt.AspectRatioMode.KeepAspectRatio))
        layout_contenedor.addWidget(label_imagen)
        
        # Campo de texto con el nombre del archivo
        nombre_archivo = QLineEdit()
        nombre_archivo.setText(ruta_imagen.split("/")[-1])  # Nombre del archivo
        layout_contenedor.addWidget(nombre_archivo)
        
        # Botón para rotar la imagen
        btn_rotar = QPushButton("Rotar 90°")
        layout_contenedor.addWidget(btn_rotar)
        
        # Botón para eliminar la imagen
        btn_eliminar = QPushButton("Eliminar")
        layout_contenedor.addWidget(btn_eliminar)
        
        # Información inicial de la imagen
        numero_imagen = len(self.lista_imagenes) + 1
        rotacion = 0
        ancho = pixmap.width()
        alto = pixmap.height()
        self.lista_imagenes.append({
            "numero": numero_imagen,
            "ruta": ruta_imagen,
            "ancho": ancho,
            "alto": alto,
            "rotacion": rotacion
        })
        
        # Función para rotar la imagen
        def rotar_imagen():
            nonlocal rotacion
            rotacion = (rotacion + 90) % 360
            pixmap_rotado = pixmap.transformed(QTransform().rotate(rotacion))
            label_imagen.setPixmap(pixmap_rotado.scaled(label_imagen.width(), label_imagen.height(), Qt.AspectRatioMode.KeepAspectRatio))
            # Actualizar la lista
            for img in self.lista_imagenes:
                if img["ruta"] == ruta_imagen:
                    img["rotacion"] = rotacion
        
        # Función para eliminar la imagen
        def eliminar_imagen():
            for i, img in enumerate(self.lista_imagenes):
                if img["ruta"] == ruta_imagen:
                    self.lista_imagenes.pop(i)
                    break
            # Eliminar el contenedor del layout
            for i in range(self.grid_layout.count()):
                widget = self.grid_layout.itemAt(i).widget()
                if widget == contenedor:
                    self.grid_layout.removeWidget(widget)
                    widget.deleteLater()
                    break
        
        btn_rotar.clicked.connect(rotar_imagen)
        btn_eliminar.clicked.connect(eliminar_imagen)
        
        # Agregar el contenedor al grid layout en dos columnas
        fila = self.grid_layout.count() // 2
        columna = self.grid_layout.count() % 2
        self.grid_layout.addWidget(contenedor, fila, columna)

# Agregar la pestaña al QTabWidget
def agregar_pestana_imagenes(tab_widget):
    pestaña_imagenes = PestañaImagenes()
    tab_widget.addTab(pestaña_imagenes, "Cargar Imágenes")
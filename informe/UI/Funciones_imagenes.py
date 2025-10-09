import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar,
                             QFileDialog, QMenuBar, QMenu, QTabWidget, QTextEdit, 
                             QFormLayout, QGroupBox, QSpinBox, QComboBox, QDateEdit, QListWidget, QListWidgetItem,QScrollArea,QTableWidgetItem,QTableWidget,QGridLayout,
                             QSizePolicy, QCheckBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt, QTimer, QDate

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QFileInfo, Qt
from PyQt6.QtGui import QPixmap
from num2words import num2words
from Estilos import Estilos



import subprocess
import os

class FuncionesImagenes:
    
    def agregar_imagen(self,layout_destino=None, path_imagen=None, leyenda=""):
        # Abrir un cuadro de diálogo para seleccionar una imagen

        if path_imagen is None:
            ruta_imagen, _ = QFileDialog.getOpenFileName(
                self, 
                "Seleccionar imagen", 
                "./Resultados/Imagenes",  # Carpeta actual
                "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
        else:
            ruta_imagen = path_imagen
        if ruta_imagen:  # Si se seleccionó una imagen
            
            contenedor = QWidget()
            layout = QVBoxLayout(contenedor)
            
            # Mostrar imagen reducida
            
            label = QLabel()
            pixmap = QPixmap(ruta_imagen)
            label.setProperty("path_imagen", ruta_imagen)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.AspectRatioMode.KeepAspectRatio))            
            
            # Campo de descripción
            descripcion = QLineEdit()
            if leyenda:
                descripcion.setText(leyenda)
            else:
                descripcion.setPlaceholderText("Descripción de la imagen")
            
            # Botón para eliminar
            btn_eliminar = QPushButton("x")
            btn_eliminar.setObjectName("botonEliminar")
            
            btn_eliminar.setStyleSheet(Estilos.cargar_estilos(self, "styles.css"))
            btn_eliminar.clicked.connect(lambda: eliminar_imagen(self,contenedor))
            
            layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(descripcion)
            layout.addWidget(btn_eliminar, alignment=Qt.AlignmentFlag.AlignCenter)
            
            #self.lista_imagenes.addWidget(contenedor)
            # Agregar el contenedor al layout proporcionado
            
            
            layout_destino.addWidget(contenedor)

        def eliminar_imagen(self, widget):
            #self.lista_imagenes.removeWidget(widget)
            widget.deleteLater()
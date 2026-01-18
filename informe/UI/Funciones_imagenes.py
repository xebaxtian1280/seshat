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
from DB import DB


import subprocess
import os

class FuncionesImagenes:
    
    def agregar_imagen(self,layout_destino=None, path_imagen=None, leyenda="", id_imagen=None, tabla=None, path_trabajo=None):
        # Abrir un cuadro de diálogo para seleccionar una imagen

        if path_imagen is None:
            print("Path trabajo:", path_trabajo)
            ruta_imagen, _ = QFileDialog.getOpenFileName(
                self, 
                "Seleccionar imagen", 
                path_trabajo,  # Carpeta actual
                "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
        else:
            ruta_imagen = path_imagen
        if ruta_imagen:  # Si se seleccionó una imagen
            
            contenedor = QWidget()

            if id_imagen:
                contenedor.setProperty("id_imagen", id_imagen)

            layout = QVBoxLayout(contenedor)
            
            # Mostrar imagen reducida
            
            label = QLabel()
            pixmap = QPixmap(ruta_imagen)
            contenedor.setProperty("path_imagen", ruta_imagen)
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
            # Botón para eliminar
            btn_actualizar_imagen = QPushButton("Actualizar imagen")
            btn_actualizar_imagen.setStyleSheet(Estilos.cargar_estilos(self, "styles.css"))
            btn_actualizar_imagen.clicked.connect(lambda: actualizar_imagen(self,contenedor))
            
            layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(descripcion)
            layout.addWidget(btn_eliminar, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(btn_actualizar_imagen, alignment=Qt.AlignmentFlag.AlignCenter)
            
            #self.lista_imagenes.addWidget(contenedor)
            # Agregar el contenedor al layout proporcionado
            
            
            layout_destino.addWidget(contenedor)

        def actualizar_imagen(self, contenedor):

            ruta_imagen, _ = QFileDialog.getOpenFileName(
                self, 
                "Seleccionar imagen", 
                "./Resultados/Imagenes",  # Carpeta actual
                "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
            )
            if ruta_imagen:  # Si se seleccionó una imagen
                
                label = contenedor.findChild(QLabel)
                pixmap = QPixmap(ruta_imagen)
                contenedor.setProperty("path_imagen", ruta_imagen)
                label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.AspectRatioMode.KeepAspectRatio))            
                
                id_imagen = contenedor.property("id_imagen")
               

        def eliminar_imagen(self, widget):
            #self.lista_imagenes.removeWidget(widget)
            if id_imagen:
                db = DB(host="localhost", database='seshat', user="postgres", password="ironmaiden")
                db.conectar()
                db.eliminar(f"DELETE FROM {tabla} WHERE id = %s", (id_imagen,))
                print(f"Imagen con ID {id_imagen} eliminada de la base de datos.")
                db.cerrar_conexion()
            
            widget.deleteLater()
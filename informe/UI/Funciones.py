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

class Funciones:


    def generar_informe(texto, template_path="Base/Informe.tex", output_name="Resultados/informe"):
        """
        Genera un informe LaTeX desde una plantilla y texto dinámico.
        
        Args:
            texto (str): Contenido a insertar
            template_path (str): Ruta de la plantilla .tex
            output_name (str): Nombre base del archivo de salida
        """
        
        # Leer plantilla
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                plantilla = f.read()
        except FileNotFoundError:
            print(f"Error: No se encontró {template_path}")
            return

        # Escapar caracteres especiales de LaTeX
        texto_procesado = texto.replace("&", "\&").replace("%", "\%").replace("$", "\$")
        
        # Reemplazar marcador en la plantilla
        informe_final = plantilla.replace("%DIRECCION%", texto_procesado)
        
        # Guardar archivo .tex
        with open(f"{output_name}.tex", "w", encoding="utf-8") as f:
            f.write(informe_final)
        
        # Compilar a PDF
        """ try:
            subprocess.run(["pdflatex", f"{output_name}.tex"], check=True)
            print(f"\nPDF generado: {output_name}.pdf")
            
            # Limpiar archivos auxiliares
            for ext in [".aux", ".log", ".out"]:
                archivo = f"{output_name}{ext}"
                if os.path.exists(archivo):
                    os.remove(archivo)
                    
        except FileNotFoundError:
            print("\n¡Error! Necesitas LaTeX instalado (pdflatex)") """
            
    def agregar_imagen(self,layout_destino=None):
        # Abrir un cuadro de diálogo para seleccionar una imagen
        ruta_imagen, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar imagen", 
            "./Resultados/Imagenes",  # Carpeta actual
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if ruta_imagen:  # Si se seleccionó una imagen
            
            contenedor = QWidget()
            layout = QVBoxLayout(contenedor)
            
            # Mostrar imagen reducida
            
            label = QLabel()
            pixmap = QPixmap(ruta_imagen)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.AspectRatioMode.KeepAspectRatio))            
            
            # Campo de descripción
            descripcion = QLineEdit()
            descripcion.setPlaceholderText("Descripción de la imagen")
            
            # Botón para eliminar
            btn_eliminar = QPushButton("X")
            btn_eliminar.setStyleSheet("color: red;")
            btn_eliminar.clicked.connect(lambda: eliminar_imagen(self,contenedor))
            
            layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(descripcion)
            layout.addWidget(btn_eliminar)
            
            #self.lista_imagenes.addWidget(contenedor)
            # Agregar el contenedor al layout proporcionado
            
            
            layout_destino.addWidget(contenedor)

        def eliminar_imagen(self, widget):
            #self.lista_imagenes.removeWidget(widget)
            widget.deleteLater()
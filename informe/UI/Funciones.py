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
from Pestana_Datos_solicitud import (PestanaDatosSolicitud)
from Pestana_caracteristicas_sector import (PestanaCaracteristicasSector)


import subprocess
import os

class Funciones:
       
        
    def agregar_pestanas_avaluo(self, id_avaluo, tab_panel):
        
        """
        Agrega las pestañas relacionadas con el avalúo al accionar el botón 'boton_accion'.
        Pasa el id_avaluo a cada pestaña para cargar la información correspondiente.
        
        :param id_avaluo: ID del avalúo seleccionado.
        """
        
        try:
            # Crear las pestañas con el id_avaluo
            
            """ pestana_solicitud = PestanaDatosSolicitud(id_avaluo)
            pestana_sector = PestanaCaracteristicasSector(id_avaluo)
            pestana_construccion = PestanaCaracteristicasConstruccion(id_avaluo)
            pestana_valuacion = PestanaCondicionesValuacion(id_avaluo)
            pestana_imagenes = agregar_pestana_imagenes(id_avaluo) """
            
            
            for index in range(tab_panel.count()):
                
                widget = tab_panel.widget(index)
                validacion=(tab_panel.tabText(index) == "PestanaDatosSolicitud")
                
                if tab_panel.tabText(index) == "Datos de la Solicitud":
                    # Si la pestaña ya existe, mover a esa pestaña y actualizar el id_avaluo
                    tab_panel.setCurrentIndex(index)
                    widget.cargar_datos_solicitud(id_avaluo)  # Método para actualizar los datos con el nuevo id_avaluo
                    print(f"Movido a la pestaña existente 'PestanaDatosSolicitud' con id_avaluo: {id_avaluo}")
                    seguimiento_index = tab_panel.indexOf(self)
                    if seguimiento_index != -1:
                        tab_panel.removeTab(seguimiento_index)
                        print("Pestaña de seguimiento cerrada.")
                    return  # Salir de la función para evitar agregar pestañas duplicadas
                
            # Agregar las pestañas al QTabWidget
            PestanaDatosSolicitud(tab_panel, id_avaluo)   
            PestanaCaracteristicasSector(tab_panel, id_avaluo)
            print(f"Movido a la pestaña existente 'PestanaDatosSolicitud' con id_avaluo: {id_avaluo}")
            """ PestanaCaracteristicasSector(self.tab_panel)
            PestanaCaracteristicasConstruccion(self.tab_panel)
            PestanaCondicionesValuacion(self.tab_panel)
            agregar_pestana_imagenes(self.tab_panel)  """
            
            tab_panel.setCurrentIndex(index+1)
            
            seguimiento_index = tab_panel.indexOf(self)
            print("Cantidad de pesta;as : ",(seguimiento_index))
            if tab_panel.count()>1:
                tab_panel.removeTab(index)
                print("Pestaña de seguimiento cerrada.")
    
            print(f"Pestañas agregadas para el avalúo con ID: {id_avaluo}")
                
            
    
        except Exception as e:
            print(f"Error al agregar las pestañas: {e}") 

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
            
    
import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import ( QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar,
                             QTabWidget, QTextEdit, 
                             QGroupBox, QComboBox,QScrollArea,QGridLayout,
                             QSizePolicy, QCheckBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt, QTimer, QDate

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QFileInfo, Qt
from PyQt6.QtGui import QPixmap
from num2words import num2words
from Estilos import Estilos
from Funciones_imagenes import FuncionesImagenes

class PestanaCondicionesValuacion(QWidget):
    def __init__(self, tab_panel: QTabWidget):
        super().__init__()
        
        # Aplicar estilos desde el archivo CSS
        self.group_style = Estilos.cargar_estilos(self, "styles.css")
        
        # Crear el widget principal de la pestaña
        pestana = QWidget()
        
        # Crear scroll area para toda la pestaña
        scroll_area = QScrollArea(pestana)   
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_area.setStyleSheet(self.group_style)  # Aplicar estilos al scroll area
        
        # Crear el widget interno que contendrá los elementos
        contenido = QWidget()
        scroll_area.setWidget(contenido)
        
        # Layout principal vertical para el contenido        
        layout_principal = QGridLayout(contenido)
        layout_principal.setContentsMargins(10, 10, 10, 10)
        layout_principal.setSpacing(15)
        
        # Configurar el mismo ancho para todas las columnas
        columnas = 2  # Número de columnas en el layout
        for i in range(columnas):
            layout_principal.setColumnStretch(i, 1)  # Asignar la misma proporción de expansión
        
        # Configurar política de tamaño
        contenido.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.MinimumExpanding
        )
        
        """ # Crear un layout principal en forma de grid para dividir en dos columnas
        layout_principal = QGridLayout(contenido)   """ 
    
        # 1. Condiciones restrictivas y afectaciones
        grupo_condiciones_restrictivas = QGroupBox("Condiciones restrictivas y afectaciones")
        layout_condiciones_restrictivas = QGridLayout(grupo_condiciones_restrictivas)
    
        layout_condiciones_restrictivas.addWidget(QLabel("Problemas de estabilidad y suelos:"), 0, 0)
        layout_condiciones_restrictivas.addWidget(QLineEdit(), 0, 1)
    
        layout_condiciones_restrictivas.addWidget(QLabel("Impacto ambiental y condiciones de salubridad:"), 1, 0)
        layout_condiciones_restrictivas.addWidget(QLineEdit(), 1, 1)
    
        layout_condiciones_restrictivas.addWidget(QLabel("Seguridad:"), 2, 0)
        layout_condiciones_restrictivas.addWidget(QLineEdit(), 2, 1)
    
        layout_principal.addWidget(grupo_condiciones_restrictivas, 0, 0)
    
        # 2. Condiciones generales
        grupo_condiciones_generales = QGroupBox("Condiciones generales")
        layout_condiciones_generales = QVBoxLayout(grupo_condiciones_generales)
    
        layout_condiciones_generales.addWidget(QLabel("Agregar condiciones:"))
        boton_agregar_condicion = QPushButton("Agregar condición")
        layout_condiciones_generales.addWidget(boton_agregar_condicion)
    
        # Espacio para agregar múltiples condiciones
        lista_condiciones = QVBoxLayout()
        layout_condiciones_generales.addLayout(lista_condiciones)
    
        def agregar_condicion():
            campo_condicion = QLineEdit()
            lista_condiciones.addWidget(campo_condicion)
    
        boton_agregar_condicion.clicked.connect(agregar_condicion)
    
        layout_principal.addWidget(grupo_condiciones_generales,0,1)
    
        # 3. Aspecto económico
        grupo_aspecto_economico = QGroupBox("Aspecto económico")
        layout_aspecto_economico = QGridLayout(grupo_aspecto_economico)
    
        layout_aspecto_economico.addWidget(QLabel("Metodologías valuatorias empleadas:"), 0, 0)
        layout_metodologias = QVBoxLayout()
        metodologias = [
            "Método de comparación o mercado",
            "Método de capitalización de rentas o ingresos",
            "Método de costo de reposición",
            "Método residual"
        ]
        for metodologia in metodologias:
            layout_metodologias.addWidget(QCheckBox(metodologia))
        layout_aspecto_economico.addLayout(layout_metodologias, 0, 1)
    
        layout_aspecto_economico.addWidget(QLabel("Justificación de las metodologías:"), 1, 0)
        layout_aspecto_economico.addWidget(QTextEdit(), 1, 1)
    
        layout_aspecto_economico.addWidget(QLabel("Perspectivas de valorización:"), 2, 0)
        combo_valorizacion = QComboBox()
        combo_valorizacion.addItems(["Bajas", "Normales", "Altas"])
        layout_aspecto_economico.addWidget(combo_valorizacion, 2, 1)
    
        layout_principal.addWidget(grupo_aspecto_economico,1,0)
    
        # 4. Valuación
        grupo_valuacion = QGroupBox("Valuación")
        layout_valuacion = QGridLayout(grupo_valuacion)
    
        layout_valuacion.addWidget(QLabel("Cuadro de liquidación (imágenes):"), 0, 0)
        boton_agregar_imagen = QPushButton("Agregar imagen")
        layout_valuacion.addWidget(boton_agregar_imagen, 0, 1)
        
    
        lista_imagenes = QVBoxLayout()
        
        layout_valuacion.addLayout(lista_imagenes, 1, 0, 1, 2)
        boton_agregar_imagen.clicked.connect(lambda:FuncionesImagenes.agregar_imagen(self, lista_imagenes))
        
        # Contenedor para imágenes y descripciones
        self.valuation_container = QVBoxLayout()
        
        # Lista para almacenar las rutas de las imágenes
        rutas_imagenes = [] 
        
        layout_valuacion.addWidget(QLabel("Valor adoptado:"), 2, 0)
        valor_adoptado = QDoubleSpinBox()
        valor_adoptado.setRange(0, 1000000000000)  # Rango de 0 a 1 billón
        valor_adoptado.setDecimals(0)  # Sin decimales
        layout_valuacion.addWidget(valor_adoptado, 2, 1)
    
        layout_valuacion.addWidget(QLabel("Valor en letras:"), 3, 0)
        valor_en_letras = QLineEdit()
        valor_en_letras.setReadOnly(True)
        layout_valuacion.addWidget(valor_en_letras, 4, 0, 4, 2)
    
        def convertir_a_letras():
            valor = valor_adoptado.value()
            valor_en_letras.setText(num2words(valor, lang="es")+ " Pesos")
    
        valor_adoptado.valueChanged.connect(convertir_a_letras)
    
        layout_principal.addWidget(grupo_valuacion,1,1)
        
        pestana_layout = QVBoxLayout(pestana)
        pestana_layout.addWidget(scroll_area)
        pestana_layout.setContentsMargins(0, 0, 0, 0)
        
        """ # Configurar el scroll area
        scroll_area.setWidget(contenido)  """   
    
        # Agregar la pestaña al panel
        
        tab_panel.addTab(pestana, "Condiciones generales y Valoración")
        


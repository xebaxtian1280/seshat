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
from Funciones import Funciones

class PestanaCaracteristicasConstruccion(QWidget):
    def __init__(self, tab_panel: QTabWidget):
        super().__init__()
    # Widget principal para la pestaña
        
        pestana = QWidget()
        
        # Crear scroll area para toda la pestaña
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                width: 10px;
                background-color: #f0f0f0;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Cargar estilos desde el archivo CSS
        group_style =  Estilos.cargar_estilos(self,"styles.css")
        
        # Widget contenedor del contenido
        contenido = QWidget()
        scroll_area.setWidget(contenido)
        
        # Layout principal vertical para el contenido
        layout_principal = QVBoxLayout(contenido)
        layout_principal.setContentsMargins(10, 10, 10, 10)
        layout_principal.setSpacing(15)
        
        # Configurar política de tamaño
        contenido.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.MinimumExpanding
        )
        
        # =================================================================
        # FILA HORIZONTAL: DATOS GENERALES + ESPECIFICACIONES CONSTRUCTIVAS
        # =================================================================
        fila_superior = QWidget()
        layout_fila = QHBoxLayout(fila_superior)
        layout_fila.setContentsMargins(0, 0, 0, 0)
        layout_fila.setSpacing(15)
        
        # Grupo 1: Datos Generales
        grupo_datos = QGroupBox("Datos Generales")
        grupo_datos.setStyleSheet(group_style)
        form_datos = QFormLayout(grupo_datos)
        
        # Campos de datos generales
        self.num_pisos = QSpinBox()
        self.num_pisos.setRange(0, 100)
        
        self.num_sotanos = QSpinBox()
        self.num_sotanos.setRange(0, 10)
        
        self.vetustez = QLineEdit()
        self.vida_util = QLineEdit()
        self.vida_restante = QLineEdit()
        
        form_datos.addRow("Número de Pisos:", self.num_pisos)
        form_datos.addRow("Sótanos:", self.num_sotanos)
        form_datos.addRow("Vetustez:", self.vetustez)
        form_datos.addRow("Vida Útil:", self.vida_util)
        form_datos.addRow("Vida Restante:", self.vida_restante)
        
        # Grupo 2: Croquis de la construcción
        grupo_croquis = QGroupBox("Croquis de la Construcción")
        grupo_croquis.setStyleSheet(group_style)
        layout_croquis = QVBoxLayout(grupo_croquis)
        
        # Contenedor para imágenes y descripciones
        self.croquis_container = QVBoxLayout()
        
        # Botón para agregar croquis
        btn_agregar_croquis = QPushButton("Agregar Croquis")
        btn_agregar_croquis.clicked.connect(lambda: Funciones.agregar_imagen(self, self.croquis_container))
        
        layout_croquis.addLayout(self.croquis_container)
        layout_croquis.addWidget(btn_agregar_croquis)
        
        # Grupo 3: Área construida
        grupo_area = QGroupBox("Área Construida")
        grupo_area.setStyleSheet(group_style)
        layout_area = QVBoxLayout(grupo_area)
        
        # Crear tabla
        self.tabla_area = QTableWidget(0, 4)  # 0 filas iniciales, 3 columnas
        self.tabla_area.setHorizontalHeaderLabels(["Identificación", "Área (m²)", "Destinación", "Dependencias"])
        
        # Configurar tabla
        self.tabla_area.horizontalHeader().setStretchLastSection(True)
        self.tabla_area.verticalHeader().setVisible(False)
        self.tabla_area.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        
        # Botones para tabla
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_agregar_fila = QPushButton("Agregar Fila")
        btn_eliminar_fila = QPushButton("Eliminar Fila")
        
        btn_agregar_fila.clicked.connect(self.agregar_fila_area)
        btn_eliminar_fila.clicked.connect(self.eliminar_fila_area)
        
        btn_layout.addWidget(btn_agregar_fila)
        btn_layout.addWidget(btn_eliminar_fila)
        
        layout_area.addWidget(self.tabla_area)
        layout_area.addWidget(btn_frame)
        
        # Grupo 4: Estado de conservación
        
        """ fila_inferior = QWidget()
        layout_fila_i = QHBoxLayout(v)
        layout_fila_i.setContentsMargins(0, 0, 0, 0)
        layout_fila_i.setSpacing(15) """
        
        grupo_estado = QGroupBox("Estado de Conservación")
        grupo_estado.setStyleSheet(group_style)
        form_estado = QFormLayout(grupo_estado)
        
        self.estructura = QTextEdit()
        self.acabados = QTextEdit()
        
        self.estructura.setFixedHeight(100)
        self.acabados.setFixedHeight(100)
        
        """ layout_fila_i.addWidget(self.estructura)        
        layout_fila_i.addWidget(self.acabados) """
        
        form_estado.addRow("Estructura:", self.estructura)
        form_estado.addRow("Acabados:", self.acabados)
        
        # Grupo 5: Especificaciones constructivas
        grupo_especificaciones = QGroupBox("Especificaciones Constructivas")
        grupo_especificaciones.setStyleSheet(group_style)
        form_especificaciones = QFormLayout(grupo_especificaciones)
        
        # Listas de opciones
        opciones_cimentacion = [
            "",
            "Ciclopea", 
            "Zapatas aisladas en concreto reforzado", 
            "Zapata corrida en concreto reforzado", 
            "Sin cimentación"
        ]
        
        opciones_estructura = [
            "",
            "Muros de Carga", 
            "Tradicional", 
            "Mampostería estructural", 
            "Mampostería confinada", 
            "Industrializada", 
            "Mixto"
        ]
        
        opciones_muros = [            
            "",
            "Ladrillo a la vista", 
            "Pañete y pintura", 
            "Estuco y Pintura", 
            "Carraplast", 
            "Estuco acrílico"
        ]
        
        opciones_cubierta = [
            "",
            "Teja en Fibrocemento", 
            "Teja de Zinc", 
            "Cerámica", 
            "Madera", 
            "Policarbonato", 
            "Placa en Concreto"
        ]
        
        opciones_fachada = [
            "",
            "Ladrillo a la vista", 
            "Carraplast", 
            "Cemento afinado", 
            "Pañete y pintura", 
            "Cerámica", 
            "Madera"
        ]
        
        opciones_cielo_raso = [
            "",
            "PVC", 
            "Placa de yeso", 
            "Madera", 
            "Metal", 
            "Fibra de vidrio"
        ]
        
        # Crear comboboxes
        self.cimentacion = QComboBox()
        self.cimentacion.addItems(opciones_cimentacion)
        
        self.estructura_const = QComboBox()
        self.estructura_const.addItems(opciones_estructura)
        
        self.muros = QComboBox()
        self.muros.addItems(opciones_muros)
        
        self.cubierta = QComboBox()
        self.cubierta.addItems(opciones_cubierta)
        
        self.fachada = QComboBox()
        self.fachada.addItems(opciones_fachada)
        
        self.cielo_raso = QComboBox()
        self.cielo_raso.addItems(opciones_cielo_raso)
        
        # Agregar al formulario
        
        form_especificaciones.addRow("Cimentación:", self.cimentacion)
        form_especificaciones.addRow("Estructura:", self.estructura_const)
        form_especificaciones.addRow("Muros:", self.muros)
        form_especificaciones.addRow("Cubierta:", self.cubierta)
        form_especificaciones.addRow("Fachada:", self.fachada)
        form_especificaciones.addRow("Cielo raso:", self.cielo_raso)
        
        # Agregar grupos a la fila horizontal
        layout_fila.addWidget(grupo_datos, 2)
        layout_fila.addWidget(grupo_especificaciones, 4)
        layout_fila.addWidget(grupo_croquis, 4)
        
        # Organizar grupos en el layout principal
        layout_principal.addWidget(fila_superior)
        layout_principal.addWidget(grupo_area)
        layout_principal.addWidget(grupo_estado)
        layout_principal.addStretch()
        
        # Layout para la pestaña (solo contiene el scroll area)
        pestana_layout = QVBoxLayout(pestana)
        pestana_layout.addWidget(scroll_area)
        pestana_layout.setContentsMargins(0, 0, 0, 0)
        
        tab_panel.addTab(pestana, "Características de Construcción")
        
        # Agregar fila inicial a la tabla
        self.agregar_fila_area()
    # Métodos auxiliares
    def agregar_croquis(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar croquis", "", "Imágenes (*.png *.jpg *.jpeg)"
        )
        if file_name:
            contenedor = QWidget()
            layout = QHBoxLayout(contenedor)
            
            # Mostrar imagen reducida
            label = QLabel()
            pixmap = QPixmap(file_name)
            label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            
            # Campo de descripción
            descripcion = QLineEdit()
            descripcion.setPlaceholderText("Descripción del croquis")
            
            # Botón para eliminar
            btn_eliminar = QPushButton("X")
            btn_eliminar.setStyleSheet("color: red;")
            btn_eliminar.clicked.connect(lambda: self.eliminar_croquis(contenedor))
            
            layout.addWidget(label)
            layout.addWidget(descripcion)
            layout.addWidget(btn_eliminar)
            
            self.croquis_container.addWidget(contenedor)

    def eliminar_croquis(self, widget):
        self.croquis_container.removeWidget(widget)
        widget.deleteLater()

    def agregar_fila_area(self):
        row_count = self.tabla_area.rowCount()
        self.tabla_area.insertRow(row_count)
        
        # Identificación
        id_item = QTableWidgetItem()
        self.tabla_area.setItem(row_count, 0, id_item)
        
        # Área (solo números)
        area_item = QTableWidgetItem()
        area_item.setFlags(area_item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.tabla_area.setItem(row_count, 1, area_item)
        
        # Destinación
        dest_item = QTableWidgetItem()
        self.tabla_area.setItem(row_count, 2, dest_item)

    def eliminar_fila_area(self):
        current_row = self.tabla_area.currentRow()
        if current_row >= 0:
            self.tabla_area.removeRow(current_row)

    
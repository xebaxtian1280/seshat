import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar,
                             QFileDialog, QMenuBar, QMenu, QTabWidget, QTextEdit, 
                             QFormLayout, QGroupBox, QSpinBox, QComboBox, QDateEdit, QListWidget, QListWidgetItem,QScrollArea,QTableWidgetItem,QTableWidget,QGridLayout,
                             QSizePolicy, QCheckBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import  Qt


class PestanaCaracteristicasSector(QWidget):
    def __init__(self, tab_panel: QTabWidget):
        super().__init__()
        
        # Aquí va el contenido de la función crear_pestana_caracteristicas_sector
        group_style = """
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                margin-top: 10px;
                border: 1px solid #cccccc;
                padding-top: 15px;
                
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """
        pestana = QWidget()
        
        # Crear scroll area para toda la pestaña
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Widget contenedor para el contenido
        
        contenido = QWidget()
        scroll_area.setWidget(contenido) 
        main_layout = QVBoxLayout(contenido)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Columna izquierda
        
        left_column = QVBoxLayout() 
        left_column.setSpacing(10)
        
        # Grupo 1: Delimitación del sector
        grupo_delimitacion = QGroupBox("Delimitación del Sector")
        grupo_delimitacion.setStyleSheet(group_style)
        form_delimitacion = QFormLayout(grupo_delimitacion)
        
        self.norte = QLineEdit()
        self.sur = QLineEdit()
        self.oriente = QLineEdit()
        self.occidente = QLineEdit()
        
        form_delimitacion.addRow("Norte:", self.norte)
        form_delimitacion.addRow("Sur:", self.sur)
        form_delimitacion.addRow("Oriente:", self.oriente)
        form_delimitacion.addRow("Occidente:", self.occidente)
        
        left_column.addWidget(grupo_delimitacion)
        left_column.addStretch()
        
        # Grupo: Vias Publicas
        altura_textos = 70
        grupo_vias = QGroupBox("Vias Publicas")
        grupo_vias.setStyleSheet(group_style)
        contenido_vias = QWidget() 
        form_vias = QFormLayout(grupo_vias)        
           
        self.vias_principales_texto = QTextEdit()
        self.vias_principales_texto.setPlaceholderText(
            "Las vı́as principal más importantes de la zona corresponden a la carrera 15 y calle 3. Se desplaza un alto flujo vehicular y se desarrolla la mayor actividad comercial de la zona, en general se encuentra en buen estado de conservación."
        )
        self.vias_principales_texto.setFixedHeight(altura_textos)
        form_vias.addRow("Principales", self.vias_principales_texto)
        
        self.vias_secundarias_texto = QTextEdit()
        self.vias_secundarias_texto.setPlaceholderText(
            "Cuenta con vı́as para acceder al sector, como la Calle 9 y Carrera 19. Se encuentran en buen estado de conservación."
        )
        self.vias_secundarias_texto.setFixedHeight(altura_textos)
        form_vias.addRow("Secundarias", self.vias_secundarias_texto)
        
        self.transporte_texto = QTextEdit()
        self.transporte_texto.setPlaceholderText(
            "El servicio de transporte público es suministrado principalmente por buses, busetas, colectivos y taxis, que comunican a los diferentes puntos del municipio."
        )
        self.transporte_texto.setFixedHeight(altura_textos)
        form_vias.addRow("Trasnporte", self.transporte_texto)
        
        left_column.addWidget(grupo_vias)
       
        
        # Grupo 2: Amoblamiento urbano
        grupo_amoblamiento = QGroupBox("Amoblamiento urbano")
        grupo_amoblamiento.setStyleSheet(group_style)
        layout_amoblamiento = QVBoxLayout(grupo_amoblamiento)     
        
           
        self.amoblamiento_texto = QTextEdit()
        layout_amoblamiento.addWidget(self.amoblamiento_texto)
        
        # Nuevo Grupo: Servicios Públicos
        grupo_servicios = QGroupBox("Servicios Públicos")
        grupo_servicios.setStyleSheet(group_style)
        servicios_layout = QVBoxLayout(grupo_servicios)    
        
        # Crear widget para dos columnas
        column_widget = QWidget()
        column_layout = QHBoxLayout(column_widget)
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        # Dividir servicios en dos columnas
        servicios = [
            "Acueducto", "Gas Natural", "Telefonía Fija",
            "Recolección de Basuras", "Alcantarillado", 
            "Energía Eléctrica", "Contador de Agua", 
            "Contador de Energia", "Contador de Gas"
        ]
        mitad = len(servicios) // 2

        for i, servicio in enumerate(servicios):
            cb = QCheckBox(servicio)
            #self.checkbox_servicios[servicio] = cb
            if i < mitad:
                col1.addWidget(cb)
            else:
                col2.addWidget(cb)

        column_layout.addLayout(col1)
        column_layout.addLayout(col2)
        servicios_layout.addWidget(column_widget)
        
        
        # left_column.addWidget(grupo_amoblamiento)
        # left_column.addStretch() 
        
        # Columna derecha
        right_column = QVBoxLayout()
        right_column.setSpacing(10)        
                
        # Grupo 3: Norma urbanística
        grupo_norma = QGroupBox("Norma urbanística")
        grupo_norma.setStyleSheet(group_style)
        layout_norma = QHBoxLayout(grupo_norma)
        
        # Instrumentos de OT
        self.instrumentos_ot = QTextEdit()
        self.instrumentos_ot.setPlainText(
            "Conforme al Plan de Ordenamiento Territorial, aprobado mediante acuerdo N° 0000 de 20xx "
            "Por el cual se adopta el Plan de Ordenamiento Territorial de segunda generación del Municipio de XXXXX."
        )
        self.instrumentos_ot.setFixedHeight(100)
        
        # Subgrupo Usos


        subgroup_style = """
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #e0e0e0;
                margin-top: 5px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 5px;
                padding: 0 2px;
            }
        """
        
        subgrupo_usos = QGroupBox("Usos")   
        subgrupo_usos.setStyleSheet(subgroup_style)
        
            # Crear scroll area
        scroll_usos = QScrollArea()
        scroll_usos.setWidgetResizable(True)
        scroll_usos.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Widget contenedor para el formulario
        contenido_usos = QWidget()  
        form_usos = QFormLayout(contenido_usos)
        
        # Descripción
        self.descripcion_usos = QTextEdit()
        form_usos.addRow("Descripción:", self.descripcion_usos)
        
        # Imágenes
        self.imagenes_usos_layout = QVBoxLayout()
        btn_agregar_imagen = QPushButton("Agregar imagen")
        btn_agregar_imagen.clicked.connect(self.agregar_imagen_usos)
        form_usos.addRow(btn_agregar_imagen)
        form_usos.addRow(self.imagenes_usos_layout)
        
        # Listas dinámicas de usos
        categorias_usos = [
            ("Principales", self.crear_lista_usos),
            ("Complementarios", self.crear_lista_usos),
            ("Condicionado", self.crear_lista_usos),
            ("Permitido", self.crear_lista_usos),
            ("Prohibido", self.crear_lista_usos)
        ]
        
        for nombre, funcion in categorias_usos:
            form_usos.addRow(funcion(nombre))
            
        scroll_usos.setWidget(contenido_usos)
    
        # Layout para el grupo de usos
        layout_usos = QVBoxLayout(subgrupo_usos)
        layout_usos.addWidget(scroll_usos)
        
        # Subgrupo Tratamientos
        subgrupo_tratamientos = QGroupBox("Tratamientos")
        form_tratamientos = QFormLayout(subgrupo_tratamientos)
        
        # Descripción tratamientos
        self.descripcion_tratamientos = QTextEdit()
        self.descripcion_tratamientos.setPlainText("De acuerdo con la consulta del POT, el predio se encuentra ubicado en una zona de tratamiento de xxxxxxxxx.")
        self.descripcion_tratamientos.setFixedHeight(100)        
        form_tratamientos.addRow("Descripción:", self.descripcion_tratamientos)
        
        # Imágenes tratamientos
        self.imagenes_tratamientos_layout = QVBoxLayout()
        btn_agregar_imagen_trat = QPushButton("Agregar imagen")
        btn_agregar_imagen_trat.clicked.connect(self.agregar_imagen_tratamientos)
        form_tratamientos.addRow(btn_agregar_imagen_trat)
        form_tratamientos.addRow(self.imagenes_tratamientos_layout)
        
        left_column_norma = QVBoxLayout() 
        right_column_norma = QVBoxLayout() 
        
        
        left_column_norma.addWidget(subgrupo_usos)
        right_column_norma.addWidget(QLabel("Instrumentos de OT:"))
        right_column_norma.addWidget(self.instrumentos_ot)
        right_column_norma.addWidget(subgrupo_tratamientos)
        
        layout_norma.addLayout(right_column_norma)
        layout_norma.addLayout(left_column_norma)
        
        # layout_norma.addWidget(subgrupo_usos)
        # layout_norma.addWidget(subgrupo_tratamientos)
        
        #Agrega Grupo norma a la columna de la derecha
        
        right_column.addWidget(grupo_amoblamiento)
        right_column.addWidget(grupo_servicios)
        
        right_column.addStretch()  
        
        
        # Ensamblar layout
        
        top_box = QHBoxLayout() 
        top_box.setSpacing(10)
        top_box.addLayout(right_column)
        top_box.addLayout(left_column)
        
        
        # CONFIGURACIÓN FINAL DEL LAYOUT
        # --------------------------------------------------
        
        main_layout.addLayout(top_box)        
        main_layout.addWidget(grupo_norma)
              
        
        # Establecer política de tamaño para que se expanda verticalmente
        contenido.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.MinimumExpanding
        )
        
        # Agregar el scroll area al layout de la pestaña
        pestana_layout = QVBoxLayout(pestana)
        pestana_layout.addWidget(scroll_area)
        pestana_layout.setContentsMargins(0, 0, 0, 0)
        
        tab_panel.addTab(pestana, "Características del Sector")
    
    def crear_lista_usos(self, nombre):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        combo = QComboBox()
        combo.addItems([
            "Residencial", "Comercio", "Comercio liviano", 
            "Comercio Pesado", "Servicios", "Industrial", 
            "Industria liviana", "Industria pesada", 
            "Dotacional", "Protección"
        ])
        
        lista = QListWidget()
        btn_agregar = QPushButton("Agregar")
        
        # Conectar con la función usando lambda y pasando los elementos específicos
        btn_agregar.clicked.connect(lambda: self.agregar_uso(combo, lista))
        
        layout.addWidget(combo)
        layout.addWidget(btn_agregar)
        layout.addWidget(lista)
        
        grupo = QGroupBox(nombre)
        grupo.setLayout(QVBoxLayout())
        grupo.layout().addWidget(widget)
        
        return grupo

    def agregar_uso(self, combo, lista):
        
        item = QListWidgetItem(combo.currentText())
        lista.addItem(item)
        
    def agregar_imagen_usos(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.mostrar_imagen(file_name, self.imagenes_usos_layout)

    def agregar_imagen_tratamientos(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.mostrar_imagen(file_name, self.imagenes_tratamientos_layout)

    def mostrar_imagen(self, file_path, layout):
        contenedor = QWidget()
        hbox = QHBoxLayout(contenedor)
        
        label = QLabel()
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        
        btn_eliminar = QPushButton("X")
        btn_eliminar.setStyleSheet("color: red;")
        btn_eliminar.clicked.connect(lambda: self.eliminar_imagen(contenedor))
        
        hbox.addWidget(label)
        hbox.addWidget(btn_eliminar)
        
        layout.addWidget(contenedor)

    def eliminar_imagen(self, widget):
        widget.deleteLater()

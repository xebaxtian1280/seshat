import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar,
                             QFileDialog, QMenuBar, QMenu, QTabWidget, QTextEdit, 
                             QFormLayout, QGroupBox, QSpinBox, QComboBox, QDateEdit, QListWidget, QListWidgetItem,QScrollArea,
                             QSizePolicy, QCheckBox)
from PyQt6.QtCore import Qt, QTimer, QDate
from funciones import generar_informe
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QFileInfo, Qt
from PyQt6.QtGui import QPixmap

import tkinter as tk

QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

class ReportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal
        
        ancho = root.winfo_screenwidth()
        alto = root.winfo_screenheight()
        
        root.destroy()
        
        self.setWindowTitle("Sistema de Gestión de Informes")
        self.setMinimumSize(1000, 700)
        self.default_save_path = str(Path.home() / "/Proyectos/seshat/informe/Resultados")
        self.init_ui()
        
    def init_ui(self):
        # Configurar widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Barra de menú integrada en el panel
        menu_bar = QMenuBar()
        file_menu = QMenu("&Archivo", self)
        
        # Acciones del menú
        generar_action = file_menu.addAction("Generar Informe")
        generar_action.triggered.connect(self.iniciar_generacion)
        
        ubicacion_action = file_menu.addAction("Guardar Como")
        ubicacion_action.triggered.connect(self.seleccionar_ubicacion)
        
        crear_proyecto = file_menu.addAction("Crear Proyecto")
        crear_proyecto.triggered.connect(self.crea_proyecto)
        
        abrir_proyecto = file_menu.addAction("Abrir proyecto")
        abrir_proyecto.triggered.connect(self.carga_proyecto)
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Salir")
        exit_action.triggered.connect(self.close)
        
        menu_bar.addMenu(file_menu)
        main_layout.addWidget(menu_bar)
        
        # Panel de pestañas
        tab_panel = QTabWidget()
        
        # Crear pestañas
        self.crear_pestana_datos_solicitud(tab_panel)
        self.crear_pestana_caracteristicas_sector(tab_panel)
        self.crear_pestana_info_basica(tab_panel)
        self.crear_pestana_info_juridica(tab_panel)
        
        
        main_layout.addWidget(tab_panel)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)
    
    def crear_pestana_datos_solicitud(self, tab_panel):
        
        
        # Estilo reutilizable
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
        main_layout = QHBoxLayout(pestana)
        
        # Columna izquierda - Contenedor vertical
        left_column = QVBoxLayout()
        
        # Grupo Datos de la Solicitud
        grupo_solicitud = QGroupBox("Datos del Cliente")
        grupo_solicitud.setStyleSheet(group_style)
        solicitud_layout = QFormLayout(grupo_solicitud)
        
        # Campos de solicitud
        self.cliente = QLineEdit()
        self.doc_identidad = QLineEdit()
        self.doc_identidad.setInputMask("9999999999")  # Máscara para 10 dígitos
        self.destinatario = QLineEdit()
        self.fecha_visita = QDateEdit(QDate.currentDate())
        self.fecha_informe = QDateEdit(QDate.currentDate())
        
        solicitud_layout.addRow("Cliente:", self.cliente)
        solicitud_layout.addRow("Documento de identificación:", self.doc_identidad)
        solicitud_layout.addRow("Destinatario del Avalúo:", self.destinatario)
        solicitud_layout.addRow("Fecha de la visita:", self.fecha_visita)
        solicitud_layout.addRow("Fecha del informe:", self.fecha_informe)
        
        # Grupo Información Jurídica y Catastral
        grupo_juridico = QGroupBox("Información Jurídica y Catastral")
        grupo_juridico.setStyleSheet(group_style)
        juridico_layout = QFormLayout(grupo_juridico)
        
        # Campos jurídicos
        self.propietario = QLineEdit()
        self.id_propietario = QLineEdit()
        self.doc_propiedad = QTextEdit()
        self.doc_propiedad.setPlainText("Copia simple de la Escritura Pública No. 4126 del 26 de Noviembre de 1997, otorgada en la Notaria 2 de Bucaramanga.")
        
        # Contenedor para matrículas dinámicas
        self.matricula_container = QWidget()
        self.matricula_layout = QVBoxLayout(self.matricula_container)
        self.matricula_layout.setContentsMargins(0, 0, 0, 0)
        
        # Botón para agregar matrículas
        btn_agregar_matricula = QPushButton("Agregar Matrícula")
        btn_agregar_matricula.clicked.connect(self.agregar_campo_matricula)
        btn_agregar_matricula.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
        self.cedula_catastral = QLineEdit()
        self.modo_adquisicion = QComboBox()
        self.modo_adquisicion.addItems([
            "Compraventa", 
            "Adjudicación en Sucesión", 
            "Transferencia a título de fiducia mercantil", 
            "Compra parcial"
        ])
        self.limitaciones = QTextEdit()
        
        juridico_layout.addRow("Propietario:", self.propietario)
        juridico_layout.addRow("ID Propietario:", self.id_propietario)
        juridico_layout.addRow("Documento de propiedad:", self.doc_propiedad)
        
        self.agregar_campo_matricula()    
        juridico_layout.addRow("Matrícula Inmobiliaria:", self.matricula_container)
        juridico_layout.addRow(btn_agregar_matricula)
        
        juridico_layout.addRow("Cédula Catastral:", self.cedula_catastral)
        juridico_layout.addRow("Modo de adquisición:", self.modo_adquisicion)
        juridico_layout.addRow("Limitaciones y gravámenes:", self.limitaciones)
        
        left_column.addWidget(grupo_solicitud)
        left_column.addWidget(grupo_juridico)
        left_column.addStretch() 
        
        # Columna derecha - Datos del inmueble
        grupo_inmueble = QGroupBox("Datos del Inmueble")
        
        grupo_inmueble.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                margin-top: 10px;
                border: 1px solid #cccccc;
            }
        """)
        right_layout = QFormLayout(grupo_inmueble)
        
        # Campos nuevos del inmueble
        self.direccion_inmueble = QLineEdit()
        self.barrio_inmueble = QLineEdit()
        self.municipio_inmueble = QLineEdit()
        self.departamento_inmueble = QLineEdit()
        
        self.tipo_inmueble = QComboBox()
        self.tipo_inmueble.addItems(["Apartamento", "Casa", "Oficina", "Bodega", "Local", "Lote", "Finca", "Consultorio", "Hospital", "Colegio", "Edificio"])
        
        self.tipo_avaluo = QComboBox()
        self.tipo_avaluo.addItems(["Comercial", "Jurídico", "Financiero", "Seguros"])
        
        self.latitud = QLineEdit()
        self.latitud.setPlaceholderText("4.6097")
        self.longitud = QLineEdit()
        self.longitud.setPlaceholderText("-74.0817")
        
        # Documentación dinámica
        grupo_documentos = QGroupBox("Documentación Aportada")
        self.documentacion_layout = QVBoxLayout(grupo_documentos)
        self.btn_agregar_doc = QPushButton("Agregar Documento")
        self.btn_agregar_doc.clicked.connect(self.agregar_campo_documento)
        
        # Campos iniciales
        self.agregar_campo_documento()  # Primer campo por defecto
        right_layout.addRow("Tipo de inmueble:", self.tipo_inmueble)
        right_layout.addRow("Dirección del inmueble:", self.direccion_inmueble)
        right_layout.addRow("Barrio / Vereda:", self.barrio_inmueble)
        right_layout.addRow("Municipio:", self.municipio_inmueble)
        right_layout.addRow("Departamento:", self.departamento_inmueble)
        right_layout.addRow("Tipo de avalúo:", self.tipo_avaluo)
        right_layout.addRow(QLabel("Coordenadas:"))
        right_layout.addRow("Latitud:", self.latitud)
        right_layout.addRow("Longitud:", self.longitud)
        right_layout.addRow(QLabel("Documentación aportada:"))
        right_layout.addWidget(grupo_documentos)
        right_layout.addWidget(self.btn_agregar_doc)
        
        # Columna izquierda - Contenedor vertical
        right_column = QVBoxLayout()
        
         # Agregar grupos a la columna izquierda
        right_column.addWidget(grupo_inmueble)
        right_column.addStretch()
    
        
        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column) 
        
        tab_panel.addTab(pestana, "Datos de la Solicitud")
        
        # Grupo para el mapa
        grupo_mapa = QGroupBox("Ubicación Geográfica")
        grupo_mapa.setStyleSheet(group_style)
        mapa_layout = QVBoxLayout(grupo_mapa)
        
        # Widget para el mapa
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(300)
        
        # Botón para actualizar mapa
        btn_actualizar = QPushButton("Actualizar Mapa")
        btn_actualizar.clicked.connect(self.actualizar_mapa)
        
        mapa_layout.addWidget(self.web_view)
        mapa_layout.addWidget(btn_actualizar)
        
        # Agregar el mapa debajo del grupo del inmueble
        right_column.addWidget(grupo_mapa)
    
        # Cargar mapa inicial
        self.actualizar_mapa()
        
    def actualizar_mapa(self):
        # Obtener coordenadas de los campos
        lat = self.latitud.text().strip() or "4.6097"  # Bogotá por defecto
        lon = self.longitud.text().strip() or "-74.0817"
        

        
        """ try:
            lat = float(self.latitud.text())
            lon = float(self.longitud.text())
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Coordenadas inválidas")
            return """
        
        # Generar HTML con el mapa
        mapa_html =  f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mapa del Inmueble</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style>
                #map {{ 
                    height: 300px;
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                // Solución para CORS y User-Agent
                L.Browser.any3d = false; // Desactivar aceleración hardware
                L.TileLayer.include({{
                    createTile: function (coords, done) {{
                        var tile = document.createElement('img');
                        tile.onload = L.bind(this._tileOnLoad, this, done, tile);
                        tile.onerror = L.bind(this._tileOnError, this, done, tile);
                        tile.src = this.getTileUrl(coords);
                        tile.setAttribute('referrerpolicy', 'no-referrer');
                        tile.setAttribute('crossorigin', 'anonymous');
                        return tile;
                    }}
                }});
                
                var map = L.map('map', {{
                    attributionControl: false,
                    zoomControl: false
                }}).setView([{lat}, {lon}], 16);
                
                // Usar servidores alternativos
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    subdomains: 'abc', // Usar subdominios alternativos
                    noWrap: true,
                    maxZoom: 19,
                    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                }}).addTo(map);
                
                L.marker([{lat}, {lon}]).addTo(map);
            </script>
        </body>
        </html>
        '''
        
        self.web_view.setHtml(mapa_html)
        # self.habilitar_permisos_webengine()
        
    # def habilitar_permisos_webengine(self):
    #     # Configuraciones esenciales para QtWebEngine
    #     settings = self.web_view.settings()
    #     settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    #     settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    #     settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
    #     settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
    #     settings.setUnknownUrlSchemePolicy(QWebEngineSettings.UnknownUrlSchemePolicy.AllowAllUnknownUrlSchemes)
        
    def agregar_campo_matricula(self):
        campo = QLineEdit()
        campo.setPlaceholderText("Ingrese número de matrícula")
        campo.setStyleSheet("""
            QLineEdit {
                margin-bottom: 5px;
                border: 1px solid #ccc;
                padding: 3px;
            }
        """)
        btn_eliminar = QPushButton("×")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                color: #ff0000;
                font-weight: bold;
                border: none;
                min-width: 20px;
                max-width: 20px;
            }
            QPushButton:hover {
                background-color: #ffe0e0;
            }
        """)
        
        # Contenedor para el campo y el botón
        campo_container = QWidget()
        layout_container = QHBoxLayout(campo_container)
        layout_container.addWidget(campo)
        layout_container.addWidget(btn_eliminar)
        layout_container.setContentsMargins(0, 0, 0, 0)
        
        # Conectar el botón de eliminar
        btn_eliminar.clicked.connect(lambda: self.eliminar_campo_matricula(campo_container))
        
        self.matricula_layout.addWidget(campo_container)

    def eliminar_campo_matricula(self, contenedor_a_eliminar):
        # Remover el widget contenedor del layout
        self.matricula_layout.removeWidget(contenedor_a_eliminar)
        
        # Eliminar los widgets hijos
        contenedor_a_eliminar.deleteLater()
    
    def obtener_matriculas(self):
        matriculas = []
        for i in range(self.matricula_layout.count()):
            item = self.matricula_layout.itemAt(i)
            if item and item.widget():
                contenedor = item.widget()
                line_edit = contenedor.findChild(QLineEdit)
                if line_edit and line_edit.text().strip():
                    matriculas.append(line_edit.text().strip())
        return matriculas

    def agregar_campo_documento(self):
        campo = QLineEdit()
        campo.setPlaceholderText("Nombre del documento")
        campo.setClearButtonEnabled(True)
        self.documentacion_layout.addWidget(campo)
        
        
        
# ------------------------------------------------Pestañas Caracteristicas del sector --------------------------------------------------------------

    def crear_pestana_caracteristicas_sector(self, tab_panel):
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
        
        main_layout.addLayout(top_box)   # 40% del ancho        
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

    # Estilo común para los grupos
    
        
# ------------------------------------------------Pestaña Informacion Juridica --------------------------------------------------------------   
    def crear_pestana_info_basica(self, tab_panel):
        pestana = QWidget()
        layout = QFormLayout()
        
        self.nombre_proyecto = QLineEdit()
        self.ubicacion = QLineEdit()
        self.area_total = QSpinBox()
        self.area_total.setRange(0, 1000000)
        self.descripcion = QTextEdit()
        
        layout.addRow("Nombre del proyecto:", self.nombre_proyecto)
        layout.addRow("Ubicación física:", self.ubicacion)
        layout.addRow("Área total (m²):", self.area_total)
        layout.addRow("Descripción:", self.descripcion)
        
        pestana.setLayout(layout)
        tab_panel.addTab(pestana, "Información Básica")
    
    def crear_pestana_info_juridica(self, tab_panel):
        pestana = QWidget()
        layout = QFormLayout()
        
        self.estado_juridico = QComboBox()
        self.estado_juridico.addItems(["En trámite", "Aprobado", "Rechazado", "En revisión"])
        self.numero_escritura = QLineEdit()
        self.fecha_escritura = QDateEdit()
        self.observaciones = QTextEdit()
        
        layout.addRow("Estado jurídico:", self.estado_juridico)
        layout.addRow("Número de escritura:", self.numero_escritura)
        layout.addRow("Fecha de escritura:", self.fecha_escritura)
        layout.addRow("Observaciones legales:", self.observaciones)
        
        pestana.setLayout(layout)
        tab_panel.addTab(pestana, "Información Jurídica")
    

    
    def seleccionar_ubicacion(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
    def crea_proyecto(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
            
    def carga_proyecto(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
    
    def iniciar_generacion(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_progreso)
        self.timer.start(100)
    
    def actualizar_progreso(self):
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
        else:
            self.timer.stop()
            self.procesar_informe()
            self.progress_bar.hide()
    
    def procesar_informe(self):
        # Recolectar datos de todas las pestañas
        
        # Obtener todas las matrículas
        matriculas = []
        for i in range(self.matricula_layout.count()):
            item = self.matricula_layout.itemAt(i)
            if item and isinstance(item, QHBoxLayout):
                line_edit = item.itemAt(0).widget()
                if line_edit and line_edit.text():
                    matriculas.append(line_edit.text())
        
        contenido = f"""
        --- DATOS DE LA SOLICITUD ---
        Cliente: {self.cliente.text()}
        Documento ID: {self.doc_identidad.text()}
        Destinatario: {self.destinatario.text()}
        Fecha Visita: {self.fecha_visita.date().toString("dd/MM/yyyy")}
        Fecha Informe: {self.fecha_informe.date().toString("dd/MM/yyyy")}
        
        --- INFORMACIÓN JURÍDICA ---
        Propietario: {self.propietario.text()}
        ID Propietario: {self.id_propietario.text()}
        Documento Propiedad: {self.doc_propiedad.toPlainText()}
        Matrícula: {self.matricula_inmobiliaria.text()}
        Cédula Catastral: {self.cedula_catastral.text()}
        Adquisición: {self.modo_adquisicion.currentText()}
        Limitaciones: {self.limitaciones.toPlainText()}
        
        --- CARACTERÍSTICAS DEL SECTOR ---
        Zona: {self.zona.currentText()}
        Equipamientos: {self.equipamientos.toPlainText()}
        Infraestructura: {self.infrastructure.toPlainText()}
        Riesgos: {self.riesgos.toPlainText()}
        """
        
        file_path = f"{self.default_save_path}/informe_{time.strftime('%Y%m%d-%H%M%S')}"
        success, resultado = generar_informe(contenido, file_path)
        
        if success:
            QMessageBox.information(self, "Éxito", f"Informe guardado en:\n{resultado}")
        else:
            QMessageBox.critical(self, "Error", f"Error al generar informe:\n{resultado}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportApp()
    window.show()
    sys.exit(app.exec())
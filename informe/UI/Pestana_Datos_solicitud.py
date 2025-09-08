from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QLineEdit, QTextEdit, QComboBox,
    QDateEdit, QPushButton, QLabel, QTabWidget, QScrollArea
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from Estilos import Estilos
from DB import DB

class PestanaDatosSolicitud(QWidget):
    def __init__(self,  tab_panel: QTabWidget, id_avaluo=None):
        super().__init__()
        self.id_avaluo = id_avaluo
        self.group_style = Estilos.cargar_estilos(self, "styles.css")
                
        # layout principal
        main_layout = QHBoxLayout(self)
        
        # Columna izquierda - Contenedor vertical
        left_column = QVBoxLayout()
        
        # Grupo Datos de la Solicitud
        grupo_solicitud = QGroupBox("Datos del Cliente")
        grupo_solicitud.setStyleSheet(self.group_style)
        solicitud_layout = QFormLayout(grupo_solicitud)
        
        # Campos de solicitud
        self.cliente = QLineEdit()
        self.doc_identidad = QLineEdit()
        self.doc_identidad.setInputMask("9999999999")  # Máscara para 10 dígitos
        self.destinatario = QLineEdit()
        self.fecha_visita = QDateEdit(QDate.currentDate())
        self.fecha_informe = QDateEdit(QDate.currentDate())
        self.tipo_avaluo = QComboBox()
        self.tipo_avaluo.addItems(["","Comercial", "Jurídico", "Financiero", "Seguros"])
        
        solicitud_layout.addRow("Cliente:", self.cliente)
        solicitud_layout.addRow("Documento de identificación:", self.doc_identidad)
        solicitud_layout.addRow("Destinatario del Avalúo:", self.destinatario)
        solicitud_layout.addRow("Fecha de la visita:", self.fecha_visita)
        solicitud_layout.addRow("Fecha del informe:", self.fecha_informe)
        solicitud_layout.addRow("Tipo de avalúo solicitado:", self.tipo_avaluo)
        
        # Grupo Información Jurídica y Catastral
        grupo_juridico = QGroupBox("Información Jurídica y Catastral")
        grupo_juridico.setStyleSheet(self.group_style)
        juridico_layout = QFormLayout(grupo_juridico)
        
        # Contenedor para matrículas dinámicas
        self.matricula_container = QWidget()
        self.matricula_layout = QVBoxLayout(self.matricula_container)
        self.matricula_layout.setContentsMargins(0, 0, 0, 0)
        
        # Documentación dinámica
        grupo_documentos = QGroupBox("Documentación Aportada")
        self.documentacion_layout = QVBoxLayout(grupo_documentos)
        self.btn_agregar_doc = QPushButton("Agregar Documento")
        self.btn_agregar_doc.clicked.connect(self.agregar_campo_documento)
        
        # Botón para agregar matrículas
        btn_agregar_matricula = QPushButton("Agregar Matrícula")
        btn_agregar_matricula.clicked.connect(self.agregar_campo_matricula)
        btn_agregar_matricula.setStyleSheet(self.group_style)
        
        # Botón para radicar solicitud
        btn_radicar_solicitud = QPushButton("Radicar Solicitud")
        btn_radicar_solicitud.clicked.connect(self.radicar_solicitud)
        btn_radicar_solicitud.setStyleSheet(self.group_style)
        
        
        juridico_layout.addRow(grupo_documentos)
        juridico_layout.addRow(self.btn_agregar_doc)
        
        self.agregar_campo_matricula()    
        juridico_layout.addRow("Matrícula Inmobiliaria:", self.matricula_container)
        juridico_layout.addRow(btn_agregar_matricula)
        
        if self.cliente.text() == "":
            juridico_layout.addRow(btn_radicar_solicitud)
        
        left_column.addWidget(grupo_solicitud)
        left_column.addWidget(grupo_juridico)
        left_column.addStretch() 
        
        # Columna derecha - Datos del inmueble
        self.grupo_inmueble = QGroupBox("Datos del Inmueble segun MI-")
        
        self.grupo_inmueble.setStyleSheet(self.group_style)
        right_layout = QFormLayout(self.grupo_inmueble)
        
        # Campos nuevos del inmueble
        self.direccion_inmueble = QLineEdit()
        self.barrio_inmueble = QLineEdit()
        self.municipio_inmueble = QLineEdit()
        self.departamento_inmueble = QLineEdit()
        self.cedula_catastral = QLineEdit()
        self.limitaciones = QTextEdit()
        
        self.modo_adquisicion = QComboBox()
        self.modo_adquisicion.addItems([
            "Compraventa", 
            "Adjudicación en Sucesión", 
            "Transferencia a título de fiducia mercantil", 
            "Compra parcial"
        ])
        
        self.tipo_inmueble = QComboBox()
        self.tipo_inmueble.addItems(["Apartamento", "Casa", "Oficina", "Bodega", "Local", "Lote", "Finca", "Consultorio", "Hospital", "Colegio", "Edificio"])
        
        
        self.latitud = QLineEdit()
        self.latitud.setPlaceholderText("4.6097")
        self.longitud = QLineEdit()
        self.longitud.setPlaceholderText("-74.0817")
        
        self.doc_propiedad = QTextEdit()
        self.doc_propiedad.setPlainText("Copia simple de la Escritura Pública No. 4126 del 26 de Noviembre de 1997, otorgada en la Notaria 2 de Bucaramanga.")
        
        self.btn_guardar_inmueble = QPushButton("Guardar informacion del Inmueble")
        self.btn_agregar_doc.setStyleSheet(self.group_style)
        self.btn_guardar_inmueble.clicked.connect(self.guardar_informacion_inmueble)

        # Campos jurídicos
        self.propietario = QLineEdit()
        self.id_propietario = QLineEdit()
        
        # Campos iniciales
        self.agregar_campo_documento()  # Primer campo por defecto
        right_layout.addRow("Tipo de inmueble:", self.tipo_inmueble)
        right_layout.addRow("Dirección del inmueble:", self.direccion_inmueble)
        right_layout.addRow("Barrio / Vereda:", self.barrio_inmueble)
        right_layout.addRow("Municipio:", self.municipio_inmueble)
        right_layout.addRow("Departamento:", self.departamento_inmueble)
        right_layout.addRow("Cédula Catastral:", self.cedula_catastral)
        right_layout.addRow("Modo de adquisición:", self.modo_adquisicion)
        right_layout.addRow("Limitaciones y gravámenes:", self.limitaciones)
        
        right_layout.addRow(QLabel("Coordenadas:"))
        right_layout.addRow("Latitud:", self.latitud)
        right_layout.addRow("Longitud:", self.longitud)
        right_layout.addRow(QLabel("Documento de Propiedad:"))
        right_layout.addWidget(self.doc_propiedad)
        right_layout.addRow("Propietario:", self.propietario)
        right_layout.addRow("ID Propietario:", self.id_propietario)
        right_layout.addWidget(self.btn_guardar_inmueble)
        #right_layout.addWidget(self.btn_agregar_doc)
        
        # Columna izquierda - Contenedor vertical
        right_column = QVBoxLayout()
        
        # Agregar grupos a la columna izquierda
        right_column.addWidget(self.grupo_inmueble)
        right_column.addStretch()
    
        
        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column) 
                
        # Grupo para el mapa
        grupo_mapa = QGroupBox("Ubicación Geográfica")
        grupo_mapa.setStyleSheet(self.group_style)
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
        
        #Agregar pestaña al Panel con barra de desplazamiento
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self)        
        tab_panel.addTab(scroll_area, "Datos de la Solicitud")
    
        # Cargar mapa inicial
        self.actualizar_mapa()        
        self.cargar_datos_solicitud(self.id_avaluo)
        
    def cargar_datos_solicitud(self, id_avaluo):
        """
        Carga los datos de la solicitud desde la base de datos utilizando el id_avaluo.
        
        :param id_avaluo: ID del avalúo para buscar los datos en la base de datos.
        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
            db.conectar()
            
            print(f"Cargando datos para el avalúo con ID: {self.id_avaluo}")
    
            # Consulta SQL para obtener los datos de la solicitud
            consulta = """
            select a.nombre_cliente , a.id_cliente , a.destinatario, a.fecha_visita ,a.fecha_avaluo , a.tipo_avaluo
            FROM "Avaluos" a 
            left join inmuebles i on a."Avaluo_id" = i.avaluo_id 
            WHERE a."Avaluo_id" = 2
            """.replace("2", str(id_avaluo))
            resultado = db.consultar(consulta)
            
            # Verificar si se encontraron datos
            if resultado:
                
                self.cliente.setText(resultado[0][0])  # Primer campo: cliente
                self.doc_identidad.setText(str(resultado[0][1]))  # Segundo campo: doc_identidad
                self.destinatario.setText(resultado[0][2])  # Tercer campo: destinatario
                self.fecha_visita.setDate(resultado[0][3].date())  # Cuarto campo: fecha_visita  
                self.fecha_informe.setDate(resultado[0][4].date())  # Quinto campo: fecha_informe
                
                index_tipo = self.tipo_avaluo.findText(resultado[0][5])  # Sexto campo: tipo_avaluo
                if index_tipo != -1:
                    self.tipo_avaluo.setCurrentIndex(index_tipo)
            else:
                print(f"No se encontraron datos para el avalúo con ID: {id_avaluo}")
    
        except Exception as e:
            print(f"Error al cargar los datos de la solicitud: {e}")
    
    def radicar_solicitud(self):
        # Obtener datos de la solicitud
        solicitud_data = {
            "cliente": self.cliente.text().strip(),
            "doc_identidad": self.doc_identidad.text().strip(),
            "destinatario": self.destinatario.text().strip(),
            "fecha_visita": self.fecha_visita.date().toString("yyyy-MM-dd"),
            "fecha_informe": self.fecha_informe.date().toString("yyyy-MM-dd"),
            "tipo_avaluo": self.tipo_avaluo.currentText()
        }
        
        # Validar campos requeridos
        if not solicitud_data["cliente"] or not solicitud_data["doc_identidad"] or not solicitud_data["tipo_avaluo"]:
            print("Por favor complete todos los campos requeridos.")
            return
        
        # Guardar los datos en una base de datos o archivo
        db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
        db.conectar()
        db.insertar(
            """INSERT INTO "Avaluos" (nombre_cliente, id_cliente, destinatario, fecha_visita, tipo_avaluo, fecha_avaluo) VALUES (%s, %s, %s, %s, %s, %s)"""
            , (solicitud_data["cliente"], solicitud_data["doc_identidad"], solicitud_data["destinatario"], solicitud_data["fecha_visita"],solicitud_data["tipo_avaluo"], solicitud_data["fecha_informe"]))
        print("Solicitud radicada:", solicitud_data)
        
    def guardar_informacion_inmueble(self):
        # Obtener datos del inmueble
        inmueble_data = {
            "direccion": self.direccion_inmueble.text().strip(),
            "tipo_inmueble": self.tipo_inmueble.currentText(),
            "barrio": self.barrio_inmueble.text().strip(),
            "municipio": self.municipio_inmueble.text().strip(),
            "departamento": self.departamento_inmueble.text().strip(),
            "cedula_catastral": self.cedula_catastral.text().strip(),
            "modo_adquisicion": self.modo_adquisicion.currentText(),
            "limitaciones": self.limitaciones.toPlainText().strip(),
            "latitud": self.latitud.text().strip(),
            "longitud": self.longitud.text().strip(),
            "doc_propiedad": self.doc_propiedad.toPlainText().strip()
        }
        
        db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
        db.conectar()
        
        # Aquí podrías guardar los datos en una base de datos o archivo
        query_insertar = """
        INSERT INTO inmuebles (direccion, tipo_inmueble, area, numero_habitaciones, numero_banos, valor, antiguedad, estado)
        VALUES ({inmueble_data[0]}, {inmueble_data[1]}, {inmueble_data[0]}, %{inmueble_data[0]}, %{inmueble_data[0]}, %{inmueble_data[0]}, %{inmueble_data[0]}, %{inmueble_data[0]});
        """
        print("Información del inmueble guardada:", inmueble_data)
        
    def actualizar_mapa(self):
        # Obtener coordenadas de los campos
        lat = self.latitud.text().strip() or "4.6097"  # Bogotá por defecto
        lon = self.longitud.text().strip() or "-74.0817"
        

        
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
        
    def agregar_campo_matricula(self):
        
        campo = QLineEdit()
        campo.setPlaceholderText("Ingrese número de matrícula")
        campo.setStyleSheet(self.group_style)
        campo.focusInEvent = lambda texto: self.actualizar_titulo(campo.text()) 
        campo.textChanged.connect(lambda: self.actualizar_titulo(campo.text()))
        btn_eliminar = QPushButton("×")
        btn_eliminar.setObjectName("botonEliminar")
        btn_eliminar.setStyleSheet(self.group_style)
        
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
        
    def actualizar_titulo(self, texto):
        # Actualizar el título del grupo_inmueble
        self.grupo_inmueble.setTitle(f"Datos del Inmueble segun MI-{texto}")
    
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
        
        btn_eliminar = QPushButton("×")
        btn_eliminar.setObjectName("botonEliminar")
        btn_eliminar.setStyleSheet(self.group_style)
        
        # Contenedor para el campo y el botón
        campo_container = QWidget()
        layout_container = QHBoxLayout(campo_container)
        layout_container.addWidget(campo)
        layout_container.addWidget(btn_eliminar)
        layout_container.setContentsMargins(0, 0, 0, 0)
        
        # Conectar el botón de eliminar
        btn_eliminar.clicked.connect(lambda: self.eliminar_campo_matricula(campo_container))
        self.documentacion_layout.addWidget(campo_container)

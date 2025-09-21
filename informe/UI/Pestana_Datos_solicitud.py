from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QLineEdit, QTextEdit, QComboBox,
    QDateEdit, QPushButton, QLabel, QTabWidget, QScrollArea, QMessageBox
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
        self.inmuebles = {}  # Lista para almacenar los inmuebles asociados a la matricula
        self.matricula_actual = None  # Variable para almacenar la matrícula actual
                
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
        
        btn_radicar_solicitud = QPushButton("Radicar Solicitud")
        btn_radicar_solicitud.clicked.connect(self.radicar_solicitud)
        btn_radicar_solicitud.setStyleSheet(self.group_style)

        juridico_layout.addRow(grupo_documentos)
        juridico_layout.addRow(self.btn_agregar_doc)
        
        self.agregar_campo_matricula()    
        juridico_layout.addRow("Matrícula Inmobiliaria:", self.matricula_container)
        juridico_layout.addRow(btn_agregar_matricula)
        
        if self.id_avaluo == "":
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
            "",
            "Compraventa", 
            "Adjudicación en Sucesión", 
            "Transferencia a título de fiducia mercantil", 
            "Compra parcial"
        ])
        
        self.tipo_inmueble = QComboBox()
        self.tipo_inmueble.addItems(["","Apartamento", "Casa", "Oficina", "Bodega", "Local", "Lote", "Finca", "Consultorio", "Hospital", "Colegio", "Edificio"])
        
        
        self.latitud = QLineEdit()
        self.latitud.setPlaceholderText("4.6097")
        self.longitud = QLineEdit()
        self.longitud.setPlaceholderText("-74.0817")
        
        self.doc_propiedad = QTextEdit()
        self.doc_propiedad.setPlainText("Copia simple de la Escritura Pública No. 4126 del 26 de Noviembre de 1997, otorgada en la Notaria 2 de Bucaramanga.")
        
        self.btn_guardar_inmueble = QPushButton("Guardar informacion del Inmueble")
        self.btn_agregar_doc.setStyleSheet(self.group_style)
        self.btn_guardar_inmueble.clicked.connect(lambda: self.guardar_informacion_inmueble(self.matricula_actual))

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
        id_avaluo = db.insertar(
           """INSERT INTO "Avaluos" (nombre_cliente, id_cliente, destinatario, fecha_visita, tipo_avaluo, fecha_avaluo) VALUES (%s, %s, %s, %s, %s, %s) returning "Avaluo_id" """
            , (solicitud_data["cliente"], solicitud_data["doc_identidad"], solicitud_data["destinatario"], solicitud_data["fecha_visita"],solicitud_data["tipo_avaluo"], solicitud_data["fecha_informe"]))
        print("Solicitud radicada:", solicitud_data)
        
        print(f"ID del avalúo radicado: {id_avaluo}")
        
        # Recorrer los elementos de matricula_layout y obtener los textos de los QLineEdit
        
        matriculas = []
        for i in range(self.matricula_layout.count()):
            widget = self.matricula_layout.itemAt(i).widget().findChild(QLineEdit)
            print(f"Procesando widget en índice {i}: {widget}")
            if isinstance(widget, QLineEdit):  # Verificar que el widget sea un QLineEdit
                texto_matricula = widget.text().strip()
                if texto_matricula:  # Solo agregar si no está vacío
                    matriculas.append(texto_matricula)
                    db.insertar(
                        """insert into inmuebles (matricula_inmobiliaria, tipo_inmueble, direccion, barrio, municipio, departamento, cedula_catastral, modo_adquicision, limitaciones, longitud, latitud, avaluo_id, doc_propiedad, propietario, id_propietario) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id_inmueble """,(texto_matricula, self.inmuebles[texto_matricula]["tipo_inmueble"], self.inmuebles[texto_matricula]["direccion"], self.inmuebles[texto_matricula]["barrio"], self.inmuebles[texto_matricula]["municipio"], self.inmuebles[texto_matricula]["departamento"], self.inmuebles[texto_matricula]["cedula_catastral"], self.inmuebles[texto_matricula]["modo_adquisicion"], self.inmuebles[texto_matricula]["limitaciones"], self.inmuebles[texto_matricula]["longitud"], self.inmuebles[texto_matricula]["latitud"], id_avaluo, self.inmuebles[texto_matricula]["doc_propiedad"], self.inmuebles[texto_matricula]["propietario"], self.inmuebles[texto_matricula]["id_propietario"]))
                    
                    print(f"Matrícula agregada: {texto_matricula}")

        print(f"Números de matrícula obtenidos: {matriculas}")

        # Guardar los datos del inmueble y las matrículas en la base de datos
        consulta_inmueble = """
        INSERT INTO "Inmuebles" (direccion, tipo_inmueble, barrio, municipio, departamento, cedula_catastral, modo_adquisicion, limitaciones, latitud, longitud, doc_propiedad)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_inmueble
        """
        #id_inmueble = db.insertar(consulta_inmueble, tuple(inmueble_data.values()))
        #print(f"Inmueble guardado con ID: {id_inmueble}")

        # Guardar las matrículas asociadas al inmueble
        consulta_matricula = """
        INSERT INTO "Matriculas" (id_inmueble, numero_matricula)
        VALUES (%s, %s)
        """
        """ for matricula in matriculas:
            db.insertar(consulta_matricula, (id_inmueble, matricula))
        print("Matrículas guardadas correctamente.") """
        
        db.cerrar_conexion()
        
    def guardar_informacion_inmueble(self, matricula):
        # Obtener datos del inmueble
        inmueble_data = {
            "tipo_inmueble": self.tipo_inmueble.currentText(),
            "direccion": self.direccion_inmueble.text().strip(),            
            "barrio": self.barrio_inmueble.text().strip(),
            "municipio": self.municipio_inmueble.text().strip(),
            "departamento": self.departamento_inmueble.text().strip(),
            "cedula_catastral": self.cedula_catastral.text().strip(),
            "modo_adquisicion": self.modo_adquisicion.currentText(),
            "limitaciones": self.limitaciones.toPlainText().strip(),
            "longitud": self.longitud.text().strip(),
            "latitud": self.latitud.text().strip(),
            "avaluo_id": self.id_avaluo,
            "doc_propiedad": self.doc_propiedad.toPlainText().strip(),
            "propietario": self.propietario.text().strip(),
            "id_propietario": self.id_propietario.text().strip()
        }     
        
        
        if matricula == "" or matricula is None:
            """
            Muestra un cuadro de advertencia con un color personalizado y centrado.
            """
            # Crear el cuadro de mensaje
            QMessageBox.warning(
                self,  # El widget padre (puede ser 'self' si estás dentro de una clase que hereda de QWidget)
                "Advertencia",  # Título de la ventana
                "Agrega una matrícula inmobiliaria",  # Mensaje de advertencia
                QMessageBox.StandardButton.Ok  # Botón estándar
            )
            return
        
        else:      
            
            self.inmuebles[self.matricula_actual]=inmueble_data
              
            """ db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
            db.conectar() """
            
            # Aquí podrías guardar los datos en una base de datos o archivo
            query_insertar = """insert into inmuebles (matricula_inmobiliaria, tipo_inmueble, direccion, barrio, municipio, departamento, cedula_catastral, modo_adquicision, limitaciones, longitud, latitud, avaluo_id, doc_propiedad, propietario, id_propietario) values """,(matricula, inmueble_data["tipo_inmueble"], inmueble_data["direccion"], inmueble_data["barrio"], inmueble_data["municipio"], inmueble_data["departamento"], inmueble_data["cedula_catastral"], inmueble_data["modo_adquisicion"], inmueble_data["limitaciones"], inmueble_data["longitud"], inmueble_data["latitud"], inmueble_data["avaluo_id"], inmueble_data["doc_propiedad"], inmueble_data["propietario"], inmueble_data["id_propietario"])
            
            print("Información del inmueble guardada:", self.inmuebles)
        
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
        
        if self.matricula_actual in self.inmuebles and self.matricula_layout.count()>1:
            QMessageBox.warning(
                self, 
                "Advertencia", 
                f"La matrícula '{self.matricula_actual}' ya existe en el diccionario.", 
                QMessageBox.StandardButton.Ok
            )
            return
        
        if self.matricula_actual:
            self.guardar_informacion_inmueble(self.matricula_actual)
        
        campo = QLineEdit()
        campo.setPlaceholderText("Ingrese número de matrícula")
        campo.setStyleSheet(self.group_style)
        campo.focusInEvent = lambda texto: self.actualizar_informacion_inmueble(campo.text()) 
        campo.textChanged.connect(lambda: self.actualizar_informacion_inmueble(campo.text()))
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
        
    def actualizar_informacion_inmueble(self, texto):
        # Actualizar el título del grupo_inmueble
        self.grupo_inmueble.setTitle(f"Datos del Inmueble segun MI-{texto}")
        self.matricula_actual = texto  # Actualizar la matrícula actual
        
        self.tipo_inmueble.setCurrentText(self.inmuebles[texto]["tipo_inmueble"] if texto in self.inmuebles else "")
        self.direccion_inmueble.setText(self.inmuebles[texto]["direccion"] if texto in self.inmuebles else "")
        self.barrio_inmueble.setText(self.inmuebles[texto]["barrio"] if texto in self.inmuebles else "")
        self.municipio_inmueble.setText(self.inmuebles[texto]["municipio"] if texto in self.inmuebles else "")
        self.departamento_inmueble.setText(self.inmuebles[texto]["departamento"] if texto in self.inmuebles else "")
        self.cedula_catastral.setText(self.inmuebles[texto]["cedula_catastral"] if texto in self.inmuebles else "")
        self.modo_adquisicion.setCurrentText(self.inmuebles[texto]["modo_adquisicion"] if texto in self.inmuebles else "")
        self.limitaciones.setPlainText(self.inmuebles[texto]["limitaciones"] if texto in self.inmuebles else "")
        self.longitud.setText(self.inmuebles[texto]["longitud"] if texto in self.inmuebles else "")
        self.latitud.setText(self.inmuebles[texto]["latitud"] if texto in self.inmuebles else "")
        self.doc_propiedad.setPlainText(self.inmuebles[texto]["doc_propiedad"] if texto in self.inmuebles else "")
        self.propietario.setText(self.inmuebles[texto]["propietario"] if texto in self.inmuebles else "")
        self.id_propietario.setText(self.inmuebles[texto]["id_propietario"] if texto in self.inmuebles else "")
    
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

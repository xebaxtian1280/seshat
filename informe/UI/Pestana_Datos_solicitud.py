from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QLineEdit, QTextEdit, QComboBox,
    QDateEdit, QPushButton, QLabel, QTabWidget, QScrollArea, QMessageBox, QInputDialog
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from Estilos import Estilos
from DB import DB
import webview

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
        if id_avaluo == "":
            btn_agregar_matricula.clicked.connect(self.agregar_campo_matricula)
        else:
            btn_agregar_matricula.clicked.connect(self.agregar_matricula_nueva)
        btn_agregar_matricula.setStyleSheet(self.group_style)
        
        btn_radicar_solicitud = QPushButton("Radicar Solicitud")
        btn_radicar_solicitud.clicked.connect(self.radicar_solicitud)
        btn_radicar_solicitud.setStyleSheet(self.group_style)

        juridico_layout.addRow(grupo_documentos)
        juridico_layout.addRow(self.btn_agregar_doc)
        
        if id_avaluo == "":
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
        
        self.latitud.textChanged.connect(self.actualizar_mapa)
        self.longitud.textChanged.connect(self.actualizar_mapa)
        
        self.doc_propiedad = QTextEdit()
        self.doc_propiedad.setPlainText("Copia simple de la Escritura Pública No. 4126 del 26 de Noviembre de 1997, otorgada en la Notaria 2 de Bucaramanga.")
        
        self.btn_guardar_inmueble = QPushButton("Guardar informacion del Inmueble")
        self.btn_agregar_doc.setStyleSheet(self.group_style)
        self.btn_guardar_inmueble.clicked.connect(lambda: self.guardar_informacion_inmueble(self.matricula_actual))

        # Campos jurídicos
        self.propietario = QLineEdit()
        self.id_propietario = QLineEdit()
        
        # Campos iniciales
        if id_avaluo == "":
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
                    
                self.cargar_inmuebles()
            
            else:
                print(f"No se encontraron datos para el avalúo con ID: {id_avaluo}")
                
            consulta_documentacion = """ select documento, id_documentacin from documentacion_aportada where "Avaluo_id" = %s""".replace("%s", str(id_avaluo))
            
            resultado_documentacion = db.consultar(consulta_documentacion)
            print(resultado_documentacion)
            if resultado_documentacion:
                for doc in resultado_documentacion:
                    self.agregar_campo_documento(doc)
            
            db.cerrar_conexion()
            
        except Exception as e:
            print(f"Error al cargar los datos de la solicitud: {e}")
            
    
    def radicar_solicitud(self):
        
        if self.matricula_actual not in self.inmuebles:
            self.guardar_informacion_inmueble(self.matricula_actual)
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

        
        # Recorrer los elementos de matricula_layout y obtener los textos de los QLineEdit
        
        matriculas = []
        for i in range(self.matricula_layout.count()):
            widget = self.matricula_layout.itemAt(i).widget().findChild(QLineEdit)
            
            if isinstance(widget, QLineEdit):  # Verificar que el widget sea un QLineEdit
                texto_matricula = widget.text().strip()
                if texto_matricula:  # Solo agregar si no está vacío
                    matriculas.append(texto_matricula)
                    db.insertar(
                        """insert into inmuebles (matricula_inmobiliaria, tipo_inmueble, direccion, barrio, municipio, departamento, cedula_catastral, modo_adquicision, limitaciones, longitud, latitud, avaluo_id, doc_propiedad, propietario, id_propietario) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id_inmueble """,(texto_matricula, self.inmuebles[texto_matricula]["tipo_inmueble"], self.inmuebles[texto_matricula]["direccion"], self.inmuebles[texto_matricula]["barrio"], self.inmuebles[texto_matricula]["municipio"], self.inmuebles[texto_matricula]["departamento"], self.inmuebles[texto_matricula]["cedula_catastral"], self.inmuebles[texto_matricula]["modo_adquisicion"], self.inmuebles[texto_matricula]["limitaciones"], self.inmuebles[texto_matricula]["longitud"], self.inmuebles[texto_matricula]["latitud"], id_avaluo, self.inmuebles[texto_matricula]["doc_propiedad"], self.inmuebles[texto_matricula]["propietario"], self.inmuebles[texto_matricula]["id_propietario"]))
                    

        # Lista para almacenar los textos de la documentación
        documentacion = []

        # Recorrer los widgets en el contenedor correspondiente
        for i in range(self.documentacion_layout.count()):
            widget = self.documentacion_layout.itemAt(i).widget().findChild(QLineEdit)
            
            if isinstance(widget, QLineEdit):  # Verificar que el widget sea un QLineEdit
                texto_documento = widget.text().strip()
                if texto_matricula:  # Solo agregar si no está vacío
                    matriculas.append(texto_matricula)
                    try:
                        db.insertar(
                            """
                            INSERT INTO documentacion_aportada ("Avaluo_id", documento)
                            VALUES (%s, %s) returning id_documentacin
                            """,
                            (id_avaluo, texto_documento)
                        )
                        print(f"Documento agregado: {texto_documento}")
                    except Exception as e:
                        print(f"Error al insertar el documento '{texto_documento}': {e}")
        
        print(f"Números de matrícula obtenidos: {matriculas}")

        
        db.cerrar_conexion()  
        
    def guardar_informacion_inmueble(self, matricula):
        
        if self.matricula_actual in self.inmuebles:
            QMessageBox.warning(
                self, 
                "Advertencia", 
                f"La matrícula '{self.matricula_actual}' ya existe en el diccionario.", 
                QMessageBox.StandardButton.Ok
            )
            return "Antes de agregar otra matricula, agrega una matricula nueva que no se encuentre repetida"
        
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
            return ""
        
        else:      
            
            self.inmuebles[self.matricula_actual]=inmueble_data
            
            print("Información del inmueble guardada:", self.inmuebles)
            return ""
        
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
                
                // Agregar marcador inicial
                var marker = L.marker([{lat}, {lon}], {{draggable: true}}).addTo(map);

                // Evento para capturar clics en el mapa
                map.on('click', function(e) {{
                    var coords = e.latlng; // Obtener las coordenadas del clic
                    marker.setLatLng(coords); // Mover el marcador al nuevo punto

                    // Enviar las coordenadas al backend
                    pywebview.api.enviar_coordenadas(coords.lat, coords.lng);
                }});
            </script>
        </body>
        </html>
        '''
        
        """ # Crear la API y exponerla al frontend
        api = API()
        self.webview.create_window('Mapa', html=mapa_html, js_api=api)
        self.webview.start() """
        
        self.web_view.setHtml(mapa_html)
        
    def agregar_campo_matricula(self):
        resultado = ""
        
        if self.matricula_actual and self.matricula_layout.count()>len(self.inmuebles):
            resultado = self.guardar_informacion_inmueble(self.matricula_actual)
            
        if resultado == "" or self.matricula_layout.count()==0 or self.matricula_actual == len(self.inmuebles):
            campo = QLineEdit()
            campo.setPlaceholderText("Ingrese número de matrícula")
            campo.setStyleSheet(self.group_style)
            campo.focusInEvent = lambda : self.actualizar_informacion_inmueble(campo) 
            campo.textChanged.connect(lambda: self.actualizar_informacion_inmueble(campo))
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
        
        else:
            QMessageBox.warning(
                self, 
                "Advertencia", 
                resultado, 
                QMessageBox.StandardButton.Ok
            )
    
    def agregar_matricula_nueva(self):
        
        if self.matricula_actual:
            
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
            print(self.inmuebles[self.matricula_actual])
            print(inmueble_data)
            
            auxiliar_comparar = False
            
            for clave, valor in inmueble_data.items():
                valor_actual = self.inmuebles[self.matricula_actual].get(clave)
                print(f"Comparando clave: {clave}, valor actual: {valor_actual}, nuevo valor: {valor}, resultado: {str(valor_actual) != str(valor)}")
                if str(valor_actual) != str(valor):
                    auxiliar_comparar = True 
                    print("Se detectó un cambio en la clave:", clave)                   
            print(auxiliar_comparar)
            if auxiliar_comparar:
                ## Crear el cuadro de diálogo
                dialogo = QMessageBox(self)
                dialogo.setWindowTitle(f"Guardar datos del Inmueble {self.matricula_actual}")
                dialogo.setText(f"Se han realizado cambios en la matrícula {self.matricula_actual}. ¿Qué desea hacer?")

                # Personalizar los botones
                btn_aceptar = dialogo.addButton("Guardar Cambios", QMessageBox.ButtonRole.AcceptRole)
                btn_descartar = dialogo.addButton("Descartar cambios", QMessageBox.ButtonRole.RejectRole)

                # Mostrar el cuadro de diálogo y manejar la respuesta
                dialogo.exec()
                if dialogo.clickedButton() == btn_aceptar:
                    self.actualizar_inmueble(self.matricula_actual)
                else:
                    print("Cambios descartados.")
        
        # Crear el cuadro de diálogo
        dialogo = QInputDialog(self)    
        dialogo.setWindowTitle("Agregar Matrícula")
        dialogo.setLabelText("Ingrese el número de matrícula:")
        dialogo.setInputMode(QInputDialog.InputMode.TextInput)
        dialogo.setOkButtonText("Aceptar")
        dialogo.setCancelButtonText("Cancelar")
        
        # Mostrar el cuadro de diálogo y capturar el resultado
        if dialogo.exec() == QInputDialog.DialogCode.Accepted:
            texto_matricula = dialogo.textValue().strip()  # Capturar el texto ingresado
            
            if texto_matricula:  # Verificar que no esté vacío
                # Crear el QLineEdit y asignar el texto ingresado
                
                 
                
                campo = QPushButton()
                campo.setText(texto_matricula)                
                campo.setStyleSheet(self.group_style)                
                
                campo.clicked.connect(lambda : self.actualizar_informacion_inmueble(campo))
                btn_eliminar = QPushButton("×")
                btn_eliminar.setObjectName("botonEliminar")
                btn_eliminar.setStyleSheet(self.group_style)
                self.actualizar_informacion_inmueble(campo)
                
                # Contenedor para el campo y el botón
                campo_container = QWidget()
                layout_container = QHBoxLayout(campo_container)
                layout_container.addWidget(campo)
                layout_container.addWidget(btn_eliminar)
                layout_container.setContentsMargins(0, 0, 0, 0)
                
                # Conectar el botón de eliminar
                btn_eliminar.clicked.connect(lambda: self.eliminar_campo_matricula(campo_container))
                
                self.matricula_layout.addWidget(campo_container)
                
                self.btn_guardar_inmueble.setText("Actualizar informacion del Inmueble")
                self.btn_guardar_inmueble.clicked.disconnect()  # Desconectar señales anteriores
                self.btn_guardar_inmueble.clicked.connect(lambda: self.actualizar_inmueble(texto_matricula))
                self.matricula_actual = texto_matricula
                
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
                
                db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
                db.conectar()
                
                query = """insert into inmuebles (matricula_inmobiliaria, tipo_inmueble, direccion, barrio, municipio, departamento, cedula_catastral, modo_adquicision, limitaciones, longitud, latitud, avaluo_id, doc_propiedad, propietario, id_propietario) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id_inmueble """
                    
                db.insertar(query, (texto_matricula, inmueble_data["tipo_inmueble"], inmueble_data["direccion"], inmueble_data["barrio"], inmueble_data["municipio"], inmueble_data["departamento"], inmueble_data["cedula_catastral"], inmueble_data["modo_adquisicion"], inmueble_data["limitaciones"], 4.6097, -74.0817, self.id_avaluo, inmueble_data["doc_propiedad"], inmueble_data["propietario"], inmueble_data["id_propietario"]))
                
                db.cerrar_conexion()

            else:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "El número de matrícula no puede estar vacío.",
                    QMessageBox.StandardButton.Ok
                )

            
        
        else:
            QMessageBox.warning(
                self, 
                "Advertencia", 
                "resultado cancelado", 
                QMessageBox.StandardButton.Ok
            )

    def eliminar_campo_matricula(self, contenedor_a_eliminar):
        
        """
        Extrae el texto de la matrícula inmobiliaria desde el contenedor,
        elimina este campo del diccionario self.inmuebles y muestra una alerta
        para confirmar si se desea eliminar la matrícula de la base de datos.
        """
        # Extraer el texto de la matrícula inmobiliaria
        matricula = None
        for widget in contenedor_a_eliminar.children():
            if isinstance(widget, QLineEdit):  # Suponiendo que el QLineEdit contiene la matrícula
                matricula = widget.text().strip()
                break

        if not matricula:
            QMessageBox.warning(
                self,
                "Advertencia",
                "No se pudo obtener la matrícula inmobiliaria del contenedor.",
                QMessageBox.StandardButton.Ok
            )
            return

        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar la matrícula '{matricula}' de la base de datos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                # Eliminar la matrícula del diccionario
                if matricula in self.inmuebles:
                    del self.inmuebles[matricula]
                    print(f"Matrícula '{matricula}' eliminada del diccionario.")

                # Consulta SQL para eliminar la matrícula de la base de datos
                
                db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
                db.conectar()
                
                query = "DELETE FROM inmuebles WHERE matricula_inmobiliaria = %s AND avaluo_id = %s"
                db.eliminar(query, (matricula, self.id_avaluo))
                print(f"Matrícula '{matricula}' eliminada de la base de datos.")

                # Remover el widget contenedor del layout
        
                self.matricula_layout.removeWidget(contenedor_a_eliminar)
                
                # Eliminar los widgets hijos
                contenedor_a_eliminar.deleteLater()

                QMessageBox.information(
                    self,
                    "Eliminación exitosa",
                    f"La matrícula '{matricula}' ha sido eliminada correctamente.",
                    QMessageBox.StandardButton.Ok
                )
                db.cerrar_conexion()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Ocurrió un error al eliminar la matrícula: {e}",
                    QMessageBox.StandardButton.Ok
                )
        else:
            print(f"Eliminación de la matrícula '{matricula}' cancelada.")
        
    def actualizar_informacion_inmueble(self, campo):
        
        texto = campo.text()
        
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
        self.longitud.setText(str(self.inmuebles[texto]["longitud"]) if texto in self.inmuebles else "")
        self.latitud.setText(str(self.inmuebles[texto]["latitud"]) if texto in self.inmuebles else "")
        self.doc_propiedad.setPlainText(self.inmuebles[texto]["doc_propiedad"] if texto in self.inmuebles else "")
        self.propietario.setText(self.inmuebles[texto]["propietario"] if texto in self.inmuebles else "")
        self.id_propietario.setText(str(self.inmuebles[texto]["id_propietario"]) if texto in self.inmuebles else "")
        
        if self.matricula_actual in self.inmuebles:             
             
             
            self.btn_guardar_inmueble.setText("Actualizar informacion del Inmueble")
            self.btn_guardar_inmueble.clicked.disconnect()  # Desconectar señales anteriores
            self.btn_guardar_inmueble.clicked.connect(lambda: self.actualizar_inmueble(self.matricula_actual))
            
        else:
            self.btn_guardar_inmueble.setText("Guardar informacion del Inmueble")
            self.btn_guardar_inmueble.clicked.disconnect()  # Desconectar señales anteriores
            self.btn_guardar_inmueble.clicked.connect(lambda: self.guardar_informacion_inmueble(self.matricula_actual))
        
    def actualizar_inmueble(self, matricula):
        """
        Actualiza la información de un inmueble en el diccionario self.inmuebles.
        Si la matrícula no existe, se agrega como un nuevo inmueble.
    
        :param matricula: La matrícula inmobiliaria (clave única).
        :param nueva_informacion: Diccionario con los nuevos datos del inmueble.
        """
        
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
        
        if not isinstance(inmueble_data, dict):
            print("Error: La nueva información debe ser un diccionario.")
            return
    
        if matricula in self.inmuebles:
            
            # Confirmar actualización
            respuesta = QMessageBox.question(
                self,
                "Confirmar actualizacion",
                f"¿Está seguro de que desea actualizar la matrícula '{matricula}' de la base de datos?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:            
                
                try:
                
                    self.inmuebles[matricula].update(inmueble_data)
                    
                    db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
                    db.conectar()
                    
                    query = """ UPDATE inmuebles SET tipo_inmueble=%s, direccion=%s, barrio=%s, municipio=%s, departamento=%s, cedula_catastral=%s, modo_adquicision=%s, limitaciones=%s, longitud=%s, latitud=%s, doc_propiedad=%s, propietario=%s, id_propietario=%s WHERE matricula_inmobiliaria=%s AND avaluo_id=%s """
                    
                    db.actualizar(query, (inmueble_data["tipo_inmueble"], inmueble_data["direccion"], inmueble_data["barrio"], inmueble_data["municipio"], inmueble_data["departamento"], inmueble_data["cedula_catastral"], inmueble_data["modo_adquisicion"], inmueble_data["limitaciones"], inmueble_data["longitud"], inmueble_data["latitud"], inmueble_data["doc_propiedad"], inmueble_data["propietario"], inmueble_data["id_propietario"], matricula, self.id_avaluo))
                    
                    db.cerrar_conexion()
                    QMessageBox.information(
                        self,
                        "Actualizacion exitosa",
                        f"La matrícula '{matricula}' ha sido actualizada correctamente.",
                        QMessageBox.StandardButton.Ok
                    )
                    db.cerrar_conexion()
                
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Ocurrió un error al eliminar la matrícula: {e}",
                        QMessageBox.StandardButton.Ok
                    )
                
                
        else:
            print(f"Agregando nuevo inmueble con matrícula: {matricula}")
            self.inmuebles[matricula] = inmueble_data
    
        print(f"Inmueble actualizado/agregado: {self.inmuebles[matricula]}")
    
    def cargar_inmuebles(self):
        """
        Carga todos los registros de la tabla 'inmuebles' desde la base de datos
        y los agrega al diccionario self.inmuebles.
        """
                    
        query = """ SELECT * FROM inmuebles WHERE avaluo_id = x; """.replace("x", str(self.id_avaluo))
        print(f"Cargando inmuebles con la consulta: {query}")
        
        try:
            # Ejecutar la consulta para obtener todos los registros de la tabla inmuebles
            db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
            db.conectar()            
            
            registros = db.consultar(query)
            
            print(f"Registros obtenidos: {registros}")
    
            # Limpiar el diccionario self.inmuebles antes de cargar nuevos datos
            self.inmuebles = {}
    
            # Recorrer los registros y agregarlos al diccionario
            for registro in registros:
                matricula = registro[12]  # Suponiendo que esta es la clave única
                print(f"Cargando inmueble con matrícula: {matricula}")
                self.inmuebles[matricula] = {
                    "tipo_inmueble": registro[1],
                    "direccion": registro[2],
                    "barrio": registro[3],
                    "municipio": registro[4],
                    "departamento": registro[5],
                    "cedula_catastral": registro[6],
                    "modo_adquisicion": registro[7],
                    "limitaciones": registro[8],
                    "longitud": registro[9],
                    "latitud": registro[10],
                    "avaluo_id": registro[11],
                    "doc_propiedad": registro[13],
                    "propietario": registro[14],
                    "id_propietario": registro[15]
                }                 
                
                # Crear el campo de texto para la matrícula
                campo = QPushButton()
                campo.setText(matricula)
                campo.setStyleSheet(self.group_style)
                
                # Conectar las señales usando una función auxiliar para capturar el valor actual
                campo.clicked.connect(self.crear_focus_evento(campo))
                self.actualizar_informacion_inmueble(campo)
                # Crear el botón de eliminar
                btn_eliminar = QPushButton("×")
                btn_eliminar.setObjectName("botonEliminar")
                btn_eliminar.setStyleSheet(self.group_style)
                
                
                # Contenedor para el campo y el botón
                campo_container = QWidget()
                layout_container = QHBoxLayout(campo_container)
                layout_container.addWidget(campo)
                layout_container.addWidget(btn_eliminar)
                layout_container.setContentsMargins(0, 0, 0, 0)    
                
                btn_eliminar.clicked.connect(self.crear_eliminar_evento(campo_container))          
                
                self.matricula_layout.addWidget(campo_container)
            db.cerrar_conexion()
            print(f"Inmuebles cargados correctamente en el diccionario self.inmuebles: {self.inmuebles}")
        except Exception as e:
            print(f"Error al cargar los inmuebles desde la base de datos: {e}")
    
    def crear_focus_evento(self, campo):
        """
        Crea un evento para manejar el focusInEvent de un campo.
        """
        def evento_focus_in(texto):
            self.actualizar_informacion_inmueble(campo)
        return evento_focus_in
    
    def crear_text_changed_evento(self, campo):
        """
        Crea un evento para manejar el textChanged de un campo.
        """
        def evento_text_changed():
            self.actualizar_informacion_inmueble(campo)
        return evento_text_changed
    
    def crear_eliminar_evento(self, campo_container):
        """
        Crea un evento para manejar el clic en el botón de eliminar.
        """
        def evento_eliminar():
            self.eliminar_campo_matricula(campo_container)
        return evento_eliminar
    
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

    def agregar_campo_documento(self, documento = None):
        campo = QLineEdit()
        print(f"agregar campo segun {self.id_avaluo}")
        if documento:
            print( documento[0])
            campo.setText(documento[0])
            campo.setProperty("id_documento", documento[1])
            
        elif self.id_avaluo is None:            
            campo.setPlaceholderText("Nombre del documento")
        
        else:
            # Crear el cuadro de diálogo
            dialogo = QInputDialog(self)    
            dialogo.setWindowTitle("Agregar Documento")
            dialogo.setLabelText("Ingrese los datos del documento:")
            dialogo.setInputMode(QInputDialog.InputMode.TextInput)
            dialogo.setOkButtonText("Aceptar")
            dialogo.setCancelButtonText("Cancelar")
            
            # Mostrar el cuadro de diálogo y capturar el resultado
            if dialogo.exec() == QInputDialog.DialogCode.Accepted:
                texto_documento = dialogo.textValue().strip()  # Capturar el texto ingresado
                
                if texto_documento:  # Verificar que no esté vacío
                    
                    campo.setText(texto_documento)
                    db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
                    db.conectar()
                    
                    resultado_documento = db.insertar(""" insert into documentacion_aportada ("Avaluo_id", documento) values (%s, %s) returning id_documentacin """, (self.id_avaluo, texto_documento))
                    
                    campo.setProperty("id_documento", resultado_documento)
            
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
        btn_eliminar.clicked.connect(lambda: self.eliminar_documento(campo_container))
        self.documentacion_layout.addWidget(campo_container)

    def eliminar_documento(self, contenedor):
        """
        Elimina el contenedor de documentos y su registro asociado en la base de datos.
        
        :param contenedor: El contenedor (QWidget) que contiene el campo del documento y el botón de eliminar.
        """
        try:
            # Obtener el campo QLineEdit dentro del contenedor
            campo = contenedor.findChild(QLineEdit)
            # Confirmar eliminación
            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Está seguro de que desea eliminar la el documento '{campo.text()}' de la base de datos?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:
                
                db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
                db.conectar()
                
                if campo:
                    # Obtener el id_documento de la propiedad del campo
                    id_documento = campo.property("id_documento")
                    
                    print(f"Eliminando documento con id_documento: {id_documento}")
                    if id_documento:
                        # Conectar a la base de datos y eliminar el registro
                        db.eliminar("DELETE FROM documentacion_aportada WHERE id_documentacin = %s", (id_documento,))
                        
                        print(f"Documento con id_documento {id_documento} eliminado de la base de datos.")
                    else:
                        print("Advertencia: No se encontró un id_documento asociado al campo.")
                
                # Eliminar el contenedor del layout
                layout = self.documentacion_layout
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget() == contenedor:
                        layout.takeAt(i)
                        contenedor.deleteLater()
                        print("Contenedor eliminado de la interfaz.")
                        break
                db.cerrar_conexion()
        except Exception as e:
            print(f"Error al eliminar el contenedor o el registro de la base de datos: {e}")
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QLineEdit, QTextEdit, QComboBox,
    QDateEdit, QPushButton, QLabel, QTabWidget, QScrollArea, QMessageBox, QInputDialog
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QDate, QObject, pyqtSlot, Qt, QTimer
from PyQt6.QtGui import QIcon
from Estilos import Estilos
from DB import DB


import enchant
from PyQt6.QtGui import QTextCharFormat, QColor

import webview

class Backend(QObject):
    def __init__(self,ventana, parent=None):
        super().__init__(parent)
        self.ventana = ventana

    @pyqtSlot(float, float)
    def update_lat_lon(self, lat, lon):
        """
        Método expuesto al frontend para capturar las coordenadas.
        """
        print(f"Latitud: {lat}, Longitud: {lon}")
        self.ventana.latitud.setText(str(lat))
        self.ventana.longitud.setText(str(lon))

class PestanaDatosSolicitud(QWidget):
    def __init__(self,  tab_panel: QTabWidget, id_avaluo=None):
        super().__init__()

        
        self.tab_panel = tab_panel
        self.id_avaluo = id_avaluo
        self.group_style = Estilos.cargar_estilos(self, "styles.css")
        self.basededatos = "seshat"
        self.inmuebles = {}  # Lista para almacenar los inmuebles asociados a la matricula
        self.matricula_actual = ""  # Variable para almacenar la matrícula actual

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
        self.municipio_inmueble = QComboBox()
        self.cargar_municipios()
        self.municipio_inmueble.currentIndexChanged.connect(self.actualizar_departamento)
        self.departamento_inmueble = QComboBox()
        self.zona = QComboBox()
        self.zona.addItems(["","Urbano", "Rural", "Expancion Urbana"])
        self.cargar_departamentos()
        self.nombre_perito = QComboBox()
        self.cargar_peritos() 
        self.nombre_revisor = QComboBox()
        self.cargar_revisores()
        
        solicitud_layout.addRow("Cliente:", self.cliente)
        solicitud_layout.addRow("Documento de identificación:", self.doc_identidad)
        solicitud_layout.addRow("Destinatario del Avalúo:", self.destinatario)
        solicitud_layout.addRow("Fecha de la visita:", self.fecha_visita)
        solicitud_layout.addRow("Fecha del informe:", self.fecha_informe)
        solicitud_layout.addRow("Tipo de avalúo solicitado:", self.tipo_avaluo)
        solicitud_layout.addRow("Municipio:", self.municipio_inmueble)
        solicitud_layout.addRow("Departamento:", self.departamento_inmueble)
        solicitud_layout.addRow("Zona:", self.zona)
        solicitud_layout.addRow("Perito asignado:", self.nombre_perito)
        solicitud_layout.addRow("Revisor asignado:", self.nombre_revisor)
        
        
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
            btn_agregar_matricula.clicked.connect(lambda _: self.agregar_campo_matricula())
        else:
            btn_agregar_matricula.clicked.connect(self.agregar_matricula_nueva)
        btn_agregar_matricula.setStyleSheet(self.group_style)
        
        btn_radicar_solicitud = QPushButton("Radicar Solicitud")
        btn_radicar_solicitud.clicked.connect(self.radicar_solicitud)
        btn_radicar_solicitud.setStyleSheet(self.group_style)

        juridico_layout.addRow(grupo_documentos)
        juridico_layout.addRow(self.btn_agregar_doc)
        
        """ if id_avaluo == "":
            self.agregar_campo_matricula()    """
         
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
        
        self.cedula_catastral = QLineEdit()
        self.limitaciones = QTextEdit()
        
        #self.limitaciones.textChanged.connect(lambda : self.resaltar_errores(self.limitaciones))
        
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
        if id_avaluo == "":
            self.agregar_campo_documento()  # Primer campo por defecto
        right_layout.addRow(QLabel("Coordenadas:"))
        right_layout.addRow("Latitud:", self.latitud)
        right_layout.addRow("Longitud:", self.longitud)
        right_layout.addRow("Tipo de inmueble:", self.tipo_inmueble)
        right_layout.addRow("Dirección del inmueble:", self.direccion_inmueble)
        right_layout.addRow("Barrio / Vereda:", self.barrio_inmueble)
        
        right_layout.addRow("Cédula Catastral:", self.cedula_catastral)
        right_layout.addRow("Modo de adquisición:", self.modo_adquisicion)
        right_layout.addRow("Limitaciones y gravámenes:", self.limitaciones)
        
        right_layout.addRow(QLabel("Documento de Propiedad:"))
        right_layout.addWidget(self.doc_propiedad)
        right_layout.addRow("Propietario:", self.propietario)
        right_layout.addRow("ID Propietario:", self.id_propietario)
        right_layout.addWidget(self.btn_guardar_inmueble)
        #right_layout.addWidget(self.btn_agregar_doc)
        
        # Columna izquierda - Contenedor vertical
        right_column = QVBoxLayout()
        
        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column) 
                
        # Grupo para el mapa
        grupo_mapa = QGroupBox("Ubicación Geográfica")
        grupo_mapa.setStyleSheet(self.group_style)
        mapa_layout = QVBoxLayout(grupo_mapa)
        
        # Widget para el mapa
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(620)
        
        #Crea el Backend para la comunicación de las coodenadas
        self.backend = Backend(self)
        self.channel = QWebChannel()
        self.channel.registerObject("qtObject", self.backend)
        self.web_view.page().setWebChannel(self.channel)
        
        # Botón para actualizar mapa
        btn_actualizar = QPushButton("Zoom ubicacion actual")
        btn_actualizar.clicked.connect(self.actualizar_mapa)
        
        mapa_layout.addWidget(self.web_view)
        mapa_layout.addWidget(btn_actualizar)
        
        # Agregar el mapa debajo del grupo del inmueble
        main_layout.addWidget(grupo_mapa)
        
        # Agregar grupos a la columna izquierda
        right_column.addWidget(self.grupo_inmueble)
        right_column.addStretch()
        
        #Agregar pestaña al Panel con barra de desplazamiento
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self)
        scroll_area.mi_pestana = self
        self.tab_panel.addTab(scroll_area, "Datos de la Solicitud")
      
        
        if self.id_avaluo == "":
            self.actualizar_mapa()
        else:
            self.cargar_datos_solicitud(self.id_avaluo)

    def on_tab_changed(self, tab_panel, index):
            """
            Maneja el evento de cambio de pestaña en el QTabWidget.
            Si la pestaña activa es "Datos de la Solicitud", recarga los datos de la solicitud.

            :param tab_panel: El QTabWidget que contiene las pestañas.
            :param index: El índice de la pestaña actualmente activa.
            """
            print(f"Pestaña cambiada a índice: {index}, Título: {tab_panel.tabText(index)}")
            if tab_panel.tabText(index) == "Datos de la Solicitud":

                if self.id_avaluo != "":
                    self.actualizar_solicitud()
                    
    def actualizar_solicitud(self):
        # Obtener datos actualizados de la solicitud
        solicitud_data = {
            "cliente": self.cliente.text().strip(),
            "doc_identidad": self.doc_identidad.text().strip(),
            "destinatario": self.destinatario.text().strip(),
            "fecha_visita": self.fecha_visita.date().toString("yyyy-MM-dd"),
            "fecha_informe": self.fecha_informe.date().toString("yyyy-MM-dd"),
            "tipo_avaluo": self.tipo_avaluo.currentText(),
            "id_peritos": self.nombre_perito.currentData(role=Qt.ItemDataRole.UserRole),
            "id_revisor": self.nombre_revisor.currentData(role=Qt.ItemDataRole.UserRole),
            "zona": self.zona.currentText()
        }

        # Validar campos requeridos
        if not solicitud_data["cliente"] or not solicitud_data["doc_identidad"] or not solicitud_data["tipo_avaluo"]:
            QMessageBox.warning(self, "Campos incompletos", "Por favor complete todos los campos requeridos.")
            return

        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        db.conectar()

        # Actualizar la solicitud en la base de datos
        db.actualizar(
            """UPDATE "Avaluos" SET nombre_cliente=%s, id_cliente=%s, destinatario=%s, fecha_visita=%s, tipo_avaluo=%s, fecha_avaluo=%s, id_peritos=%s, id_revisor=%s, zona=%s WHERE "Avaluo_id"=%s""",
            (solicitud_data["cliente"], solicitud_data["doc_identidad"], solicitud_data["destinatario"], solicitud_data["fecha_visita"], solicitud_data["tipo_avaluo"], solicitud_data["fecha_informe"], solicitud_data["id_peritos"], solicitud_data["id_revisor"], solicitud_data["zona"], self.id_avaluo)
        )

        # Actualizar inmuebles asociados
        for i in range(self.matricula_layout.count()):
            widget = self.matricula_layout.itemAt(i).widget().findChild(QPushButton)
            if isinstance(widget, QPushButton):
                texto_matricula = widget.text().strip()
                id_matricula = widget.property("id_matricula")
                if id_matricula:
                    db.actualizar(
                        """UPDATE inmuebles SET tipo_inmueble=%s, direccion=%s, barrio=%s, municipio=%s, departamento=%s, cedula_catastral=%s, modo_adquicision=%s, limitaciones=%s, longitud=%s, latitud=%s, doc_propiedad=%s, propietario=%s, id_propietario=%s WHERE id_inmueble=%s """,
                        (self.inmuebles[texto_matricula]["tipo_inmueble"], self.inmuebles[texto_matricula]["direccion"], self.inmuebles[texto_matricula]["barrio"], self.inmuebles[texto_matricula]["municipio"], self.inmuebles[texto_matricula]["departamento"], self.inmuebles[texto_matricula]["cedula_catastral"], self.inmuebles[texto_matricula]["modo_adquisicion"], self.inmuebles[texto_matricula]["limitaciones"], self.inmuebles[texto_matricula]["longitud"], self.inmuebles[texto_matricula]["latitud"], self.inmuebles[texto_matricula]["doc_propiedad"], self.inmuebles[texto_matricula]["propietario"], self.inmuebles[texto_matricula]["id_propietario"], id_matricula)
                    )

        # Actualizar documentación aportada
        for i in range(self.documentacion_layout.count()):
            widget = self.documentacion_layout.itemAt(i).widget().findChild(QLineEdit)
            if isinstance(widget, QLineEdit):
                texto_documento = widget.text().strip()
                if texto_documento:
                    db.actualizar(
                        """UPDATE documentacion_aportada SET documento=%s WHERE \"Avaluo_id\"=%s AND documento=%s""",
                        (texto_documento, self.id_avaluo, texto_documento)
                    )

        db.cerrar_conexion()
        #QMessageBox.information(self, "Actualización", "La información ha sido actualizada correctamente.")
        self.mostrar_mensaje_temporal("¡Actualización exitosa!", 5000)

    def mostrar_mensaje_temporal(self,texto, milisegundos=5000):
        mensaje = QLabel(texto)
        mensaje.setStyleSheet("background: #e0ffe0; color: #333; border: 1px solid #8f8; padding: 8px;")
        mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mensaje.setGeometry(50, 50, 300, 40)  # Ajusta posición y tamaño según tu ventana
        mensaje.show()

        QTimer.singleShot(milisegundos, mensaje.deleteLater)

    def cargar_datos_solicitud(self, id_avaluo):
        """
        Carga los datos de la solicitud desde la base de datos utilizando el id_avaluo.

        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
            db.conectar()
            
            print(f"Cargando datos para el avalúo con ID: {self.id_avaluo}")
    
            # Consulta SQL para obtener los datos de la solicitud
            consulta = """
            SELECT 
                a.nombre_cliente, 
                a.id_cliente, 
                a.destinatario, 
                a.fecha_visita, 
                a.fecha_avaluo, 
                a.tipo_avaluo, 
                CONCAT(p.nombre, ' ', p.apellido) AS perito_nombre,
                p.id_peritos, 
                CONCAT(r.nombre, ' ', r.apellido) AS revisor_nombre,
                r.id_revisor,
                a.zona 
            FROM 
                "Avaluos" a
            LEFT JOIN 
                inmuebles i ON a."Avaluo_id" = i.avaluo_id
            LEFT JOIN 
                peritos p ON a.id_peritos = p.id_peritos
            LEFT JOIN 
                revisores r ON a.id_revisor = r.id_revisor
            WHERE 
                a."Avaluo_id" = 2;
            """.replace("2", str(id_avaluo))
            resultado = db.consultar(consulta)
            print(resultado)
            # Verificar si se encontraron datos
            if resultado:
                
                self.cliente.setText(resultado[0][0])  # Primer campo: cliente
                self.doc_identidad.setText(str(resultado[0][1]))  # Segundo campo: doc_identidad
                self.destinatario.setText(resultado[0][2])  # Tercer campo: destinatario
                self.fecha_visita.setDate(resultado[0][3])  # Cuarto campo: fecha_visita  
                self.fecha_informe.setDate(resultado[0][4])  # Quinto campo: fecha_informe

                index_zona = self.zona.findText(resultado[0][10])  # Undécimo campo: zona
                if index_zona != -1:
                    self.zona.setCurrentIndex(index_zona)
                
                index_tipo = self.tipo_avaluo.findText(resultado[0][5])  # Sexto campo: tipo_avaluo
                if index_tipo != -1:
                    self.tipo_avaluo.setCurrentIndex(index_tipo)
                
                index_perito = self.nombre_perito.findText(resultado[0][6])  # Séptimo campo: perito_nombre
                
                if index_perito != -1:
                    self.nombre_perito.setCurrentIndex(index_perito)
                
                index_revisor = self.nombre_revisor.findText(resultado[0][8])  # Noveno campo: revisor_nombre
                
                if index_revisor != -1:
                    self.nombre_revisor.setCurrentIndex(index_revisor)                
                
                self.cargar_inmuebles()
            
            else:
                print(f"No se encontraron datos para el avalúo con ID: {id_avaluo}")
                
            consulta_documentacion = """ select documento, id_documentacin from documentacion_aportada where "Avaluo_id" = %s""".replace("%s", str(id_avaluo))
            
            resultado_documentacion = db.consultar(consulta_documentacion)
            print(resultado_documentacion)
            if resultado_documentacion:
                for doc, id_documentacion in resultado_documentacion:
                    self.agregar_campo_documento(doc, id_documentacion)

            db.cerrar_conexion()
            
        except Exception as e:
            print(f"Error al cargar los datos de la solicitud: {e}")
            
    def cargar_peritos(self):
        """
        Consulta la tabla 'peritos' de la base de datos y agrega los nombres de los peritos a self.filtro_nombre_perito.
        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
            db.conectar()
    
            # Consulta SQL para obtener los nombres de los peritos
            consulta = """SELECT CONCAT(nombre, ' ', apellido) AS perito_nombre, id_peritos FROM peritos;"""            
            resultados = db.consultar(consulta)
    
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.nombre_perito.clear()
    
            # Agregar los nombres de los peritos al QComboBox
            self.nombre_perito.addItem("")
            
            for resultado in resultados:
                self.nombre_perito.addItem(resultado[0])  # resultado[0] contiene el nombre del perito
                indice = self.nombre_perito.count() - 1  # Obtener el índice del último elemento agregado
                self.nombre_perito.setItemData(indice, resultado[1], role=Qt.ItemDataRole.UserRole)  # resultado[1] es el id_revisor
            
            db.cerrar_conexion()
        except Exception as e:
            print(f"Error al cargar los peritos: {e}")        
    
    def cargar_revisores(self):
        """
        Consulta la tabla 'peritos' de la base de datos y agrega los nombres de los peritos a self.filtro_nombre_perito.
        """
        try:
            # Crear una instancia de la clase DB
            db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
            db.conectar()
    
            # Consulta SQL para obtener los nombres de los peritos
            consulta = "SELECT CONCAT(nombre, ' ', apellido) AS revisor_nombre, id_revisor FROM revisores;"            
            resultados = db.consultar(consulta)
    
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.nombre_revisor.clear()
            self.nombre_revisor.addItem("") 
            # Agregar los nombres de los peritos al QComboBox
            for resultado in resultados:
                self.nombre_revisor.addItem(resultado[0])  # resultado[0] contiene el nombre del perito
                indice = self.nombre_revisor.count() - 1  # Obtener el índice del último elemento agregado
                self.nombre_revisor.setItemData(indice, resultado[1], role=Qt.ItemDataRole.UserRole)  # resultado[1] es el id_revisor
            db.cerrar_conexion()
        except Exception as e:
            print(f"Error al cargar los peritos: {e}")
    
    def cargar_municipios(self):
        """
        Carga los municipios desde la base de datos y los agrega al QComboBox.
        """
        try:
            # Consulta para obtener los municipios
            db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
            db.conectar()
            query = "SELECT id, nombre, departamento_id FROM municipios ORDER BY nombre"
            resultados = db.consultar(query)  # Ejecutar la consulta en la base de datos
            
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.municipio_inmueble.clear()
            self.municipio_inmueble.addItem("")  # Agregar un elemento vacío al inicio
            
            # Agregar los municipios al QComboBox
            for resultado in resultados:
                self.municipio_inmueble.addItem(resultado[1])  # resultado[1] contiene el nombre del municipio
                indice = self.municipio_inmueble.count() - 1  # Obtener el índice del último elemento agregado
                self.municipio_inmueble.setItemData(indice, resultado[0], role=Qt.ItemDataRole.UserRole)  # resultado[0] es el id
                self.municipio_inmueble.setItemData(indice, resultado[2], role=Qt.ItemDataRole.UserRole + 1)  # resultado[2] es el código departamento
                
            db.cerrar_conexion()
        except Exception as e:
            print(f"Error al cargar los municipios: {e}")
 
    def cargar_departamentos(self):
        """
        Carga los municipios desde la base de datos y los agrega al QComboBox.
        """
        try:
            # Consulta para obtener los municipios
            db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
            db.conectar()
            query = "SELECT id, nombre FROM departamentos ORDER BY nombre"
            resultados = db.consultar(query)  # Ejecutar la consulta en la base de datos
            
            # Limpiar el QComboBox antes de agregar nuevos datos
            self.departamento_inmueble.clear()
            self.departamento_inmueble.addItem("")  # Agregar un elemento vacío al inicio
            
            # Agregar los municipios al QComboBox
            for resultado in resultados:
                
                self.departamento_inmueble.addItem(resultado[1])  # resultado[1] contiene el nombre del municipio
                indice = self.departamento_inmueble.count() - 1  # Obtener el índice del último elemento agregado
                self.departamento_inmueble.setItemData(indice, resultado[0], role=Qt.ItemDataRole.UserRole)  # resultado[0] es el id
                
            db.cerrar_conexion()
        except Exception as e:
            print(f"Error al cargar los municipios: {e}")
    
    def actualizar_departamento(self):
        
        """
        Recupera la propiedad asociada al índice 2 del municipio seleccionado
        y la asigna al QComboBox de departamentos.
        """
        # Recuperar la propiedad asociada al índice 2 (por ejemplo, el id del departamento)
        id_departamento = self.municipio_inmueble.currentData(role=Qt.ItemDataRole.UserRole + 1)
        indice = self.departamento_inmueble.findData(id_departamento, role=Qt.ItemDataRole.UserRole)
        print("ID Departamento recuperado:", id_departamento)
        if indice is not None:
            # Asignar el valor recuperado al QComboBox de departamentos
            self.departamento_inmueble.setCurrentIndex(indice)
        else:
            print("No se encontró un departamento asociado al municipio seleccionado.")
    
    def radicar_solicitud(self):
        
        from Pestana_seguimiento import PestanaSeguimiento

        if self.matricula_actual not in self.inmuebles:
            self.guardar_informacion_inmueble(self.matricula_actual)
        # Obtener datos de la solicitud
        solicitud_data = {
            "cliente": self.cliente.text().strip(),
            "doc_identidad": self.doc_identidad.text().strip(),
            "destinatario": self.destinatario.text().strip(),
            "fecha_visita": self.fecha_visita.date().toString("yyyy-MM-dd"),
            "fecha_informe": self.fecha_informe.date().toString("yyyy-MM-dd"),
            "tipo_avaluo": self.tipo_avaluo.currentText(),
            "id_peritos": self.nombre_perito.currentData(role=Qt.ItemDataRole.UserRole),
            "id_revisor": self.nombre_revisor.currentData(role=Qt.ItemDataRole.UserRole),
            "zona": self.zona.currentText()
        }
        
        # Validar campos requeridos
        if not solicitud_data["cliente"] or not solicitud_data["doc_identidad"] or not solicitud_data["tipo_avaluo"]:
            
            QMessageBox.warning(self, "Campos incompletos", "Por favor complete todos los campos requeridos.")
            return
        
        # Guardar los datos en una base de datos o archivo
        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        db.conectar()
        id_avaluo = db.insertar(
           """INSERT INTO "Avaluos" (nombre_cliente, id_cliente, destinatario, fecha_visita, tipo_avaluo, fecha_avaluo, id_peritos, id_revisor, zona) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning "Avaluo_id" """
            , (solicitud_data["cliente"], solicitud_data["doc_identidad"], solicitud_data["destinatario"], solicitud_data["fecha_visita"],solicitud_data["tipo_avaluo"], solicitud_data["fecha_informe"], solicitud_data["id_peritos"], solicitud_data["id_revisor"], solicitud_data["zona"]))

        
        # Recorrer los elementos de matricula_layout y obtener los textos de los QLineEdit
        
        matriculas = []
        for i in range(self.matricula_layout.count()):
            widget = self.matricula_layout.itemAt(i).widget().findChild(QPushButton)

            if isinstance(widget, QPushButton):  # Verificar que el widget sea un QPushButton
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
                if texto_documento:  # Solo agregar si no está vacío
                    matriculas.append(texto_documento)
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
        try:
            # Crear las pestañas con el id_avaluo            
            
            for index in range(self.tab_panel.count()):
                
                """ widget = self.tab_panel.widget(index)
                validacion=(self.tab_panel.tabText(index) == "PestanaDatosSolicitud") """
                print(f"Cerrando pestaña: {self.tab_panel.tabText(index)} con idex {index}")
                
                self.tab_panel.removeTab(0)
                
            
            # Crear las pestaña seguimiento
            self.pestana_seguimiento = PestanaSeguimiento(self.tab_panel)
                   
    
        except Exception as e:
            print(f"Error al agregar las pestañas: {e}")
        
        db.cerrar_conexion()  
        
    def guardar_informacion_inmueble(self, matricula):
        
        if self.matricula_actual in self.inmuebles:
            QMessageBox.warning(
                self, 
                "Advertencia", 
                f"La matrícula '{self.matricula_actual}' ya existe en el diccionario.", 
                QMessageBox.StandardButton.Ok
            )
            return "existe"
        
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
            return "Sin matrícula no se puede guardar la información del inmueble"
        
        else:      

            # Obtener datos del inmueble
            inmueble_data = {
            "tipo_inmueble": self.tipo_inmueble.currentText(),
            "direccion": self.direccion_inmueble.text().strip(),            
            "barrio": self.barrio_inmueble.text().strip(),
            "municipio": self.municipio_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
            "departamento": self.departamento_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
            "zona": self.zona.currentData(role=Qt.ItemDataRole.UserRole),
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
            
            self.inmuebles[self.matricula_actual]=inmueble_data
            
            print("Información del inmueble guardada:", self.inmuebles)
            return ""
        
    def actualizar_mapa(self):
        # Obtener coordenadas de los campos
        lat = self.latitud.text().strip() or "4.6097"  # Bogotá por defecto
        lon = self.longitud.text().strip() or "-74.0817"
        
       
        # Generar HTML con el mapa
        """
        Carga un mapa interactivo en el QWebEngineView.
        """
        mapa_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa</title>
            <style>
                #map {{
                    height: 100%;
                    width: 100%;
                }}
                html, body {{
                    margin: 0;
                    height: 100%;
                }}
            </style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.js"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/leaflet.css" />
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var backend;
                new QWebChannel(qt.webChannelTransport, function(channel) {{
                    backend = channel.objects.qtObject;
                }});

                var map = L.map('map').setView([{lat},{lon}], 16);
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    maxZoom: 19,
                    attribution: '© OpenStreetMap'
                }}).addTo(map);

                var marker = L.marker([{lat},{lon}]).addTo(map)
                    .bindPopup('Ubicación inmueble')
                    .openPopup();

                map.on('click', function(e) {{
                    var clickedLat = e.latlng.lat;
                    var clickedLon = e.latlng.lng;

                    marker.setLatLng(e.latlng)
                          .bindPopup('Nueva ubicación: ' + clickedLat.toFixed(5) + ', ' + clickedLon.toFixed(5))
                          .openPopup();

                    backend.update_lat_lon(clickedLat, clickedLon);
                }});
            </script>
        </body>
        </html>
        """
        
        
        # Agregar el QWebEngineView al contenedor en la interfaz
         
        self.web_view.setHtml(mapa_html)
    
    def recibir_coordenadas(self, lat, lon):
        """
        Método para recibir las coordenadas desde el frontend y actualizar los campos de latitud y longitud.
        """
        self.latitud.setText(f"{lat:.5f}")  # Actualizar el campo de latitud
        self.longitud.setText(f"{lon:.5f}")  # Actualizar el campo de longitud
        print(f"Coordenadas actualizadas: Latitud={lat}, Longitud={lon}")
        
    def agregar_campo_matricula(self):

        """ Agrega un campo de matricula, sin modificar la base de datos, para generar la radicacion inicial."""

        resultado = self.id_propietario.text().strip()

        if self.matricula_actual:
            
            self.comparar_cambios_inmuebles()
        
        # Crear el cuadro de diálogo
        dialogo = QInputDialog(self)    
        dialogo.setWindowTitle("Agregar Matrícula")
        dialogo.setLabelText("Ingrese el número de matrícula:")
        dialogo.setInputMode(QInputDialog.InputMode.TextInput)
        dialogo.setOkButtonText("Aceptar")
        dialogo.setCancelButtonText("Cancelar")
        
        # Mostrar el cuadro de diálogo y capturar el resultado
        if dialogo.exec() == QInputDialog.DialogCode.Accepted:
            self.matricula_actual = dialogo.textValue().strip()  # Capturar el texto ingresado
        
            if self.matricula_actual in self.inmuebles:
                QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    f"La matrícula '{self.matricula_actual}' ya existe en el diccionario.", 
                    QMessageBox.StandardButton.Ok
                )
                return
            print("resultado:", resultado!='')
            print("matricula actual:", self.matricula_actual)
            if resultado != '' and self.matricula_actual:
                campo = QPushButton()
                campo.setText(self.matricula_actual)
                campo.clicked.connect(lambda : self.actualizar_informacion_inmueble(campo))
                campo.setStyleSheet(self.group_style)
                """ campo.focusInEvent = lambda _: self.actualizar_informacion_inmueble(campo) 
                campo.textChanged.connect(lambda: self.actualizar_informacion_inmueble(campo)) """
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

                self.btn_guardar_inmueble.setText("Actualizar informacion del Inmueble")
                self.btn_guardar_inmueble.clicked.disconnect()  # Desconectar señales anteriores
                self.btn_guardar_inmueble.clicked.connect(lambda: self.actualizar_inmueble(self.matricula_actual))
                
                self.guardar_informacion_inmueble(self.matricula_actual)
            
            else:
                QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    "Primero ingrese los datos del inmueble para agregar una nueva matrícula.", 
                    QMessageBox.StandardButton.Ok
                )
                self.matricula_actual = ""
    
    def comparar_cambios_inmuebles(self):
        
        inmueble_data = {
                "tipo_inmueble": self.tipo_inmueble.currentText(),
                "direccion": self.direccion_inmueble.text().strip(),            
                "barrio": self.barrio_inmueble.text().strip(),
                "municipio": self.municipio_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
                "departamento": self.departamento_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
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
        
        auxiliar_comparar = False
        print("Comparando datos del inmueble para la matrícula:", self.matricula_actual)
        print("Datos actuales del inmueble:", self.inmuebles)
        for clave, valor in inmueble_data.items():
            valor_actual = self.inmuebles[self.matricula_actual][clave]
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
    
    def agregar_matricula_nueva(self):
        
        if self.matricula_actual:
            
            self.comparar_cambios_inmuebles()
        
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
                #self.actualizar_informacion_inmueble(campo)
                
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
                "municipio": self.municipio_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
                "departamento": self.departamento_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
                "zona": self.zona.currentData(role=Qt.ItemDataRole.UserRole),
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

                self.guardar_informacion_inmueble(self.matricula_actual)
                
                db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
                db.conectar()
                
                query = """insert into inmuebles (matricula_inmobiliaria, tipo_inmueble, direccion, barrio, municipio, departamento, cedula_catastral, modo_adquicision, limitaciones, longitud, latitud, avaluo_id, doc_propiedad, propietario, id_propietario, zona) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id_inmueble """
                    
                id_matricula = db.insertar(query, (texto_matricula, inmueble_data["tipo_inmueble"], inmueble_data["direccion"], inmueble_data["barrio"], inmueble_data["municipio"], inmueble_data["departamento"], inmueble_data["cedula_catastral"], inmueble_data["modo_adquisicion"], inmueble_data["limitaciones"], 4.6097, -74.0817, self.id_avaluo, inmueble_data["doc_propiedad"], inmueble_data["propietario"], inmueble_data["id_propietario"], inmueble_data["zona"]))
                campo_container.setProperty("id_matricula", id_matricula)
                
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
            if isinstance(widget, QPushButton):  # Suponiendo que el QLineEdit contiene la matrícula
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
            f"¿Está seguro de que desea eliminar la matrícula '{matricula}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                # Eliminar la matrícula del diccionario
                if matricula in self.inmuebles:
                    del self.inmuebles[matricula]

                # Consulta SQL para eliminar la matrícula de la base de datos
                
                if self.id_avaluo != "":
                    
                    # Crear una instancia de la clase DB
                    db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
                    db.conectar()
                    
                    query = "DELETE FROM inmuebles WHERE matricula_inmobiliaria = %s AND avaluo_id = %s"
                    db.eliminar(query, (matricula, self.id_avaluo))
                    print(f"Matrícula '{matricula}' eliminada de la base de datos.")
                    db.cerrar_conexion()                

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
        
        if self.matricula_actual:
            
            self.comparar_cambios_inmuebles()
        
        # Actualizar el título del grupo_inmueble
        self.grupo_inmueble.setTitle(f"Datos del Inmueble segun MI-{texto}")
        self.matricula_actual = texto  # Actualizar la matrícula actual
        
        self.tipo_inmueble.setCurrentText(self.inmuebles[texto]["tipo_inmueble"] if texto in self.inmuebles else "")
        self.direccion_inmueble.setText(self.inmuebles[texto]["direccion"] if texto in self.inmuebles else "")
        self.barrio_inmueble.setText(self.inmuebles[texto]["barrio"] if texto in self.inmuebles else "")
        
            # Seleccionar el municipio en el QComboBox        
        indice = self.municipio_inmueble.findData(self.inmuebles[texto]["municipio"], role=Qt.ItemDataRole.UserRole)
    
        if indice != -1:  # Si se encuentra un índice válido
            self.municipio_inmueble.setCurrentIndex(indice)
                
        # Seleccionar el departamento en el QComboBox   
             
        indice = self.departamento_inmueble.findData(self.inmuebles[texto]["departamento"], role=Qt.ItemDataRole.UserRole)
    
        if indice != -1:  # Si se encuentra un índice válido
            self.departamento_inmueble.setCurrentIndex(indice)

        
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
        self.actualizar_mapa()
        
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
                "municipio": self.municipio_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
                "departamento": self.departamento_inmueble.currentData(role=Qt.ItemDataRole.UserRole),
                "zona": self.zona.currentData(role=Qt.ItemDataRole.UserRole),
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

        if self.id_avaluo == "":
            # Confirmar actualización
            respuesta = QMessageBox.question(
                self,
                "Confirmar actualizacion",
                f"¿Está seguro de que desea actualizar la matrícula '{matricula}' actual?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if respuesta == QMessageBox.StandardButton.Yes:            
                
                try:
                
                    self.inmuebles[matricula].update(inmueble_data)
                    return
                
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Ocurrió un error al eliminar la matrícula: {e}",
                        QMessageBox.StandardButton.Ok
                    )

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

                    db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
                    db.conectar()
                    
                    query = """ UPDATE inmuebles SET tipo_inmueble=%s, direccion=%s, barrio=%s, municipio=%s, departamento=%s, cedula_catastral=%s, modo_adquicision=%s, limitaciones=%s, longitud=%s, latitud=%s, doc_propiedad=%s, propietario=%s, id_propietario=%s, zona=%s WHERE matricula_inmobiliaria=%s AND avaluo_id=%s """
                    
                    db.actualizar(query, (inmueble_data["tipo_inmueble"], inmueble_data["direccion"], inmueble_data["barrio"], inmueble_data["municipio"], inmueble_data["departamento"], inmueble_data["cedula_catastral"], inmueble_data["modo_adquisicion"], inmueble_data["limitaciones"], inmueble_data["longitud"], inmueble_data["latitud"], inmueble_data["doc_propiedad"], inmueble_data["propietario"], inmueble_data["id_propietario"], inmueble_data["zona"], matricula, self.id_avaluo))
                    
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
            db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
            db.conectar()            
            
            registros = db.consultar(query)
            
            print(f"Registros obtenidos: {registros}")
    
            # Limpiar el diccionario self.inmuebles antes de cargar nuevos datos
            self.inmuebles = {}
    
            # Recorrer los registros y agregarlos al diccionario
            for registro in registros:
                matricula = registro[1]  # Suponiendo que esta es la clave única
                print(f"Cargando inmueble con matrícula: {matricula}")
                self.inmuebles[matricula] = {
                    "tipo_inmueble": registro[2],
                    "direccion": registro[3],
                    "barrio": registro[4],
                    "municipio": registro[5],
                    "departamento": registro[6],
                    "cedula_catastral": registro[7],
                    "modo_adquisicion": registro[8],
                    "limitaciones": registro[9],
                    "longitud": registro[10],
                    "latitud": registro[11],
                    "avaluo_id": registro[12],
                    "doc_propiedad": registro[13],
                    "propietario": registro[14],
                    "id_propietario": registro[15]
                }
                print(f"Inmueble agregado al diccionario: {self.inmuebles[matricula]}")
                
                # Crear el campo de texto para la matrícula
                campo = QPushButton()
                campo.setText(str(matricula))
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
                campo_container.setProperty("id_matricula", registro[0])  # Almacenar el ID del inmueble en el contenedor
                layout_container = QHBoxLayout(campo_container)
                layout_container.addWidget(campo)
                layout_container.addWidget(btn_eliminar)
                layout_container.setContentsMargins(0, 0, 0, 0)    
                
                btn_eliminar.clicked.connect(self.crear_eliminar_evento(campo_container))          
                self.actualizar_mapa()
                self.matricula_layout.addWidget(campo_container)

            if not self.matricula_layout.count():
                self.actualizar_mapa()
            db.cerrar_conexion()
            print(f"Inmuebles cargados correctamente en el diccionario self.inmuebles: {self.inmuebles}")
        except Exception as e:
            print(f"Error al cargar los inmuebles desde la base de datos: {e}")
    
    def crear_focus_evento(self, campo):
        """
        Crea un evento para manejar el focusInEvent de un campo.
        """
        def evento_focus_in(texto):
            if self.matricula_actual and self.matricula_actual in self.inmuebles:
                self.comparar_cambios_inmuebles()
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
            
        elif self.id_avaluo == "":            
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
                    db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
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

            if self.id_avaluo == "":
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Está seguro de que desea eliminar la el documento '{campo.text()}' de la radicación?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if respuesta == QMessageBox.StandardButton.Yes:
                    # Eliminar el contenedor del layout
                    layout = self.documentacion_layout
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        if item and item.widget() == contenedor:
                            layout.takeAt(i)
                            contenedor.deleteLater()
                            print("Contenedor eliminado de la interfaz.")
                            break

            else:
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Está seguro de que desea eliminar la el documento '{campo.text()}' de la base de datos?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if respuesta == QMessageBox.StandardButton.Yes:

                    db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
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

    def resaltar_errores(self, text_edit, *args):
        dic = enchant.Dict("es_ES")  # Español
        texto = text_edit.toPlainText()
        cursor = text_edit.textCursor()
        cursor.select(cursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())  # Limpia formato previo

        palabras = texto.split()
        pos = 0
        for palabra in palabras:
            formato = QTextCharFormat()
            if not dic.check(palabra):
                formato.setUnderlineColor(QColor("red"))
                formato.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
            cursor.setPosition(pos)
            cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, len(palabra))
            cursor.setCharFormat(formato)
            pos += len(palabra) + 1  # +1 por el espacio
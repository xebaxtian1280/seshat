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
from Estilos import Estilos
from Funciones_imagenes import FuncionesImagenes
from DB import DB

class PestanaCaracteristicasSector(QWidget):
    def __init__(self, tab_panel: QTabWidget, id_avaluo = None, ventana_principal=None):
        super().__init__()
        
        self.basededatos = 'seshat'
        self.id_avaluo = id_avaluo
        self.pestana_activa = False  # Estado para rastrear si la pestaña está activa
        self.caracteristicas_sector_id = None  # ID del registro en la tabla caracteristicas_sector
        self.ventana_principal = ventana_principal
        self.path_trabajo = ""
        
        # Aquí va el contenido de la función crear_pestana_caracteristicas_sector
        self.group_style = Estilos.cargar_estilos(self, "styles.css")
        pestana = QWidget()
       
        # Crear scroll area para toda la pestaña
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        """ # Conectar eventos
        tab_panel.currentChanged.connect(lambda : self.on_tab_changed(tab_panel, tab_panel.currentIndex()))
        tab_panel.tabCloseRequested.connect(lambda : self.on_tab_changed(tab_panel, tab_panel.currentIndex())) """
        
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
        grupo_delimitacion.setStyleSheet(self.group_style)
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
        grupo_vias.setStyleSheet(self.group_style)
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
        grupo_amoblamiento.setStyleSheet(self.group_style)
        layout_amoblamiento = QVBoxLayout(grupo_amoblamiento)     
        
           
        self.amoblamiento_texto = QTextEdit()
        self.amoblamiento_texto.setFixedHeight(altura_textos)
        layout_amoblamiento.addWidget(self.amoblamiento_texto)
        
        # Nuevo Grupo: Servicios Públicos
        grupo_servicios = QGroupBox("Servicios Públicos")
        grupo_servicios.setStyleSheet(self.group_style)
        servicios_layout = QVBoxLayout(grupo_servicios)    
        
        # Crear widget para dos columnas
        column_widget = QWidget()
        column_layout = QHBoxLayout(column_widget)
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()

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
                self.col1.addWidget(cb)
            else:
                self.col2.addWidget(cb)

        column_layout.addLayout(self.col1)
        column_layout.addLayout(self.col2)
        servicios_layout.addWidget(column_widget)
        
        
        # left_column.addWidget(grupo_amoblamiento)
        # left_column.addStretch() 
        
        # Columna derecha
        right_column = QVBoxLayout()
        right_column.setSpacing(10)        
                
        # Grupo 3: Norma urbanística
        grupo_norma = QGroupBox("Norma urbanística")
        grupo_norma.setStyleSheet(self.group_style)
        layout_norma = QHBoxLayout(grupo_norma)
        
        # Instrumentos de OT
        self.instrumentos_ot = QTextEdit()
        self.instrumentos_ot.setPlainText(
            "Conforme al Plan de Ordenamiento Territorial, aprobado mediante acuerdo N° 0000 de 20xx "
            "Por el cual se adopta el Plan de Ordenamiento Territorial de segunda generación del Municipio de XXXXX."
        )
        self.instrumentos_ot.setFixedHeight(100)
        
        # Subgrupo Usos

        subgrupo_usos = QGroupBox("Usos")   
        subgrupo_usos.setStyleSheet(self.group_style)
        
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
        btn_agregar_imagen.setStyleSheet(self.group_style)

        # Conectar botón agregar imagenes usos
        btn_agregar_imagen.clicked.connect(lambda: FuncionesImagenes.agregar_imagen(self, self.imagenes_usos_layout, path_trabajo=self.path_trabajo+"/Norma"))
        
        form_usos.addRow(btn_agregar_imagen)
        form_usos.addRow(self.imagenes_usos_layout)
        
        """ # Listas dinámicas de usos
        categorias_usos = [
            ("Principales", self.crear_lista_usos),
            ("Complementarios", self.crear_lista_usos),
            ("Condicionado", self.crear_lista_usos),
            ("Permitido", self.crear_lista_usos),
            ("Prohibido", self.crear_lista_usos)
        ]
        
        for nombre, funcion in categorias_usos:
            form_usos.addRow(funcion(nombre))
             """
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
        btn_agregar_imagen_trat.clicked.connect(lambda : FuncionesImagenes.agregar_imagen(self, self.imagenes_tratamientos_layout, path_trabajo=self.path_trabajo+"/Norma"))
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
        pestana.mi_pestana = self
        
        tab_panel.addTab(pestana, "Características del Sector")

        self.cargar_datos_sector(self.id_avaluo)

        

    def guardar_datos(self):
        try:

            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()

            valores_checkbox = {cb.text(): cb.isChecked() for cb in self.col1.parentWidget().findChildren(QCheckBox) + self.col2.parentWidget().findChildren(QCheckBox)}

            if self.caracteristicas_sector_id:
                
                query_caracteristicas = """UPDATE caracteristicas_sector
                SET
                    transporte = %s,
                    amoblamiento_urbano = %s,
                    agua = %s,
                    gas = %s,
                    telefonia = %s,
                    recoleccion_basuras = %s,
                    alcantarillado = %s,
                    energia = %s,
                    contador_agua = %s,
                    contador_energia = %s,
                    contador_gas = %s,
                    descripcion_tratamiento = %s,
                    descripcion_usos = %s,
                    delimitacion_norte = %s,
                    delimitacion_sur = %s,
                    delimitacion_oriente = %s,
                    delimitacion_occidente = %s,
                    via_principal = %s,
                    via_secundaria = %s
                WHERE id_avaluo = %s;"""

                db.actualizar(query_caracteristicas, (
                    self.transporte_texto.toPlainText(), self.amoblamiento_texto.toPlainText(), valores_checkbox["Acueducto"], valores_checkbox["Gas Natural"], valores_checkbox["Telefonía Fija"], valores_checkbox["Recolección de Basuras"], valores_checkbox["Alcantarillado"], valores_checkbox["Energía Eléctrica"], valores_checkbox["Contador de Agua"], valores_checkbox["Contador de Energia"], valores_checkbox["Contador de Gas"], self.descripcion_tratamientos.toPlainText(), self.descripcion_usos.toPlainText(), self.norte.text(), self.sur.text(), self.oriente.text(), self.occidente.text(), self.vias_principales_texto.toPlainText(), self.vias_secundarias_texto.toPlainText(), self.id_avaluo
                ))
                id_caracteristicas = self.caracteristicas_sector_id
            else:
                
                query_caracteristicas = """
                INSERT INTO caracteristicas_sector (
                id_avaluo, transporte, amoblamiento_urbano, agua, gas, telefonia, recoleccion_basuras,
                alcantarillado, energia, contador_agua, contador_energia, contador_gas,
                descripcion_tratamiento, descripcion_usos, delimitacion_norte, delimitacion_sur,
                delimitacion_oriente, delimitacion_occidente, via_principal, via_secundaria
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """
                        
                id_caracteristicas = db.insertar(query_caracteristicas, (
                    self.id_avaluo, self.transporte_texto.toPlainText(), self.amoblamiento_texto.toPlainText(), valores_checkbox["Acueducto"], valores_checkbox["Gas Natural"], valores_checkbox["Telefonía Fija"], valores_checkbox["Recolección de Basuras"], valores_checkbox["Alcantarillado"], valores_checkbox["Energía Eléctrica"], valores_checkbox["Contador de Agua"], valores_checkbox["Contador de Energia"], valores_checkbox["Contador de Gas"], self.descripcion_tratamientos.toPlainText(), self.descripcion_usos.toPlainText(), self.norte.text(), self.sur.text(), self.oriente.text(), self.occidente.text(), self.vias_principales_texto.toPlainText(), self.vias_secundarias_texto.toPlainText()
                ))
                
            # Insertar en usos_sector
              
            for i in range(self.imagenes_usos_layout.count()):
                # Obtener el contenedor en la posición actual
                contenedor = self.imagenes_usos_layout.itemAt(i).widget()
                id_imagen = contenedor.property("id_imagen") if contenedor else None
                

                if contenedor:
                    # Obtener el QLabel y el QLineEdit dentro del contenedor
                    label = contenedor.findChild(QLabel)
                    line_edit = contenedor.findChild(QLineEdit)
                    
                    # Obtener el texto del QLineEdit
                    texto_descripcion = line_edit.text() if line_edit else "Sin descripción"
                    
                    # Obtener el path de la propiedad del label
                    path_imagen = contenedor.property("path_imagen") if contenedor else "Sin imagen"
                    
                    existe_imagen = db.consultar("SELECT id FROM usos_sector WHERE id = %s", (id_imagen,))
                    print(f"Existe imagen: {len(existe_imagen)}, ID: {id_imagen}")
                    if len(existe_imagen)>0:

                        query_usos = """
                        UPDATE usos_sector
                        SET uso = %s, path_imagen = %s
                        WHERE id = %s
                        """
                        print(query_usos)
                        print(f"Actualizando uso con ID {id_imagen}")
                        
                        db.actualizar(query_usos, (texto_descripcion, path_imagen,id_imagen))


                    else:
                        query_usos = """
                        INSERT INTO usos_sector (caracteristicas_sector_id, uso, path_imagen)
                        VALUES (%s, %s, %s) RETURNING id;
                        """
                        print(query_usos)
                        
                        id_imagen = db.insertar(query_usos, (id_caracteristicas, texto_descripcion, path_imagen))

                        contenedor.setProperty("id_imagen", id_imagen)
            
            # Insertar en tratamientos_sector
                        
            for i in range(self.imagenes_tratamientos_layout.count()):
                # Obtener el contenedor en la posición actual
                contenedor = self.imagenes_tratamientos_layout.itemAt(i).widget()
                id_imagen = contenedor.property("id_imagen") if contenedor else None

                if contenedor:
                    # Obtener el QLabel y el QLineEdit dentro del contenedor
                    label = contenedor.findChild(QLabel)
                    line_edit = contenedor.findChild(QLineEdit)
                    
                    # Obtener el texto del QLineEdit
                    texto_descripcion = line_edit.text() if line_edit else ""
                    
                    # Obtener el path de la propiedad del label
                    path_imagen = contenedor.property("path_imagen") if contenedor else ""
                    
                    existe_imagen = db.consultar("SELECT id FROM tratamientos_sector WHERE id = %s", (id_imagen,))
                    
                    if len(existe_imagen)>0:
                    
                        query_tratamiento = """ UPDATE tratamientos_sector
                        SET tratamiento = %s, path_imagen = %s
                        WHERE id = %s"""
                        print(query_tratamiento)
                        
                        db.actualizar(query_tratamiento, (texto_descripcion, path_imagen, id_imagen))


                    else:
                        query_tratamiento = """
                        INSERT INTO tratamientos_sector (caracteristicas_sector_id, tratamiento, path_imagen)
                        VALUES (%s, %s, %s) RETURNING id;
                        """
                        print(query_tratamiento)
                        
                        id_imagen = db.insertar(query_tratamiento, (id_caracteristicas, texto_descripcion, path_imagen))
                        
                        contenedor.setProperty("id_imagen", id_imagen)


            # Confirmar los cambios
            db.cerrar_conexion()
            print("Datos guardados correctamente.")
            
        except Exception as e:
            db.rollback()
            db.cerrar_conexion()
            print(f"Error al guardar los datos: {e}")
    
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
        btn_agregar.setStyleSheet(self.group_style)
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


    def mostrar_imagen(self, file_path, layout):
        contenedor = QWidget()
        hbox = QHBoxLayout(contenedor)
        
        label = QLabel()
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        
        btn_eliminar = QPushButton("x")
        btn_eliminar.setObjectName("botonEliminar")
        btn_eliminar.setStyleSheet(self.group_style)
        btn_eliminar.clicked.connect(lambda: self.eliminar_imagen(contenedor))
        
        hbox.addWidget(label)
        hbox.addWidget(btn_eliminar)
        
        layout.addWidget(contenedor)

    def eliminar_imagen(self, widget):
        widget.deleteLater()
     
    def on_tab_changed(self, tab_panel, index):
        
        print(f"Cambio de pestaña detectado. {tab_panel.tabText(index)}")
        # Verificar si la pestaña activa es la de "Características del Sector"
        if tab_panel.tabText(index) == "Características del Sector":
            """     self.pestana_activa = True  # Marcar la pestaña como activa
                print("Pestaña 'Características del Sector' está activa.")
            elif self.pestana_activa: """
            print("Pestaña 'Características del Sector' dejó de estar activa. Guardando datos...")
            # Si la pestaña estuvo activa y se cambió a otra pestaña, guardar los datos
            
            try:
                if self.amoblamiento_texto.toPlainText().strip() != "":                    
                    self.guardar_datos()
                    
            except Exception as e:
                print(f"Error al guardar datos: {e}")
            
            self.pestana_activa = False  # Resetear el estado

    def cargar_datos_sector(self, id_avaluo):
        db = self.ventana_principal.obtener_conexion_db()
        db.conectar()
        try:
            # Consulta principal
            query = """
            SELECT transporte, amoblamiento_urbano, agua, gas, telefonia, recoleccion_basuras,
                   alcantarillado, energia, contador_agua, contador_energia, contador_gas,
                   descripcion_tratamiento, descripcion_usos, delimitacion_norte, delimitacion_sur,
                   delimitacion_oriente, delimitacion_occidente, via_principal, via_secundaria, id
            FROM caracteristicas_sector
            WHERE id_avaluo = %s
            """
             # Obtener path_trabajo

            query_path_trabajo = """
            select a.path_trabajo 
            from "Avaluos" a 
            where a."Avaluo_id" = %s
            """
           

            print(f"Ejecutando consulta para id_avaluo: {id_avaluo}")
            # IMPORTANTE: pasar los parámetros como tupla (incluso si es 1) -> (id_avaluo,)
            # Pasar (id_avaluo) no crea una tupla y puede provocar errores de formateo
            resultado = db.consultar(query, (id_avaluo,))
            
            self.path_trabajo = db.consultar(query_path_trabajo, (id_avaluo,))[0][0]

            if resultado:
                datos = resultado[0]
                self.transporte_texto.setPlainText(datos[0])
                self.amoblamiento_texto.setPlainText(datos[1])
                # Checkboxes
                servicios = [
                    "Acueducto", "Gas Natural", "Telefonía Fija", "Recolección de Basuras",
                    "Alcantarillado", "Energía Eléctrica", "Contador de Agua",
                    "Contador de Energia", "Contador de Gas"
                ]
                valores_servicios = datos[2:11]
                for i, servicio in enumerate(servicios):
                    for cb in self.col1.parentWidget().findChildren(QCheckBox) + self.col2.parentWidget().findChildren(QCheckBox):
                        if cb.text() == servicio:
                            cb.setChecked(valores_servicios[i])
                self.descripcion_tratamientos.setPlainText(datos[11])
                self.descripcion_usos.setPlainText(datos[12])
                self.norte.setText(datos[13])
                self.sur.setText(datos[14])
                self.oriente.setText(datos[15])
                self.occidente.setText(datos[16])
                self.vias_principales_texto.setPlainText(datos[17])
                self.vias_secundarias_texto.setPlainText(datos[18])
                self.caracteristicas_sector_id = datos[19]  # Guardar el ID para usos y tratamientos
                

            else:
                print("No se encontraron datos para el avalúo.")
                return  # Salir si no hay datos

            # Cargar usos y tratamientos del sector
            if resultado:
                self.cargar_usos_sector(datos[19])
                self.cargar_tratamientos_sector(datos[19])
            else:
                print("No se encontraron datos para el avalúo.")
        except Exception as e:
            print(f"Error al cargar los datos del sector: {e}")
        finally:
            db.cerrar_conexion()
    
    def cargar_tratamientos_sector(self, caracteristicas_sector_id):

        db = self.ventana_principal.obtener_conexion_db()
        db.conectar()

        try:
            query = """
            SELECT tratamiento, path_imagen, id
            FROM tratamientos_sector
            WHERE caracteristicas_sector_id = %s
            """
            resultados = db.consultar(query, (caracteristicas_sector_id,))
            for tratamiento, path_imagen, id_imagen in resultados:
                # Aquí puedes crear el widget para mostrar el tratamiento y la imagen
                FuncionesImagenes.agregar_imagen(self, self.imagenes_tratamientos_layout, path_imagen, tratamiento, id_imagen,'tratamientos_sector', ventana_principal=self.ventana_principal)

                
        except Exception as e:
            print(f"Error al cargar tratamientos: {e}")
        finally:
            db.cerrar_conexion()
    
    def cargar_usos_sector(self, caracteristicas_sector_id):

        db = self.ventana_principal.obtener_conexion_db()
        db.conectar()

        try:
            query = """
            SELECT uso, path_imagen, id
            FROM usos_sector
            WHERE caracteristicas_sector_id = %s
            """
            resultados = db.consultar(query, (caracteristicas_sector_id,))
            for uso, path_imagen, id_imagen in resultados:
                print(f"Cargando uso: {uso}, imagen: {path_imagen}, id: {id_imagen}")
                FuncionesImagenes.agregar_imagen(self, self.imagenes_usos_layout, path_imagen, uso, id_imagen, 'usos_sector', ventana_principal=self.ventana_principal)

                
        except Exception as e:
            print(f"Error al cargar usos: {e}")
        finally:
            db.cerrar_conexion()
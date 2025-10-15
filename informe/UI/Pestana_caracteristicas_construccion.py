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
from Funciones_imagenes import FuncionesImagenes
from DB import DB

class PestanaCaracteristicasConstruccion(QWidget):
    
    def __init__(self, tab_panel: QTabWidget, id_avaluo= ""):
        super().__init__()
    # Widget principal para la pestaña

        self.basededatos = 'seshat'
        self.id_avaluo = id_avaluo

        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        db.conectar()
        query = "SELECT matricula_inmobiliaria, id_inmueble FROM inmuebles WHERE avaluo_id = %s"
        self.matriculas = db.consultar(query, (self.id_avaluo))
        
        db.cerrar_conexion()
        
        pestana = QWidget()
        
        self.group_style = Estilos.cargar_estilos(self,"styles.css")
        
        # Crear scroll area para toda la pestaña
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_area.setStyleSheet(self.group_style)
        
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
        btn_agregar_croquis.clicked.connect(lambda: FuncionesImagenes.agregar_imagen(self, self.croquis_container))
        
        layout_croquis.addLayout(self.croquis_container)
        layout_croquis.addWidget(btn_agregar_croquis)
        
        # Grupo 3: Área construida
        grupo_area = QGroupBox("Área Construida")
        grupo_area.setStyleSheet(group_style)
        layout_area = QVBoxLayout(grupo_area)
        
        # Crear tabla
        self.tabla_area = QTableWidget(0, 5)  # 0 filas iniciales, 3 columnas
        self.tabla_area.setHorizontalHeaderLabels(["MI", "Identificación", "Área (m²)", "Destinación", "Dependencias"])
        
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
        
        grupo_estado = QGroupBox("Estado de Conservación")
        grupo_estado.setStyleSheet(group_style)
        form_estado = QFormLayout(grupo_estado)
        
        self.estructura = QTextEdit()
        self.acabados = QTextEdit()
        
        self.estructura.setFixedHeight(100)
        self.acabados.setFixedHeight(100)
        
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
        layout_principal.addWidget(grupo_area)
        layout_principal.addWidget(fila_superior)
        
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

    def agregar_fila_area(self):
        row_count = self.tabla_area.rowCount()
        self.tabla_area.insertRow(row_count)

        # Crear combo box para la columna "MI"
        self.combo_matriculas = QComboBox()
        
        for r in self.matriculas:
            print(r)
            self.combo_matriculas.addItem(str(r[0]))
            index = self.combo_matriculas.count() - 1
            self.combo_matriculas.setItemData(index, r[1], role=Qt.ItemDataRole.UserRole)
        
        self.tabla_area.setCellWidget(row_count, 0, self.combo_matriculas)

        # Identificación

        tipos_construccion = [
            "Casa", "Bodega", "Local comercial", "Ramada", "Cobertizo", "Galpon", "Establo", "Cochera", "Silo", "Piscina", "Tanque", "Beneficiadero", "Secadero", "Kiosco", "Alberca", "Capilla", "Corral", "Poso", "Muelle", "Cancha", "Via", "Placa huella", "Zona Dura", "Cimientos", "Hangar", "Camaronera", "Pergola", "Glamping", "Cerca", "Cerramiento", "Sotano", "Cocina", "Baño", "Deposito", "Urbanismo"
        ]
        self.combo_tipo_construccion = QComboBox()
        self.combo_tipo_construccion.addItems(tipos_construccion)
        self.tabla_area.setCellWidget(row_count, 1, self.combo_tipo_construccion)
        
        # Área (solo números)
        area_item = QTableWidgetItem()
        area_item.setFlags(area_item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.tabla_area.setItem(row_count, 2, area_item)
        
        # 3. ComboBox de usos
        usos = ["Residencial", "Comercial", "Industrial", "Servicios", "Dotacional", "Anexo"]
        self.combo_usos = QComboBox()
        self.combo_usos.addItems(usos)
        self.tabla_area.setCellWidget(row_count, 3, self.combo_usos)

        if self.tabla_area.rowCount() > 1:
            result, mensaje = self.validar_campos_construccion(row_count)
            if result:

                self.guardar_construccion(row_count)
            else:
                QMessageBox.warning(self, "Advertencia", mensaje)

    def eliminar_fila_area(self):
        current_row = self.tabla_area.currentRow()
        if current_row >= 0:
            self.tabla_area.removeRow(current_row)

    def validar_campos_construccion(self, row):
        # Validar combo matriculas
        combo_matricula = self.tabla_area.cellWidget(row, 0)
        if not combo_matricula or not combo_matricula.currentText().strip():
            return False, "Seleccione la matrícula inmobiliaria."

        # Validar tipo de construcción
        combo_tipo = self.tabla_area.cellWidget(row, 1)
        if not combo_tipo or not combo_tipo.currentText().strip():
            return False, "Seleccione el tipo de construcción."

        # Validar área
        area_item = self.tabla_area.item(row, 2)
        if not area_item or not area_item.text().strip():
            return False, "Ingrese el área construida."

        # Validar uso
        combo_uso = self.tabla_area.cellWidget(row, 3)
        if not combo_uso or not combo_uso.currentText().strip():
            return False, "Seleccione el uso de la construcción."

        # Validar dependencias
        dependencias_item = self.tabla_area.item(row, 4)
        if not dependencias_item or not dependencias_item.text().strip():
            return False, "Ingrese las dependencias."

        # Validar datos generales
        if self.num_pisos.value() == 0:
            return False, "Ingrese el número de pisos."
        if self.vetustez.text().strip() == "":
            return False, "Ingrese la vetustez."
        if self.vida_util.text().strip() == "":
            return False, "Ingrese la vida útil."
        if self.vida_restante.text().strip() == "":
            return False, "Ingrese la vida restante."

        # Validar especificaciones constructivas
        if self.cimentacion.currentText().strip() == "":
            return False, "Seleccione la cimentación."
        if self.estructura_const.currentText().strip() == "":
            return False, "Seleccione la estructura."
        if self.muros.currentText().strip() == "":
            return False, "Seleccione los muros."
        if self.cubierta.currentText().strip() == "":
            return False, "Seleccione la cubierta."
        if self.fachada.currentText().strip() == "":
            return False, "Seleccione la fachada."
        if self.cielo_raso.currentText().strip() == "":
            return False, "Seleccione el cielo raso."

        # Validar estado de conservación
        if self.estructura.toPlainText().strip() == "":
            return False, "Ingrese la descripción de la estructura."
        if self.acabados.toPlainText().strip() == "":
            return False, "Ingrese la descripción de los acabados."

        return True, ""    

    def guardar_construccion(self, row):
        
        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        db.conectar()
    
        # Obtén los datos de la fila
        combo_matricula = self.tabla_area.cellWidget(row, 0)
        combo_tipo_construccion = self.tabla_area.cellWidget(row, 1)
        area_item = self.tabla_area.item(row, 2)
        combo_uso = self.tabla_area.cellWidget(row, 3)
        dependencias_item = self.tabla_area.item(row, 4)

        # Obtiene el id del inmueble seleccionado
        inmueble_id = combo_matricula.currentData(role=Qt.ItemDataRole.UserRole)  # O el valor real del id según tu lógica
        print("Inmueble ID seleccionado:", inmueble_id)
        # Datos principales de la construcción
        query_construccion = """
            INSERT INTO construcciones (
                inmueble_id, num_pisos, num_sotanos, vetustez, vida_util, vida_restante,
                tipo_construccion, uso, area, dependencias, cimentacion,
                estructura, muros, cubierta, fachada, cielo_raso, estructura_estado, acabados_estado,
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        datos = (
            inmueble_id,
            self.num_pisos.value(),
            self.num_sotanos.value(),
            self.vetustez.text(),
            self.vida_util.text(),
            self.vida_restante.text(),
            combo_tipo_construccion.currentText(),
            combo_uso.currentText(),
            area_item.text() if area_item else None,
            combo_uso.currentText(),
            dependencias_item.text() if dependencias_item else None,
            self.cimentacion.currentText(),
            self.estructura_const.currentText(),
            self.muros.currentText(),
            self.cubierta.currentText(),
            self.fachada.currentText(),
            self.cielo_raso.currentText(),
            self.acabados.toPlainText(),
            self.estructura.toPlainText()
        )

        id_construccion = db.insertar(query_construccion, datos)
    
        # Guardar croquis asociados
        for i in range(self.croquis_container.count()):
            widget = self.croquis_container.itemAt(i).widget()
            if widget:
                label = widget.findChild(QLabel)
                descripcion = widget.findChild(QLineEdit)
                path_imagen = label.property("path_imagen") if label else None
                texto_descripcion = descripcion.text() if descripcion else ""
                query_croquis = """
                    INSERT INTO croquis_construccion (construccion_id, imagen_path, descripcion)
                    VALUES (%s, %s, %s)
                """
                db.insertar(query_croquis, (id_construccion, path_imagen, texto_descripcion))
    
        db.cerrar_conexion()
        QMessageBox.information(self, "Guardado", "Datos de la construcción guardados correctamente.")
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
        
        self.vetustez = QSpinBox()
        self.vetustez.setRange(0, 100)
        self.vida_util = QSpinBox()
        self.vida_util.setRange(0, 100)
        self.vida_restante = QSpinBox()
        self.vida_restante.setRange(0, 100)

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
        self.cargar_datos_construccion()
    # Métodos auxiliares

    def agregar_fila_area(self):

        row_count = self.tabla_area.rowCount()
        
        if row_count >= 1:
            result, mensaje = self.validar_campos_construccion(row_count-1)

            if result:
                    
                self.guardar_construccion(row_count-1)

            else:
                QMessageBox.warning(self, "Advertencia", mensaje)
                return
            self.limpiar_datos()
        
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
            "", "Casa", "Bodega", "Local comercial", "Ramada", "Cobertizo", "Galpon", "Establo", "Cochera", "Silo", "Piscina", "Tanque", "Beneficiadero", "Secadero", "Kiosco", "Alberca", "Capilla", "Corral", "Poso", "Muelle", "Cancha", "Via", "Placa huella", "Zona Dura", "Cimientos", "Hangar", "Camaronera", "Pergola", "Glamping", "Cerca", "Cerramiento", "Sotano", "Cocina", "Baño", "Deposito", "Urbanismo"
        ]
        self.combo_tipo_construccion = QComboBox()
        self.combo_tipo_construccion.addItems(tipos_construccion)
        self.tabla_area.setCellWidget(row_count, 1, self.combo_tipo_construccion)
        
        # Área (solo números)
        area_item = QTableWidgetItem()
        area_item.setFlags(area_item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.tabla_area.setItem(row_count, 2, area_item)
        
        # 3. ComboBox de usos
        usos = ["" , "Residencial", "Comercial", "Industrial", "Servicios", "Dotacional", "Anexo"]
        self.combo_usos = QComboBox()
        self.combo_usos.addItems(usos)
        self.tabla_area.setCellWidget(row_count, 3, self.combo_usos)

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
        
        try:
             
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

            # Verificar si ya existe una construcción para este inmueble con este id
            existe_construccion = db.consultar("SELECT id FROM construcciones WHERE inmueble_id = %s", (inmueble_id,))
            if len(existe_construccion) > 0:
                print("Ya existe una construcción para este inmueble.")

                # Actualizar los datos de la construcción existente
                query_update = """
                    UPDATE construcciones
                    SET num_pisos = %s, num_sotanos = %s, vetustez = %s, vida_util = %s, vida_restante = %s, tipo_construccion = %s, uso = %s, area = %s, dependencias = %s, cimentacion = %s, estructura = %s, muros = %s, cubierta = %s, fachada = %s, cielo_raso = %s, estructura_estado = %s, acabados_estado = %s
                    WHERE inmueble_id = %s
                """
                datos_update = (
                    self.num_pisos.value(),
                    self.num_sotanos.value(),
                    self.vetustez.value(),
                    self.vida_util.value(),
                    self.vida_restante.value(),
                    combo_tipo_construccion.currentText(),          
                    combo_uso.currentText(),
                    area_item.text() if area_item else None,
                    dependencias_item.text() if dependencias_item else None,
                    self.cimentacion.currentText(),
                    self.estructura_const.currentText(),
                    self.muros.currentText(),
                    self.cubierta.currentText(),
                    self.fachada.currentText(),
                    self.cielo_raso.currentText(),
                    self.estructura.toPlainText(),
                    self.acabados.toPlainText(),
                    inmueble_id
                )
                print("Actualizando construcción:", (query_update, datos_update))
                db.actualizar(query_update, datos_update)

                return  # Evitar insertar duplicados

            else:

                # Datos principales de la construcción
                query_construccion = """
                    INSERT INTO construcciones (
                        inmueble_id, num_pisos, num_sotanos, vetustez, vida_util, vida_restante, tipo_construccion, uso, area, dependencias, cimentacion, estructura, muros, cubierta, fachada, cielo_raso, estructura_estado, acabados_estado
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """
                datos = (
                    inmueble_id,
                    self.num_pisos.value(),
                    self.num_sotanos.value(),
                    self.vetustez.value(),
                    self.vida_util.value(),
                    self.vida_restante.value(),
                    combo_tipo_construccion.currentText(),
                    combo_uso.currentText(),
                    area_item.text() if area_item else None,
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

                print("Datos a insertar:", (query_construccion, datos))

                id_construccion = db.insertar(query_construccion, datos)
        
            # Guardar croquis asociados
            for i in range(self.croquis_container.count()):
                widget = self.croquis_container.itemAt(i).widget()
                id_imagen = widget.property("id_imagen") if widget else None

                if widget:

                    # Obtener qlineedit y qlabel de la imagen
                    label = widget.findChild(QLabel)
                    descripcion = widget.findChild(QLineEdit)

                    #obtener texto descripcion y path imagen
                    texto_descripcion = descripcion.text() if descripcion else ""
                    path_imagen = widget.property("path_imagen") if label else None

                    existe_imagen = db.consultar("SELECT id FROM croquis_construccion WHERE id = %s", (id_imagen,))

                    if len(existe_imagen) > 0:
                        query_croquis = """
                            UPDATE croquis_construccion
                            SET imagen_path = %s, descripcion = %s
                            WHERE id = %s
                        """
                        print("Actualizando croquis:", (query_croquis, (path_imagen, texto_descripcion, id_imagen)))
                        db.actualizar(query_croquis, (path_imagen, texto_descripcion, id_imagen))
                    else:   
                        query_croquis = """
                            INSERT INTO croquis_construccion (construccion_id, imagen_path, descripcion)
                            VALUES (%s, %s, %s) RETURNING id
                        """
                        print("Insertando croquis:", (query_croquis, (id_construccion, path_imagen, texto_descripcion)))
                        db.insertar(query_croquis, (id_construccion, path_imagen, texto_descripcion))
        
            db.cerrar_conexion()
            QMessageBox.information(self, "Guardado", "Datos de la construcción guardados correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar los datos de la construcción: {e}")
            print(f"Error al guardar los datos de la construcción: {e}")

    def cargar_datos_construccion(self):

        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        db.conectar()

        # Consulta construcciones asociadas al avaluo
        query = """
            SELECT c.id, c.inmueble_id, i.matricula_inmobiliaria, c.tipo_construccion, c.uso, c.area, c.dependencias,
                   c.num_pisos, c.num_sotanos, c.vetustez, c.vida_util, c.vida_restante,
                   c.estructura, c.acabados_estado, c.muros, c.cubierta, c.fachada, c.cielo_raso, c.cimentacion, c.estructura_estado 
            FROM construcciones c
            JOIN inmuebles i ON c.inmueble_id = i.id_inmueble
            WHERE i.avaluo_id =  %s
        """
        construcciones = db.consultar(query, (self.id_avaluo,))
        print("Construcciones encontradas:", construcciones)
        self.tabla_area.setRowCount(0)

        for row_data in construcciones:
            row_count = self.tabla_area.rowCount()
            self.tabla_area.insertRow(row_count)

            # MI (matricula)
            combo_matricula = QComboBox()
            combo_matricula.addItem("")
            for r in self.matriculas:
                combo_matricula.addItem(str(r[0]))
                index = combo_matricula.count() - 1
                combo_matricula.setItemData(index, r[1], role=Qt.ItemDataRole.UserRole)
            # Seleccionar la matrícula correspondiente
            idx = combo_matricula.findText(str(row_data[2]))
            if idx >= 0:
                combo_matricula.setCurrentIndex(idx)
            self.tabla_area.setCellWidget(row_count, 0, combo_matricula)

            # Tipo construcción
            combo_tipo = QComboBox()
            tipos_construccion = [
                "Casa", "Bodega", "Local comercial", "Ramada", "Cobertizo", "Galpon", "Establo", "Cochera", "Silo", "Piscina", "Tanque", "Beneficiadero", "Secadero", "Kiosco", "Alberca", "Capilla", "Corral", "Poso", "Muelle", "Cancha", "Via", "Placa huella", "Zona Dura", "Cimientos", "Hangar", "Camaronera", "Pergola", "Glamping", "Cerca", "Cerramiento", "Sotano", "Cocina", "Baño", "Deposito", "Urbanismo"
            ]
            combo_tipo.addItems(tipos_construccion)
            idx_tipo = combo_tipo.findText(str(row_data[3]))
            if idx_tipo >= 0:
                combo_tipo.setCurrentIndex(idx_tipo)
            self.tabla_area.setCellWidget(row_count, 1, combo_tipo)

            # Área
            area_item = QTableWidgetItem(str(row_data[5]) if row_data[5] is not None else "")
            self.tabla_area.setItem(row_count, 2, area_item)

            # Uso
            combo_uso = QComboBox()
            usos = ["Residencial", "Comercial", "Industrial", "Servicios", "Dotacional", "Anexo"]
            combo_uso.addItems(usos)
            idx_uso = combo_uso.findText(str(row_data[4]))
            if idx_uso >= 0:
                combo_uso.setCurrentIndex(idx_uso)
            self.tabla_area.setCellWidget(row_count, 3, combo_uso)

            # Dependencias
            dependencias_item = QTableWidgetItem(str(row_data[6]) if row_data[6] is not None else "")
            self.tabla_area.setItem(row_count, 4, dependencias_item)

            # Cargar datos generales y especificaciones
            self.num_pisos.setValue(row_data[7] if row_data[7] is not None else 0)
            self.num_sotanos.setValue(int(row_data[8]) if row_data[8] is not None else 0)
            self.vetustez.setValue(int(row_data[9]) if row_data[9] is not None else 0)
            self.vida_util.setValue(int(row_data[10]) if row_data[10] is not None else 0)
            self.vida_restante.setValue(int(row_data[11]) if row_data[11] is not None else 0)
            self.estructura_const.setCurrentText(str(row_data[12]) if row_data[12] is not None else "")
            self.acabados.setPlainText(str(row_data[13]) if row_data[13] is not None else "")
            self.muros.setCurrentText(str(row_data[14]) if row_data[14] is not None else "")
            self.cubierta.setCurrentText(str(row_data[15]) if row_data[15] is not None else "")
            self.fachada.setCurrentText(str(row_data[16]) if row_data[16] is not None else "")
            self.cielo_raso.setCurrentText(str(row_data[17]) if row_data[17] is not None else "")
            self.cimentacion.setCurrentText(str(row_data[18]) if row_data[18] is not None else "")
            self.estructura.setPlainText(str(row_data[19]) if row_data[19] is not None else "")

            # Cargar croquis asociados
            croquis_query = "SELECT imagen_path, descripcion FROM croquis_construccion WHERE construccion_id = %s"
            croquis = db.consultar(croquis_query, (row_data[0],))
            for imagen_path, descripcion in croquis:
                FuncionesImagenes.agregar_imagen(self, self.croquis_container, imagen_path, descripcion)

        db.cerrar_conexion()
    
    def limpiar_datos(self):
        row = self.tabla_area.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "No hay ninguna fila seleccionada.")
            return

        # Limpiar combo matricula
        combo_matricula = self.tabla_area.cellWidget(row, 0)
        if combo_matricula:
            combo_matricula.setCurrentIndex(0)

        # Limpiar tipo construcción
        combo_tipo = self.tabla_area.cellWidget(row, 1)
        if combo_tipo:
            combo_tipo.setCurrentIndex(0)

        # Limpiar área
        area_item = self.tabla_area.item(row, 2)
        if area_item:
            area_item.setText("")

        # Limpiar uso
        combo_uso = self.tabla_area.cellWidget(row, 3)
        if combo_uso:
            combo_uso.setCurrentIndex(0)

        # Limpiar dependencias
        dependencias_item = self.tabla_area.item(row, 4)
        if dependencias_item:
            dependencias_item.setText("")

        # Limpiar campos generales y especificaciones
        self.num_pisos.setValue(0)
        self.num_sotanos.setValue(0)
        self.vetustez.setValue(0)
        self.vida_util.setValue(0)
        self.vida_restante.setValue(0)
        self.estructura.clear()
        self.acabados.clear()
        self.cimentacion.setCurrentIndex(0)
        self.estructura_const.setCurrentIndex(0)
        self.muros.setCurrentIndex(0)
        self.cubierta.setCurrentIndex(0)
        self.fachada.setCurrentIndex(0)
        self.cielo_raso.setCurrentIndex(0)
        # Limpiar croquis
        while self.croquis_container.count():
            item = self.croquis_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.acabados.clear()
        self.estructura.clear()

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
        self.datos_sin_guardar = {}
        self.datos_sin_guardar_coquis = {}
        self.fila_anterior = 0
        self.editando_fila = False
        self.datos_actuales = {}

        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        db.conectar()
        query = "SELECT matricula_inmobiliaria, id_inmueble FROM inmuebles WHERE avaluo_id = %s"
        # Pasar el parámetro como tupla de un elemento para evitar errores de formateo
        self.matriculas = db.consultar(query, (self.id_avaluo,))


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
        
        layout_croquis.addWidget(btn_agregar_croquis)
        layout_croquis.addLayout(self.croquis_container)
        
        # Grupo 3: Área construida
        grupo_area = QGroupBox("Área Construida")
        grupo_area.setStyleSheet(group_style)
        layout_area = QVBoxLayout(grupo_area)
        
        # Crear tabla
        self.tabla_area = QTableWidget(0, 5)  # 0 filas iniciales, 6 columnas
        self.tabla_area.setHorizontalHeaderLabels(["MI", "Identificación", "Área (m²)", "Destinación", "Dependencias"])
        
        # Configurar tabla
        self.tabla_area.horizontalHeader().setStretchLastSection(True)
        self.tabla_area.verticalHeader().setVisible(False)
        self.tabla_area.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        # Conectar selección de fila para actualizar los campos generales y croquis
        self.tabla_area.cellClicked.connect(self.actualizar_campos_desde_fila)
        # currentCellChanged signature: currentRow, currentColumn, previousRow, previousColumn
        self.tabla_area.currentCellChanged.connect(lambda curR, curC, prevR, prevC: self.actualizar_campos_desde_fila(curR))
        
        # Botones para tabla
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_agregar_fila = QPushButton("Agregar Fila")
        btn_eliminar_fila = QPushButton("Eliminar Fila")
        btn_guardar_fila = QPushButton("Guardar Cambios")
        
        btn_agregar_fila.clicked.connect(self.agregar_fila_area)
        btn_eliminar_fila.clicked.connect(self.eliminar_fila_area)
        btn_guardar_fila.clicked.connect(lambda: self.guardar_construccion(self.tabla_area.currentRow()))

        btn_layout.addWidget(btn_agregar_fila)
        btn_layout.addWidget(btn_eliminar_fila)
        btn_layout.addWidget(btn_guardar_fila)

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
            "Estuco acrílico",
            "Sin Muros"
        ]
        
        opciones_cubierta = [
            "",
            "Teja en Fibrocemento", 
            "Teja de Zinc", 
            "Cerámica", 
            "Madera", 
            "Policarbonato", 
            "Placa en Concreto",
            "Sin Cubierta"
        ]
        
        opciones_fachada = [
            "",
            "Ladrillo a la vista", 
            "Carraplast", 
            "Cemento afinado", 
            "Pañete y pintura", 
            "Cerámica", 
            "Madera",
            "Sin Fachada"
        ]
        
        opciones_cielo_raso = [
            "",
            "PVC", 
            "Placa de yeso", 
            "Madera", 
            "Metal", 
            "Fibra de vidrio",
            "Sin Cielo Raso"
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
        pestana.mi_pestana = self
        
        tab_panel.addTab(pestana, "Características de Construcción")
        
        # Agregar fila inicial a la tabla
        
        self.cargar_datos_construccion()
    # Métodos auxiliares

    def obtener_actuales(self,row_idx):
        res = {}
        combo_mat = self.tabla_area.cellWidget(row_idx, 0)
        res['matricula'] = combo_mat.currentText().strip() if combo_mat else ''
        res['inmueble_id'] = combo_mat.currentData(role=Qt.ItemDataRole.UserRole) if combo_mat else None

        combo_tipo = self.tabla_area.cellWidget(row_idx, 1)
        res['tipo'] = combo_tipo.currentText().strip() if combo_tipo else ''

        item_area = self.tabla_area.item(row_idx, 2)
        res['area'] = item_area.text().strip() if item_area and item_area.text() else ''

        combo_uso = self.tabla_area.cellWidget(row_idx, 3)
        res['uso'] = combo_uso.currentText().strip() if combo_uso else ''

        item_dep = self.tabla_area.item(row_idx, 4)
        res['dependencias'] = item_dep.text().strip() if item_dep and item_dep.text() else ''

        # Datos generales / especificaciones (si existen en la interfaz)
        try:
            res['num_pisos'] = int(self.num_pisos.value())
            res['num_sotanos'] = int(self.num_sotanos.value())
            res['vetustez'] = int(self.vetustez.value())
            res['vida_util'] = int(self.vida_util.value())
            res['vida_restante'] = int(self.vida_restante.value())
        except Exception:
            # si no existen, omitir
            res['num_pisos'] = res.get('num_pisos', None)
            res['num_sotanos'] = res.get('num_sotanos', None)
        # especificaciones
        res['cimentacion'] = self.cimentacion.currentText().strip() if hasattr(self, 'cimentacion') else ''
        res['estructura_const'] = self.estructura_const.currentText().strip() if hasattr(self, 'estructura_const') else ''
        res['muros'] = self.muros.currentText().strip() if hasattr(self, 'muros') else ''
        res['cubierta'] = self.cubierta.currentText().strip() if hasattr(self, 'cubierta') else ''
        res['fachada'] = self.fachada.currentText().strip() if hasattr(self, 'fachada') else ''
        res['cielo_raso'] = self.cielo_raso.currentText().strip() if hasattr(self, 'cielo_raso') else ''

        # textos largos
        res['estructura_estado'] = self.estructura.toPlainText().strip() if hasattr(self, 'estructura') else ''
        res['acabados_estado'] = self.acabados.toPlainText().strip() if hasattr(self, 'acabados') else ''

        # Croquis
        croquis = []
        try:

            # Guardar croquis asociados
            for i in range(self.croquis_container.count()):
                widget = self.croquis_container.itemAt(i).widget()

                id_imagen = widget.property("id_imagen") if widget else None
                print("id_imagen croquis:", id_imagen)
                if widget:

                    # Obtener qlineedit y qlabel de la imagen
                    label = widget.findChild(QLabel)
                    descripcion = widget.findChild(QLineEdit)

                    #obtener texto descripcion y path imagen
                    texto_descripcion = descripcion.text() if descripcion else ""
                    path_imagen = widget.property("path_imagen") if label else None

                    croquis.append({
                        'id_imagen': id_imagen,
                        'path': path_imagen,
                        'descripcion': texto_descripcion
                    })
        except Exception:
            croquis = []
        # normalizar croquis a lista de tuplas (path, descripcion)
        res['croquis'] = [(c.get('path'), c.get('descripcion')) for c in croquis]
        return res

    def actualizar_campos_desde_fila(self, row):

        """Actualizar campos generales, especificaciones y croquis según la fila seleccionada."""
        if row is None or row < 0:
            return

        datos_comparacion = self.obtener_actuales(self.fila_anterior)

        # comparar datos para evaluar si hay cambios sin guardar
        
        if self.datos_actuales:
            for key in datos_comparacion:
                if key in self.datos_actuales:
                    if datos_comparacion[key] != self.datos_actuales[key]:
                        
                        """
                        Muestra un QMessageBox preguntando si guardar o descartar los cambios.
                        Retorna: "guardar", "descartar" o "cancelar"
                        """
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Guardar cambios")
                        msg.setText("Se han detectado cambios. ¿Desea guardar los cambios actuales o descartarlos?")
                        msg.setIcon(QMessageBox.Icon.Question)

                        btn_guardar = msg.addButton("Guardar", QMessageBox.ButtonRole.AcceptRole)
                        btn_descartar = msg.addButton("Descartar", QMessageBox.ButtonRole.DestructiveRole)

                        msg.setDefaultButton(btn_guardar)
                        msg.exec()

                        clicked = msg.clickedButton()
                        if clicked == btn_guardar:
                            self.guardar_construccion(self.fila_anterior)
                        """ elif clicked == btn_descartar:
                            return "descartar" """
             
 

        # Obtener combo matricula de la fila
        combo_matricula = self.tabla_area.cellWidget(row, 0)
        if not combo_matricula:
            return
        
        resultado, mensaje = self.validar_campos_construccion(self.fila_anterior)
        if resultado == False and self.editando_fila and self.fila_anterior != row:
            QMessageBox.warning(self, "Advertencia", "Por favor, termine de editar la fila actual antes de cambiar a otra.")
            if resultado == False:
                QMessageBox.warning(self, "Advertencia", mensaje)
            
            self.tabla_area.selectRow(self.fila_anterior); self.tabla_area.setCurrentCell(self.fila_anterior, 4)
            return

        # Intentar obtener construccion_id guardado en la propiedad del combo
        construccion_id = combo_matricula.property("construccion_id")

        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        db.conectar()
        filas = []
        # Si tenemos construccion_id, cargar directamente
        if construccion_id:
            query = "SELECT num_pisos, num_sotanos, vetustez, vida_util, vida_restante, cimentacion, estructura, muros, cubierta, fachada, cielo_raso, estructura_estado, acabados_estado FROM construcciones WHERE id = %s"
            filas = db.consultar(query, (construccion_id,))

            """ if self.fila_anterior == self.tabla_area.rowCount() - 1:

                # Actualiza la información de la fila anterior antes de cargar la nueva

                datos = {
                    'num_pisos': self.num_pisos.value(),
                    'num_sotanos': self.num_sotanos.value(),
                    'vetustez': self.vetustez.value(),
                    'vida_util': self.vida_util.value(),
                    'vida_restante': self.vida_restante.value(),
                    'cimentacion': self.cimentacion.currentText(),
                    'estructura': self.estructura_const.currentText(),
                    'muros': self.muros.currentText(),
                    'cubierta': self.cubierta.currentText(),
                    'fachada': self.fachada.currentText(),
                    'cielo_raso': self.cielo_raso.currentText(),
                    'estructura_estado': self.estructura.toPlainText(),
                    'acabados_estado': self.acabados.toPlainText()
                }
                self.datos_sin_guardar[self.fila_anterior] = datos
            
                for i in range(self.croquis_container.count()):
                    item = self.croquis_container.itemAt(i)
                    if item is None:
                        continue
                    widget = item.widget()
                    if widget is None:
                        continue

                    # Buscar QLabel y QLineEdit dentro del widget
                    label = widget.findChild(QLabel)
                    descripcion = widget.findChild(QLineEdit)

                    path_imagen = None
                    if label is not None:
                        try:
                            path_imagen = label.property("path_imagen")
                        except Exception:
                            path_imagen = None

                    texto_descripcion = descripcion.text() if descripcion else ""

                    self.datos_sin_guardar_croquis.append({
                        'path': path_imagen,
                        'descripcion': texto_descripcion
                    })

                print('Cargando datos sin guardar para construccion_id:', construccion_id) """
        else:
            self.fila_anterior = row
            print('No hay construccion_id, no se puede cargar datos.')
            
            db.cerrar_conexion()    
            return

            """ #Almacena los datos sin guardar en un arreglo temporal
            if row in self.datos_sin_guardar:
                datos = self.datos_sin_guardar[row]
                self.num_pisos.setValue(datos['num_pisos'])
                self.num_sotanos.setValue(datos['num_sotanos'])
                self.vetustez.setValue(datos['vetustez'])
                self.vida_util.setValue(datos['vida_util'])
                self.vida_restante.setValue(datos['vida_restante'])
                self.cimentacion.setCurrentText(datos['cimentacion'])
                self.estructura_const.setCurrentText(datos['estructura'])
                self.muros.setCurrentText(datos['muros'])
                self.cubierta.setCurrentText(datos['cubierta'])
                self.fachada.setCurrentText(datos['fachada'])
                self.cielo_raso.setCurrentText(datos['cielo_raso'])
                self.estructura.setPlainText(datos['estructura_estado'])
                self.acabados.setPlainText(datos['acabados_estado'])
                # Cargar croquis guardados temporalmente
                if self.datos_sin_guardar_croquis:
                    for imagen_path, descripcion in self.datos_sin_guardar_croquis:
                        FuncionesImagenes.agregar_imagen(self, self.croquis_container, imagen_path, descripcion)

            else:
                
                datos = {
                    'num_pisos': self.num_pisos.value(),
                    'num_sotanos': self.num_sotanos.value(),
                    'vetustez': self.vetustez.value(),
                    'vida_util': self.vida_util.value(),
                    'vida_restante': self.vida_restante.value(),
                    'cimentacion': self.cimentacion.currentText(),
                    'estructura': self.estructura_const.currentText(),
                    'muros': self.muros.currentText(),
                    'cubierta': self.cubierta.currentText(),
                    'fachada': self.fachada.currentText(),
                    'cielo_raso': self.cielo_raso.currentText(),
                    'estructura_estado': self.estructura.toPlainText(),
                    'acabados_estado': self.acabados.toPlainText()
                }
                self.datos_sin_guardar[row] = datos            
                self.datos_sin_guardar_croquis = []
                for i in range(self.croquis_container.count()):
                    item = self.croquis_container.itemAt(i)
                    if item is None:
                        continue
                    widget = item.widget()
                    if widget is None:
                        continue

                    # Buscar QLabel y QLineEdit dentro del widget
                    label = widget.findChild(QLabel)
                    descripcion = widget.findChild(QLineEdit)

                    path_imagen = None
                    if label is not None:
                        try:
                            path_imagen = label.property("path_imagen")
                        except Exception:
                            path_imagen = None

                    texto_descripcion = descripcion.text() if descripcion else ""

                    self.datos_sin_guardar_croquis.append({
                        'path': path_imagen,
                        'descripcion': texto_descripcion
                    })
                print('imagenes sin guardar:', self.datos_sin_guardar_croquis)
            resultado, mensaje = self.validar_campos_construccion(row)

            print('Validando campos antes de cambiar fila:', resultado, mensaje)

            if resultado:
                print('row:', row)
                self.guardar_construccion(row)
                self.datos_sin_guardar_coquis = []
                self.datos_sin_guardar = {}
                self.fila_anterior = 0
                return
            else:
                print(mensaje) """

            
        if filas and len(filas) > 0:
            datos = filas[0]
            # Si la consulta devolvió id en la primera columna (cuando buscamos por inmueble)
            if construccion_id is None:
                # datos[0] es id cuando consultamos por inmueble_id
                construccion_id = datos[0]
                offset = 1
            else:
                offset = 0

            # Mapear valores según offset
            self.num_pisos.setValue(datos[0+offset] if datos[0+offset] is not None else 0)
            self.num_sotanos.setValue(datos[1+offset] if datos[1+offset] is not None else 0)
            try:
                # vetustez y vida util son QSpinBox ahora
                self.vetustez.setValue(int(datos[2+offset]) if datos[2+offset] is not None else 0)
                self.vida_util.setValue(int(datos[3+offset]) if datos[3+offset] is not None else 0)
                self.vida_restante.setValue(int(datos[4+offset]) if datos[4+offset] is not None else 0)
            except Exception:
                pass

            # Especificaciones
            self.cimentacion.setCurrentText(str(datos[5+offset]) if datos[5+offset] is not None else "")
            # estructura, muros, cubierta, fachada, cielo_raso
            self.estructura_const.setCurrentText(str(datos[6+offset]) if datos[6+offset] is not None else "")
            self.muros.setCurrentText(str(datos[7+offset]) if datos[7+offset] is not None else "")
            self.cubierta.setCurrentText(str(datos[8+offset]) if datos[8+offset] is not None else "")
            self.fachada.setCurrentText(str(datos[9+offset]) if datos[9+offset] is not None else "")
            self.cielo_raso.setCurrentText(str(datos[10+offset]) if datos[10+offset] is not None else "")

            # Estados/descripcion
            try:
                self.estructura.setPlainText(str(datos[11+offset]) if datos[11+offset] is not None else "")
                self.acabados.setPlainText(str(datos[12+offset]) if datos[12+offset] is not None else "")
            except Exception:
                # en caso de offset o campos faltantes
                pass

        else:
            # Si no hay registros, limpiar campos
            self.num_pisos.setValue(0)
            self.num_sotanos.setValue(0)
            self.vetustez.setValue(0)
            self.vida_util.setValue(0)
            self.vida_restante.setValue(0)
            self.cimentacion.setCurrentIndex(0)
            self.estructura_const.setCurrentIndex(0)
            self.muros.setCurrentIndex(0)
            self.cubierta.setCurrentIndex(0)
            self.fachada.setCurrentIndex(0)
            self.cielo_raso.setCurrentIndex(0)
            self.estructura.clear()
            self.acabados.clear()

        # Cargar croquis asociados (si tenemos construccion_id)
        # Primero limpiar contenedor de croquis
        while self.croquis_container.count() > 0:
            item = self.croquis_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        if construccion_id:
            croquis_query = "SELECT id, imagen_path, descripcion FROM croquis_construccion WHERE construccion_id = %s"
            croquis = db.consultar(croquis_query, (construccion_id,))
            for id_img, imagen_path, descripcion in croquis:
                # usar la función existente para añadir imagen pero con path y descripcion
                FuncionesImagenes.agregar_imagen(self, self.croquis_container, imagen_path, descripcion, id_img, "croquis_construccion")
        self.datos_actuales = self.obtener_actuales(row)
        self.fila_anterior = row
        print('Datos actuales cargados para fila', row, ':', self.datos_actuales)
        db.cerrar_conexion()

    def agregar_fila_area(self):

        row_count = self.tabla_area.rowCount()
        self.editando_fila = True
        
        if row_count >= 1:
            result, mensaje = self.validar_campos_construccion(row_count-1)

            """ if result:
                # Crea un mensaje preguntando al usuario si desea guardar los datos antes de agregar una nueva fila
                respuesta = QMessageBox.question(self, "Confirmar", "¿Desea guardar los cambios en la fila anterior?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

                if respuesta == QMessageBox.StandardButton.Yes:
                    print("Guardando construcción de la fila anterior antes de agregar nueva fila.")
                    self.guardar_construccion(row_count-1)
                
            else:
                QMessageBox.warning(self, "Advertencia", mensaje)
                return """
            self.limpiar_datos()
        
        self.tabla_area.insertRow(row_count)

        # Crear combo box para la columna "MI"
        combo_matriculas = QComboBox()
        combo_matriculas.addItem("")
        for r in self.matriculas:
            print(r)
            combo_matriculas.addItem(str(r[0]))
            index = combo_matriculas.count() - 1
            combo_matriculas.setItemData(index, r[1], role=Qt.ItemDataRole.UserRole)
        
        """ combo_matricula.setProperty("construccion_id", row_data[0])
        combo_matricula.setProperty("construccion_data", row_data) """

        self.tabla_area.setCellWidget(row_count, 0, combo_matriculas)

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
        self.fila_anterior = row_count

        """ datos = self.guardar_construccion(row_count, nueva_construccion=True)
        combo_matriculas.setProperty("construccion_id", datos[0])
        combo_matriculas.setProperty("construccion_data", datos) """

    def eliminar_fila_area(self):
        self.datos_actuales = {}
        row = self.tabla_area.currentRow()
        """ if current_row >= 0:
            self.tabla_area.removeRow(current_row) """
        
        if row < 0:
            QMessageBox.warning(self, "Advertencia", "No hay ninguna fila seleccionada para eliminar.")
            return False

        combo_matricula = self.tabla_area.cellWidget(row, 0)
        if combo_matricula is None:
            QMessageBox.warning(self, "Advertencia", "No se encontró la matrícula en la fila seleccionada.")
            return False

        # intentar obtener construccion_id almacenado en la propiedad (si existe)
        construccion_id = combo_matricula.property("construccion_id")
        inmueble_id = combo_matricula.currentData(role=Qt.ItemDataRole.UserRole)

        # Confirmación del usuario
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Desea eliminar la construcción seleccionada y todos sus croquis asociados?\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta != QMessageBox.StandardButton.Yes:
            return False

        db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
        try:
            db.conectar()

            # Ejecutar borrado en BD (si hay construccion_id)
            if construccion_id:
                # borrar construcción
                db.actualizar("DELETE FROM construcciones WHERE id = %s", (construccion_id,))
            else:
                
                # nada que borrar en BD
                pass

            db.cerrar_conexion()

            # Limpiar widgets de croquis en la UI
            self.limpiar_datos()

            # Quitar la fila de la tabla
            self.tabla_area.removeRow(row)

            QMessageBox.information(self, "Eliminado", "La construcción y sus croquis se eliminaron correctamente.")
            return True

        except Exception as e:
            try:
                db.cerrar_conexion()
            except Exception:
                pass
            QMessageBox.critical(self, "Error", f"Ocurrió un error al eliminar: {e}")
            print(f"Error al eliminar fila: {e}")
            return False

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

    def guardar_construccion(self, row, nueva_construccion=False):
        
        try:

            resultado, mensaje = self.validar_campos_construccion(row)
            if resultado == False:
                QMessageBox.warning(self, "Advertencia", mensaje)
                return

             # Conectar a la base de datos
            print("Guardando construcción para la fila:", row)
            db = DB(host="localhost", database=self.basededatos, user="postgres", password="ironmaiden")
            db.conectar()
        
            # Obtén los datos de la fila
            combo_matricula = self.tabla_area.cellWidget(row, 0)
            combo_tipo_construccion = self.tabla_area.cellWidget(row, 1)
            area_item = self.tabla_area.item(row, 2)
            combo_uso = self.tabla_area.cellWidget(row, 3)
            dependencias_item = self.tabla_area.item(row, 4)

            # Obtiene el id del inmueble seleccionado
            construccion_id = combo_matricula.property("construccion_id")  # O el valor real del id según tu lógica
            inmueble_id = combo_matricula.currentData(role=Qt.ItemDataRole.UserRole)  # Obtener el id del inmueble desde el combo
            print('construccion_id:', construccion_id)
    
            # Verificar si ya existe una construcción para este inmueble con este id
            
            existe_construccion = db.consultar("SELECT id FROM construcciones WHERE id = %s", (construccion_id,))
            
            print("existe_construccion:", existe_construccion, self.editando_fila)
            if len(existe_construccion) > 0 and self.editando_fila == False:
                print("Ya existe una construcción para este inmueble.")
                print("Construcción ID seleccionado:", construccion_id)
                # Actualizar los datos de la construcción existente
                query_update = """
                    UPDATE construcciones
                    SET num_pisos = %s, num_sotanos = %s, vetustez = %s, vida_util = %s, vida_restante = %s, tipo_construccion = %s, uso = %s, area = %s, dependencias = %s, cimentacion = %s, estructura = %s, muros = %s, cubierta = %s, fachada = %s, cielo_raso = %s, estructura_estado = %s, acabados_estado = %s
                    WHERE id = %s
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
                    construccion_id
                )
                print("Actualizando construcción:", (query_update, datos_update))
                db.actualizar(query_update, datos_update)
            
            else:
                print("No existe una construcción para este inmueble.")
                print("Guardando construccion para inmueble ID seleccionado:", inmueble_id)

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

                construccion_id = db.insertar(query_construccion, datos)
                self.editando_fila = False
                combo_matricula.setProperty("construccion_id", construccion_id)

            # Guardar croquis asociados
            for i in range(self.croquis_container.count()):
                widget = self.croquis_container.itemAt(i).widget()

                id_imagen = widget.property("id_imagen") if widget else None
                print("id_imagen croquis:", id_imagen)
                if widget:

                    # Obtener qlineedit y qlabel de la imagen
                    label = widget.findChild(QLabel)
                    descripcion = widget.findChild(QLineEdit)

                    #obtener texto descripcion y path imagen
                    texto_descripcion = descripcion.text() if descripcion else ""
                    path_imagen = widget.property("path_imagen") if label else None

                    existe_imagen = db.consultar("SELECT id FROM croquis_construccion WHERE id = %s", (id_imagen,))
                    print("existe_imagen:", existe_imagen)
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
                        print("Insertando croquis:", (query_croquis, (construccion_id, path_imagen, texto_descripcion)))
                        db.insertar(query_croquis, (construccion_id, path_imagen, texto_descripcion))
            #self.cargar_datos_construccion()
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
            WHERE i.avaluo_id =  %s ORDER BY c.id ASC
        """
        construcciones = db.consultar(query, (self.id_avaluo,))
        print("Construcciones encontradas:", len(construcciones))
        self.tabla_area.setRowCount(0)
        self.fila_anterior = len(construcciones) -1 if len(construcciones) >0 else 0

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
            # Guardar id de la construcción y todos los datos como propiedades para uso posterior
            print('row_data[0]:', row_data[0])
            combo_matricula.setProperty("construccion_id", row_data[0])
            combo_matricula.setProperty("construccion_data", row_data)
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
            croquis_query = "SELECT imagen_path, descripcion, id FROM croquis_construccion WHERE construccion_id = %s"
            croquis = db.consultar(croquis_query, (row_data[0],))
            # Primero limpiar contenedor de croquis
            while self.croquis_container.count() > 0:
                item = self.croquis_container.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)
            for imagen_path, descripcion, id in croquis:
                FuncionesImagenes.agregar_imagen(self, self.croquis_container, imagen_path, descripcion, id, "croquis_construccion")
        self.tabla_area.selectRow(self.fila_anterior); self.tabla_area.setCurrentCell(self.fila_anterior, 4)
        db.cerrar_conexion()

    def limpiar_datos(self):

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

    def on_tab_changed(self, tab_panel, index):
        print("Pestaña cambiada a index:", index, "nombre:", tab_panel.tabText(index))
        if tab_panel.tabText(index) == "Características de Construcción":
            print("Cambiando a pestaña de características de construcción.")
            current_row = self.tabla_area.currentRow()

            datos_comparacion = self.obtener_actuales(self.fila_anterior)

            # comparar datos para evaluar si hay cambios sin guardar
        
            if self.datos_actuales:
                for key in datos_comparacion:
                    if key in self.datos_actuales:
                        if datos_comparacion[key] != self.datos_actuales[key]:
                            
                            """
                            Muestra un QMessageBox preguntando si guardar o descartar los cambios.
                            Retorna: "guardar", "descartar" o "cancelar"
                            """
                            msg = QMessageBox(self)
                            msg.setWindowTitle("Guardar cambios")
                            msg.setText("Se han detectado cambios en la construcción. ¿Desea guardar los cambios actuales o descartarlos?")
                            msg.setIcon(QMessageBox.Icon.Question)

                            btn_guardar = msg.addButton("Guardar", QMessageBox.ButtonRole.AcceptRole)
                            btn_descartar = msg.addButton("Descartar", QMessageBox.ButtonRole.DestructiveRole)

                            msg.setDefaultButton(btn_guardar)
                            msg.exec()

                            clicked = msg.clickedButton()
                            if clicked == btn_guardar:
                                self.guardar_construccion(self.fila_anterior)
                            self.datos_actuales = self.obtener_actuales(self.fila_anterior)

                                

import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import ( QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QMessageBox, QProgressBar,
                             QTabWidget, QTextEdit, 
                             QGroupBox, QComboBox,QScrollArea,QGridLayout,
                             QSizePolicy, QCheckBox, QDoubleSpinBox, QHBoxLayout)
from PyQt6.QtCore import Qt, QTimer, QDate

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QFileInfo, Qt
from PyQt6.QtGui import QPixmap
from num2words import num2words
from Estilos import Estilos
from Funciones_imagenes import FuncionesImagenes
from DB import DB

class PestanaCondicionesValuacion(QWidget):
    def __init__(self, tab_panel: QTabWidget, id_avaluo=None, ventana_principal=None):
        super().__init__()

        self.id_avaluo = id_avaluo
        self.basededatos = "seshat"  # Nombre de la base de
        self.id_valuacion = None  # Inicializar id_valoracion
        self.ventana_principal = ventana_principal
        
        # Aplicar estilos desde el archivo CSS
        self.group_style = Estilos.cargar_estilos(self, "styles.css")
        
        # Crear el widget principal de la pestaña
        pestana = QWidget()
        
        # Crear scroll area para toda la pestaña
        scroll_area = QScrollArea(pestana)   
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        scroll_area.setStyleSheet(self.group_style)  # Aplicar estilos al scroll area
        
        # Crear el widget interno que contendrá los elementos
        contenido = QWidget()
        scroll_area.setWidget(contenido)
        
        # Layout principal vertical para el contenido        
        layout_principal = QGridLayout(contenido)
        layout_principal.setContentsMargins(10, 10, 10, 10)
        layout_principal.setSpacing(15)
        
        # Configurar el mismo ancho para todas las columnas
        columnas = 2  # Número de columnas en el layout
        for i in range(columnas):
            layout_principal.setColumnStretch(i, 1)  # Asignar la misma proporción de expansión
        
        # Configurar política de tamaño
        contenido.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.MinimumExpanding
        )
        
        """ # Crear un layout principal en forma de grid para dividir en dos columnas
        layout_principal = QGridLayout(contenido)   """ 
    
        # 1. Condiciones restrictivas y afectaciones
        grupo_condiciones_restrictivas = QGroupBox("Condiciones restrictivas y afectaciones")
        layout_condiciones_restrictivas = QGridLayout(grupo_condiciones_restrictivas)
        self.problemas_estabilidad = QLineEdit()
        self.impacto_ambiental = QLineEdit()
        self.seguridad = QLineEdit()
    
        layout_condiciones_restrictivas.addWidget(QLabel("Problemas de estabilidad y suelos:"), 0, 0)
        layout_condiciones_restrictivas.addWidget(self.problemas_estabilidad, 0, 1)

        layout_condiciones_restrictivas.addWidget(QLabel("Impacto ambiental y condiciones de salubridad:"), 1, 0)
        layout_condiciones_restrictivas.addWidget(self.impacto_ambiental, 1, 1)

        layout_condiciones_restrictivas.addWidget(QLabel("Seguridad:"), 2, 0)
        layout_condiciones_restrictivas.addWidget(self.seguridad, 2, 1)

        layout_principal.addWidget(grupo_condiciones_restrictivas, 0, 0)
    
        # 2. Condiciones generales
        grupo_condiciones_generales = QGroupBox("Condiciones generales")
        layout_condiciones_generales = QVBoxLayout(grupo_condiciones_generales)
    
        layout_condiciones_generales.addWidget(QLabel("Agregar condiciones:"))
        boton_agregar_condicion = QPushButton("Agregar condición")
        layout_condiciones_generales.addWidget(boton_agregar_condicion)
    
        # Espacio para agregar múltiples condiciones
        self.lista_condiciones = QVBoxLayout()
        layout_condiciones_generales.addLayout(self.lista_condiciones)

        boton_agregar_condicion.clicked.connect(self.agregar_condicion)
    
        layout_principal.addWidget(grupo_condiciones_generales,0,1)
    
        # 3. Aspecto económico
        grupo_aspecto_economico = QGroupBox("Aspecto económico")
        layout_aspecto_economico = QGridLayout(grupo_aspecto_economico)
    
        layout_aspecto_economico.addWidget(QLabel("Metodologías valuatorias empleadas:"), 0, 0)
        self.layout_metodologias = QVBoxLayout()
        metodologias = [
            "Método de comparación o mercado",
            "Método de capitalización de rentas o ingresos",
            "Método de costo de reposición",
            "Método residual"
        ]
        for metodologia in metodologias:
            self.layout_metodologias.addWidget(QCheckBox(metodologia))
        layout_aspecto_economico.addLayout(self.layout_metodologias, 0, 1)

        self.justificacion_metodologias = QTextEdit()
    
        layout_aspecto_economico.addWidget(QLabel("Justificación de las metodologías:"), 1, 0)
        layout_aspecto_economico.addWidget(self.justificacion_metodologias, 1, 1)

        layout_aspecto_economico.addWidget(QLabel("Perspectivas de valorización:"), 2, 0)
        self.combo_valorizacion = QComboBox()
        self.combo_valorizacion.addItems(["Bajas", "Normales", "Altas"])
        layout_aspecto_economico.addWidget(self.combo_valorizacion, 2, 1)
    
        layout_principal.addWidget(grupo_aspecto_economico,1,0)
    
        # 4. Valuación
        grupo_valuacion = QGroupBox("Valuación")
        layout_valuacion = QGridLayout(grupo_valuacion)
    
        layout_valuacion.addWidget(QLabel("Cuadro de liquidación (imágenes):"), 0, 0)
        boton_agregar_imagen = QPushButton("Agregar imagen")
        layout_valuacion.addWidget(boton_agregar_imagen, 0, 1)
        
    
        self.lista_imagenes = QVBoxLayout()
        
        layout_valuacion.addLayout(self.lista_imagenes, 1, 0, 1, 2)
        boton_agregar_imagen.clicked.connect(lambda:FuncionesImagenes.agregar_imagen(self, self.lista_imagenes))
        
        # Contenedor para imágenes y descripciones
        self.valuation_container = QVBoxLayout()
        
        
        layout_valuacion.addWidget(QLabel("Valor adoptado:"), 2, 0)
        self.valor_adoptado = QDoubleSpinBox()
        self.valor_adoptado.setRange(0, 1000000000000)  # Rango de 0 a 1 billón
        self.valor_adoptado.setDecimals(0)  # Sin decimales
        layout_valuacion.addWidget(self.valor_adoptado, 2, 1)

        layout_valuacion.addWidget(QLabel("Valor en letras:"), 3, 0)
        self.valor_en_letras = QLineEdit()
        self.valor_en_letras.setReadOnly(True)
        layout_valuacion.addWidget(self.valor_en_letras, 4, 0, 4, 2)

        def convertir_a_letras():
            valor = self.valor_adoptado.value()
            complemento = " PESOS"
            if valor%1000000 == 0:
                complemento = " DE PESOS"

            self.valor_en_letras.setText(num2words(valor, lang="es").upper() + complemento)

        self.valor_adoptado.valueChanged.connect(convertir_a_letras)
    
        layout_principal.addWidget(grupo_valuacion,1,1)
        
        pestana_layout = QVBoxLayout(pestana)
        pestana_layout.addWidget(scroll_area)
        pestana_layout.setContentsMargins(0, 0, 0, 0)
        
        """ # Configurar el scroll area
        scroll_area.setWidget(contenido)  """   
    
        # Agregar la pestaña al panel
        pestana.mi_pestana = self
        
        tab_panel.addTab(pestana, "Condiciones generales y Valoración")
        self.cargar_datos(self.id_avaluo)
    
    def agregar_condicion(self, texto="", id_condicion=None):
            contenedor_condicion = QWidget()
            layout_condicion = QHBoxLayout(contenedor_condicion)
            campo_condicion = QLineEdit()
            if texto:
                campo_condicion.setText(texto)
                campo_condicion.setProperty("id_condicion", id_condicion)
            btn_eliminar = QPushButton("×")
            btn_eliminar.setObjectName("botonEliminar")
            btn_eliminar.setStyleSheet(self.group_style)
            btn_eliminar.clicked.connect(lambda: self.eliminar_condicion(campo_condicion))
            layout_condicion.addWidget(campo_condicion)
            layout_condicion.addWidget(btn_eliminar)
            self.lista_condiciones.addWidget(contenedor_condicion)

    def eliminar_condicion(self, campo_condicion):
        # Buscar el contenedor padre del QLineEdit
        contenedor = campo_condicion.parentWidget()
        if contenedor:
            # Eliminar el contenedor del layout de condiciones
            self.lista_condiciones.removeWidget(contenedor)
            contenedor.deleteLater()  # Eliminar el widget de forma segura
            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()
            id_condicion = campo_condicion.property("id_condicion")
            if id_condicion:
                db.eliminar("DELETE FROM condiciones WHERE id = %s", (id_condicion,))
            db.cerrar_conexion()

    def validar_campos_valoracion(self, avaluo_id=None, require_images=False):
        """
        Valida que los campos obligatorios de la pestaña 'Condiciones y Valoración' estén diligenciados.
        Parámetros:
          avaluo_id (int|None): id del avaluo. Si no se provee, intenta usar self.avaluo_id si existe.
          require_images (bool): si True exige al menos 1 imagen en el cuadro de valuación.
        Retorna:
          (True, "") si todo está bien, o (False, "mensaje") si falta algo.
        """
        # Helper: buscar groupbox por título (igual que en guardar_toda_valoracion)
        def buscar_groupbox_por_titulo(titulo):
            for gb in self.findChildren(QGroupBox):
                try:
                    if gb.title().strip() == titulo:
                        return gb
                except Exception:
                    continue
            return None
    
        # 2) Condiciones restrictivas: problemas, impacto, seguridad
        grupo_restrictivas = buscar_groupbox_por_titulo("Condiciones restrictivas y afectaciones")
        if not grupo_restrictivas:
            return False, "No se encontró el grupo 'Condiciones restrictivas y afectaciones' en la interfaz."
    
        lineeds = grupo_restrictivas.findChildren(QLineEdit)
        # esperamos al menos 3 QLineEdit según diseño: problemas, impacto, seguridad
        textos = [le.text().strip() for le in lineeds]
        if len(textos) < 3:
            return False, "Faltan campos en 'Condiciones restrictivas y afectaciones'."
        problemas = textos[0]
        impacto = textos[1]
        seguridad = textos[2]
        if not problemas:
            return False, "Ingrese los problemas de estabilidad y suelos."
        if not impacto:
            return False, "Ingrese el impacto ambiental y condiciones de salubridad."
        if not seguridad:
            return False, "Ingrese la información de seguridad."
    
        # 3) Condiciones generales: al menos 1 condición (si tu flujo las permite vacías, ajusta aquí)
        grupo_cond_gen = buscar_groupbox_por_titulo("Condiciones generales")
        if not grupo_cond_gen:
            return False, "No se encontró el grupo 'Condiciones generales' en la interfaz."
        condiciones = []
        # recogemos QLineEdit hijos que representen condiciones
        for le in grupo_cond_gen.findChildren(QLineEdit):
            v = le.text().strip()
            if v:
                condiciones.append(v)
        if len(condiciones) == 0:
            return False, "Agregue al menos una condición en 'Condiciones generales'."
    
        # 4) Aspecto económico: al menos una metodología seleccionada, justificación y perspectiva
        grupo_aspecto = buscar_groupbox_por_titulo("Aspecto económico")
        if not grupo_aspecto:
            return False, "No se encontró el grupo 'Aspecto económico' en la interfaz."
    
        # comprobar checkboxes (hay 4 metodologías)
        metodologias_checks = grupo_aspecto.findChildren(QCheckBox)
        any_checked = any(cb.isChecked() for cb in metodologias_checks) if metodologias_checks else False
        if not any_checked:
            return False, "Seleccione al menos una metodología valuatoria en 'Aspecto económico'."
    
        # justificación (QTextEdit) no vacía
        te = grupo_aspecto.findChild(QTextEdit)
        justificacion = te.toPlainText().strip() if te else ""
        if not justificacion:
            return False, "Ingrese la justificación de las metodologías empleadas."
    
        # perspectiva de valorización (QComboBox) no vacía
        cb_val = grupo_aspecto.findChild(QComboBox)
        if not cb_val or not cb_val.currentText().strip():
            return False, "Seleccione la perspectiva de valorización."
    
        # 5) Valuación: valor adoptado > 0 y valor_en_letras no vacío
        grupo_valuacion = buscar_groupbox_por_titulo("Valuación")
        if not grupo_valuacion:
            return False, "No se encontró el grupo 'Valuación' en la interfaz."
    
        sb = grupo_valuacion.findChild(QDoubleSpinBox)
        valor_adoptado = sb.value() if sb else 0
        if valor_adoptado is None or float(valor_adoptado) <= 0:
            return False, "Ingrese un 'Valor adoptado' mayor que cero."
    
        # valor en letras (QLineEdit readonly)
        valor_en_letras = ""
        for le in grupo_valuacion.findChildren(QLineEdit):
            if le.isReadOnly():
                valor_en_letras = le.text().strip()
                break
        if not valor_en_letras:
            return False, "El campo 'Valor en letras' está vacío. Asegúrese de que el valor adoptrado se haya convertido a letras."
    
        # 6) Imágenes del cuadro de valuación (opcional según parámetro)
        if require_images:
            # intentamos usar self.valuation_container como en guardar_toda_valoracion
            imagenes = []
            if hasattr(self, 'valuation_container'):
                layout = getattr(self, 'valuation_container')
                # recorrer layout para contar imágenes
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if not item:
                        continue
                    w = item.widget()
                    if not w:
                        continue
                    label = w.findChild(QLabel)
                    if label:
                        try:
                            path = label.property("path_imagen")
                        except Exception:
                            path = None
                        if path:
                            imagenes.append(path)
            if len(imagenes) == 0:
                return False, "Agregue al menos una imagen en el 'Cuadro de liquidación' (Valuación)."
    
        # Si llegamos aquí todo pasó
        return True, ""
    
    def on_tab_changed(self, tab_panel, index):
            """
            Maneja el evento de cambio de pestaña en el QTabWidget.
            Si la pestaña activa es "Datos de la valoracion", recarga los datos de la solicitud.

            :param tab_panel: El QTabWidget que contiene las pestañas.
            :param index: El índice de la pestaña actualmente activa.
            """
            print(f"Pestaña cambiada a índice: {index}, Título: {tab_panel.tabText(index)}")
            if tab_panel.tabText(index) == "Condiciones generales y Valoración":

                if self.id_avaluo != "":
                    self.guardar_datos()

    def guardar_datos(self):
        # Aquí se implementaría la lógica para guardar los datos ingresados en la pestaña
        try:
            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()

            valores_checkboxes = {cb.text(): cb.isChecked() for cb in self.layout_metodologias.parentWidget().findChildren(QCheckBox)}            

            if self.id_valuacion is None:
                query_insert = """
                    INSERT INTO valoracion (
                    avaluo_id,
                    problemas,
                    impacto_ambiental,
                    seguridad,
                    comparacion_mercado,
                    rentas,
                    reposicion,
                    residual,
                    justificacion_metodologias,
                    valorizacion,
                    valor_adoptado,
                    valor_en_letras
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_valoracion
                """
                
                self.id_valuacion = db.insertar(query_insert, (
                    self.id_avaluo,
                    self.problemas_estabilidad.text(),
                    self.impacto_ambiental.text(),
                    self.seguridad.text(),
                    valores_checkboxes["Método de comparación o mercado"],
                    valores_checkboxes["Método de capitalización de rentas o ingresos"],
                    valores_checkboxes["Método de costo de reposición"],
                    valores_checkboxes["Método residual"],
                    self.justificacion_metodologias.toPlainText(),
                    self.combo_valorizacion.currentText(),
                    self.valor_adoptado.value(),
                    self.valor_en_letras.text()
                    # Otros campos aquí...
                ))
                
            else:
                query_update = """
                    UPDATE valoracion
                    SET
                    problemas = %s,
                    impacto_ambiental = %s,
                    seguridad = %s,
                    comparacion_mercado = %s,
                    rentas = %s,
                    reposicion = %s,
                    residual = %s,
                    justificacion_metodologias = %s,
                    valorizacion = %s,
                    valor_adoptado = %s,
                    valor_en_letras = %s,
                    updated_at = NOW()
                    WHERE id_valoracion = %s
                    ;
                """
                valores_update = (
                    self.problemas_estabilidad.text(),
                    self.impacto_ambiental.text(),
                    self.seguridad.text(),
                    valores_checkboxes["Método de comparación o mercado"],  
                    valores_checkboxes["Método de capitalización de rentas o ingresos"],
                    valores_checkboxes["Método de costo de reposición"],
                    valores_checkboxes["Método residual"],
                    self.justificacion_metodologias.toPlainText(),
                    self.combo_valorizacion.currentText(),
                    self.valor_adoptado.value(),
                    self.valor_en_letras.text(),
                    self.id_valuacion
                )
                

                db.actualizar(query_update, valores_update)
            

            # Agrega las condiciones de forma dinamica

            for i in range(self.lista_condiciones.count()):
                item = self.lista_condiciones.itemAt(i)
                if not item:
                    continue
                widget = item.widget()
                
                # buscar el QLineEdit dentro del widget contenedor
                le = widget.findChild(QLineEdit)
                if le and isinstance(le, QLineEdit):
                    text = le.text().strip()
                    if text:
                        
                        resultado = le.property("id_condicion")
                        
                        

                        if resultado:                           
                            query_update_condicion = """
                                UPDATE condiciones
                                SET condicion = %s
                                WHERE id = %s
                            """
                            db.actualizar(query_update_condicion, (text, resultado))
                        else:
                            query_insert_condicion = """
                                INSERT INTO condiciones (valoracion_id, condicion)
                                VALUES (%s, %s) RETURNING id;
                            """ 
                            id_condicion = db.insertar(query_insert_condicion, (self.id_valuacion, text))
                            le.setProperty("id_condicion", id_condicion)

            # Insertar en imangenes del cuadro de valuación
            
            
            for i in range(self.lista_imagenes.count()):
                # Obtener el contenedor en la posición actual
                contenedor = self.lista_imagenes.itemAt(i).widget()
                id_imagen = contenedor.property("id_imagen") if contenedor else None
                

                if contenedor:
                    # Obtener el QLabel y el QLineEdit dentro del contenedor
                    label = contenedor.findChild(QLabel)
                    line_edit = contenedor.findChild(QLineEdit)
                    
                    
                    # Obtener el texto del QLineEdit
                    texto_descripcion = line_edit.text() if line_edit else "Sin descripción"
                    
                    # Obtener el path de la propiedad del label
                    path_imagen = contenedor.property("path_imagen") if contenedor else "Sin imagen"
                    
                    
                    if id_imagen:

                        query_usos = """
                        UPDATE cuadro_valuacion
                        SET descripcion = %s, imagen_path = %s
                        WHERE id_cuadro = %s
                        """
                        
                        
                        db.actualizar(query_usos, (texto_descripcion, path_imagen,id_imagen))


                    else:
                        query_usos = """
                        INSERT INTO cuadro_valuacion (valoracion_id, descripcion, imagen_path)
                        VALUES (%s, %s, %s) RETURNING id_cuadro;
                        """
                        
                        
                        id_imagen = db.insertar(query_usos, (self.id_valuacion, texto_descripcion, path_imagen))

                        contenedor.setProperty("id_imagen", id_imagen)
            
            db.cerrar_conexion()
        except Exception as e:
            db.rollback()
            db.cerrar_conexion()
            print(f"Error al guardar los datos: {e}")

    def cargar_datos(self, avaluo_id=None):
        """
        Carga desde la base de datos los datos de `valoracion`, sus `condiciones` y el
        `cuadro_valuacion` asociado al `avaluo_id` (o a `self.id_avaluo` si no se pasa).
        Llena los widgets de la pestaña con los valores encontrados.
        """
        aid = avaluo_id if avaluo_id is not None else self.id_avaluo
        if not aid:
            return False, "No hay avaluo_id para cargar datos"

        try:
            db = self.ventana_principal.obtener_conexion_db()
            db.conectar()

            # 1) Cargar fila de valoracion
            q_val = (
                "SELECT id_valoracion, problemas, impacto_ambiental, seguridad, "
                "comparacion_mercado, rentas, reposicion, residual, justificacion_metodologias, "
                "valorizacion, valor_adoptado, valor_en_letras "
                "FROM valoracion WHERE avaluo_id = %s LIMIT 1"
            )
            row = db.consultar(q_val, (self.id_avaluo,))

            if row:
                # db.consultar puede devolver lista de tuplas
                r = row[0] if isinstance(row, (list, tuple)) and len(row) > 0 else row

                # si r es tupla con columnas en orden
                self.id_valuacion = r[0]
                self.problemas_estabilidad.setText(str(r[1] or ""))
                self.impacto_ambiental.setText(str(r[2] or ""))
                self.seguridad.setText(str(r[3] or ""))

                # valores de metodologias (asumimos booleanos en columnas 4..7)
                metod_vals = {
                    "Método de comparación o mercado": bool(r[4]) if len(r) > 4 else False,
                    "Método de capitalización de rentas o ingresos": bool(r[5]) if len(r) > 5 else False,
                    "Método de costo de reposición": bool(r[6]) if len(r) > 6 else False,
                    "Método residual": bool(r[7]) if len(r) > 7 else False,
                }
                # localizar checkboxes por texto y aplicar
                for cb in self.layout_metodologias.parentWidget().findChildren(QCheckBox):
                    text = cb.text()
                    if text in metod_vals:
                        cb.setChecked(metod_vals[text])

                # justificacion, valorizacion, valor_adoptado, valor_en_letras
                self.justificacion_metodologias.setPlainText(str(r[8] or "") if len(r) > 8 else "")

                if len(r) > 9:
                    try:
                        self.combo_valorizacion.setCurrentText(str(r[9] or ""))
                    except Exception:
                        pass
                if len(r) > 10:
                    try:
                        self.valor_adoptado.setValue(float(r[10] or 0))
                    except Exception:
                        pass
                if len(r) > 11:
                    try:
                        self.valor_en_letras.setText(str(r[11] or ""))
                    except Exception:
                        pass
            else:
                # No hay valoración creada todavía
                print("No se encontró valoración para avaluo_id:", self.id_avaluo)

            # 2) Cargar condiciones (tabla condiciones)
            # limpiar layout de condiciones actuales
            def clear_layout(lay):
                # elimina widgets hijos de un QLayout
                for i in reversed(range(lay.count())):
                    item = lay.itemAt(i)
                    if item is None:
                        continue
                    w = item.widget()
                    if w is not None:
                        w.setParent(None)
                    else:
                        # si es layout anidado
                        sub = item.layout()
                        if sub is not None:
                            clear_layout(sub)

            clear_layout(self.lista_condiciones)

            if self.id_valuacion:
                conds = db.consultar("SELECT id, condicion FROM condiciones WHERE valoracion_id = %s ORDER BY id", (self.id_valuacion,))
                if conds:
                    for c in conds:
                        id_cond = c[0]
                        texto = c[1] if len(c) > 1 else ""
                        self.agregar_condicion(texto, id_condicion=id_cond)

            # 3) Cargar cuadro_valuacion (imagenes y descripciones)
            clear_layout(self.lista_imagenes)
            if self.id_valuacion:
                usos = db.consultar("SELECT id_cuadro, descripcion, imagen_path FROM cuadro_valuacion WHERE valoracion_id = %s ORDER BY id_cuadro", (self.id_valuacion,))
                
                if usos:
                    for u in usos:
                        id_cuadro = u[0]
                        descripcion = u[1] if len(u) > 1 else ""
                        path = u[2] if len(u) > 2 else None
                        
                        FuncionesImagenes.agregar_imagen(self, self.lista_imagenes, path, descripcion, id_cuadro, "cuadro_valuacion")

            db.cerrar_conexion()
            return True, "ok"

        except Exception as e:
            try:
                db.rollback()
                db.cerrar_conexion()
            except Exception:
                pass
            return False, str(e)
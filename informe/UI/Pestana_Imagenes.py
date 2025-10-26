from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QScrollArea
)
from PyQt6.QtGui import (QPixmap,QTransform)
from PyQt6.QtCore import Qt
from Estilos import Estilos
from DB import DB

class PestañaImagenes(QWidget):
    def __init__(self, id_avaluo):
        super().__init__()
        
        self.id_avaluo = id_avaluo
        self.layout_principal = QVBoxLayout(self)
        
        self.group_style = Estilos.cargar_estilos(self, "styles.css")
        
        # Crear un área de desplazamiento
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(self.group_style)  # Aplicar estilos al scroll area
        self.layout_principal.addWidget(self.scroll_area)
        
        # Contenedor interno para el contenido desplazable
        self.contenedor_scroll = QWidget()
        self.scroll_area.setWidget(self.contenedor_scroll)
        
        # Layout para el contenedor interno
        self.layout_scroll = QVBoxLayout(self.contenedor_scroll)
        
        # Lista para almacenar información de las imágenes
        self.lista_imagenes = []
        
        # Layout para organizar las imágenes en dos columnas
        self.grid_layout = QGridLayout()
        self.layout_scroll.addLayout(self.grid_layout)
        
        # Botón para cargar múltiples imágenes
        btn_cargar_imagenes = QPushButton("Cargar Imágenes")
        btn_cargar_imagenes.setStyleSheet(self.group_style)
        btn_cargar_imagenes.clicked.connect(self.cargar_imagenes)
        self.layout_principal.addWidget(btn_cargar_imagenes)

        #Cargar imagenes desde la base de datos
        self.cargar_imagenes_desde_db(self.id_avaluo)
    
    def cargar_imagenes(self):
        # Abrir cuadro de diálogo para seleccionar múltiples imágenes
        rutas_imagenes, _ = QFileDialog.getOpenFileNames(
            self, 
            "Seleccionar Imágenes", 
            "./Resultados/Imagenes", 
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        for ruta in rutas_imagenes:
            self.agregar_imagen(ruta)
    
    def agregar_imagen(self, ruta_imagen, datos_imagen=None):
        # Crear un contenedor para la imagen y sus controles
        contenedor = QWidget()
        layout_contenedor = QVBoxLayout(contenedor)
        
        # Mostrar la imagen
        label_imagen = QLabel()
        pixmap = QPixmap(ruta_imagen)
        
        self.imagen_width = label_imagen.width  # Ancho fijo para la vista previa
        self.imagen_height = label_imagen.height  # Alto fijo para la vista previa      
        
        label_imagen.setPixmap(pixmap.scaled(self.imagen_width(), self.imagen_height(), Qt.AspectRatioMode.KeepAspectRatio))
        layout_contenedor.addWidget(label_imagen, alignment=Qt.AlignmentFlag.AlignCenter)

        # Campo de texto con el nombre del archivo
        nombre_archivo = QLineEdit()

        nombre_archivo.setText(datos_imagen["nombre"] if datos_imagen else ruta_imagen.split("/")[-1])

        layout_contenedor.addWidget(nombre_archivo)
        
        # Botón para rotar la imagen
        btn_rotar = QPushButton("Rotar 90°")
        layout_contenedor.addWidget(btn_rotar)
        
        # Botón para eliminar la imagen
        btn_eliminar = QPushButton("Eliminar")
        layout_contenedor.addWidget(btn_eliminar)
        
        # Información inicial de la imagen
        numero_imagen = len(self.lista_imagenes) + 1
        rotacion = 0
        ancho = pixmap.width()
        alto = pixmap.height()
        print("Agregando imagen:" , ruta_imagen)
        self.lista_imagenes.append({
            "numero": numero_imagen,
            "ruta": ruta_imagen,
            "ancho": datos_imagen["ancho"] if datos_imagen else ancho,
            "alto": datos_imagen["alto"] if datos_imagen else alto,
            "rotacion": datos_imagen["rotacion"] if datos_imagen else rotacion
        })
        # Guardar propiedades útiles en el contenedor para facilitar lectura posterior
        contenedor.setProperty("ruta_imagen", ruta_imagen)
        contenedor.setProperty("numero_imagen", numero_imagen)
        contenedor.setProperty("rotacion", rotacion)
        contenedor.setProperty("ancho", ancho)
        contenedor.setProperty("alto", alto)

        contenedor.setProperty("id_imagen",   datos_imagen["id_imagen"] if datos_imagen else None)
        
        # Función para rotar la imagen
        def rotar_imagen():
            nonlocal rotacion
            rotacion = (rotacion + 90) % 360
            pixmap_rotado = pixmap.transformed(QTransform().rotate(rotacion))
            label_imagen.setPixmap(pixmap_rotado.scaled(self.imagen_width(), self.imagen_height(), Qt.AspectRatioMode.KeepAspectRatio))
            # Actualizar la lista
            for img in self.lista_imagenes:
                if img["ruta"] == ruta_imagen:
                    img["rotacion"] = rotacion
            # actualizar propiedad en el contenedor
            contenedor.setProperty("rotacion", rotacion)
        
        # Función para eliminar la imagen
        def eliminar_imagen():
            for i, img in enumerate(self.lista_imagenes):
                if img["ruta"] == ruta_imagen:
                    self.lista_imagenes.pop(i)
                    break
            # Eliminar el contenedor del layout
            for i in range(self.grid_layout.count()):
                widget = self.grid_layout.itemAt(i).widget()
                if widget == contenedor:

                    id_imagen = contenedor.property("id_imagen")

                    if id_imagen is not None:
                        db = DB(host="localhost", database="seshat", user="postgres", password="ironmaiden")
                        db.conectar()
                        query = "DELETE FROM imagenes_avaluo WHERE id_imagen = %s;"
                        db.actualizar(query, (id_imagen,))
                        db.cerrar_conexion()

                    self.grid_layout.removeWidget(widget)
                    widget.deleteLater()
                    
                    break
        
        btn_rotar.clicked.connect(rotar_imagen)
        btn_eliminar.clicked.connect(eliminar_imagen)
        
        # Agregar el contenedor al grid layout en dos columnas
        fila = self.grid_layout.count() // 2
        columna = self.grid_layout.count() % 2
        self.grid_layout.addWidget(contenedor, fila, columna)

    def guardar_imagenes(self, table_name='imagenes_avaluo'):
        """
        Recorre `self.grid_layout` y recopila metadatos de cada imagen mostrada.


        Retorna:
          (True, lista) con la lista de diccionarios si todo salió bien, o
          (False, mensaje) en caso de error.
        """
        imagenes = []
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item is None:
                continue
            cont = item.widget()
            if cont is None:
                continue

            # Intentar leer propiedades guardadas
            ruta = cont.property("ruta_imagen") if cont.property("ruta_imagen") is not None else None
            numero = cont.property("numero_imagen") if cont.property("numero_imagen") is not None else None
            rotacion = cont.property("rotacion") if cont.property("rotacion") is not None else 0
            id_imagen = cont.property("id_imagen") if cont.property("id_imagen") else None
            ancho = cont.property("ancho") if cont.property("ancho") is not None else 0
            alto = cont.property("alto") if cont.property("alto") is not None else 0

            # intentar obtener el QLineEdit (nombre/descripcion)
            le = cont.findChild(QLineEdit)
            nombre = le.text().strip() if le is not None else None

            try:
                from DB import DB
                db = DB(host="localhost", database="seshat", user="postgres", password="ironmaiden")
                db.conectar()

                if id_imagen:
                    query = f"UPDATE {table_name} SET imagen_path=%s, nombre=%s, ancho=%s, alto=%s, rotacion=%s WHERE id_imagen=%s;"
                    params = (ruta, nombre, ancho, alto, rotacion, id_imagen)
                    db.actualizar(query, params)
                else:
            
                    query = f"INSERT INTO {table_name} (avaluo_id, imagen_path, nombre, ancho, alto, rotacion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_imagen;"
                    params = (self.id_avaluo, ruta, nombre, ancho, alto, rotacion)
                    new_id = db.insertar(query, params)
                    cont.setProperty("id_imagen", new_id)
                db.cerrar_conexion()
                
            except Exception as e:
                try:
                    db.rollback()
                    db.cerrar_conexion()
                except Exception:
                    pass
                return False, str(e)

    def cargar_imagenes_desde_db(self, avaluo_id=None):
        """
        Carga las imágenes asociadas a un `avaluo_id` desde la tabla `imagenes_avaluo`
        y las muestra en `self.grid_layout`. Si `avaluo_id` es None se usa
        `self.id_avaluo` si existe.
        """
        aid = avaluo_id if avaluo_id is not None else getattr(self, 'id_avaluo', None)
        print("Cargando imágenes para avaluo_id:", aid)
        if not aid:
            return False, "No hay avaluo_id para cargar imágenes"

        def clear_grid(grid):
            for i in reversed(range(grid.count())):
                item = grid.itemAt(i)
                if item is None:
                    continue
                w = item.widget()
                if w is not None:
                    grid.removeWidget(w)
                    w.setParent(None)
                    w.deleteLater()
                else:
                    sub = item.layout()
                    if sub is not None:
                        clear_grid(sub)

        try:
            
            db = DB(host="localhost", database="seshat", user="postgres", password="ironmaiden")
            db.conectar()

            clear_grid(self.grid_layout)
            self.lista_imagenes.clear()

            query = (
                "SELECT id_imagen, nombre, imagen_path, descripcion, ancho, alto, rotacion "
                "FROM imagenes_avaluo WHERE avaluo_id = %s ORDER BY id_imagen"
            )
            filas = db.consultar(query, (aid,))

            if not filas:
                db.cerrar_conexion()
                return True, []
            print(f"Se encontraron {len(filas)} imágenes para avaluo_id {aid}")
            print("comparando filas:", filas)
            for fila in filas:
                
                datos_imagen = {
                    "id_imagen": fila[0],
                    "nombre": fila[1] if len(fila) > 1 else None,
                    "path": fila[2] if len(fila) > 2 else None,
                    "descripcion": fila[3] if len(fila) > 3 else None,
                    "ancho": fila[4] if len(fila) > 4 else None,
                    "alto": fila[5] if len(fila) > 5 else None,
                    "rotacion": fila[6] if len(fila) > 6 else 0
                }
                
                self.agregar_imagen(datos_imagen["path"], datos_imagen)

            db.cerrar_conexion()
            return True, self.lista_imagenes

        except Exception as e:
            try:
                db.rollback()
                db.cerrar_conexion()
            except Exception:
                pass
            return False, str(e)

    def on_tab_changed(self, tab_panel, index):
        """
        Maneja el evento de cambio de pestaña en el QTabWidget.
        Si la pestaña activa es "Datos de la valoracion", recarga los datos de la solicitud.
        :param tab_panel: El QTabWidget que contiene las pestañas.
        :param index: El índice de la pestaña actualmente activa.
        """
        print(f"Pestaña cambiada a índice: {index}, Título: {tab_panel.tabText(index)}")
        print("comparando con 'Cargar Imágenes'", tab_panel.tabText(index) == "Cargar Imágenes")
        if tab_panel.tabText(index) == "Cargar Imágenes":
            if self.id_avaluo != "":
                self.guardar_imagenes()
# Agregar la pestaña al QTabWidget
def agregar_pestana_imagenes(tab_widget, id_avaluo):
    pestaña_imagenes = PestañaImagenes(id_avaluo)
    pestaña_imagenes.mi_pestana = pestaña_imagenes
    tab_widget.addTab(pestaña_imagenes, "Cargar Imágenes")
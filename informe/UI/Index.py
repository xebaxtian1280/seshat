import sys, os
import subprocess
import time
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QProgressBar,
                             QFileDialog, QMenuBar, QMenu, QTabWidget)
from PyQt6.QtCore import Qt, QTimer

# Importar las pestañas

from Pestana_Imagenes import agregar_pestana_imagenes
from Pestana_Datos_solicitud import PestanaDatosSolicitud
from Pestana_caracteristicas_sector import PestanaCaracteristicasSector
from Pestana_caracteristicas_construccion import PestanaCaracteristicasConstruccion
from Pestana_condiciones_valuacion import PestanaCondicionesValuacion
from Pestana_seguimiento import PestanaSeguimiento
from DB import DB

QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)


class ReportApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sistema de Gestión de Informes")
        #self.setMinimumSize(1000, 700)
        self.showMaximized()
        self.default_save_path = ""
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        # Configurar widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Barra de menú integrada en el panel
        menu_bar = QMenuBar()
        file_menu = QMenu("&Archivo", self)
        
        # Acciones del menú
        generar_action = file_menu.addAction("Generar Informe")
        generar_action.triggered.connect(self.iniciar_generacion)
        
        ubicacion_action = file_menu.addAction("Guardar Como")
        ubicacion_action.triggered.connect(self.seleccionar_ubicacion)
        
        crear_proyecto = file_menu.addAction("Crear Proyecto")
        crear_proyecto.triggered.connect(self.crea_proyecto)
        
        abrir_proyecto = file_menu.addAction("Abrir proyecto")
        abrir_proyecto.triggered.connect(self.carga_proyecto)
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Salir")
        exit_action.triggered.connect(self.close)
        
        menu_bar.addMenu(file_menu)
        main_layout.addWidget(menu_bar)
        
        # Panel de pestañas
        self.tab_panel = QTabWidget()
        
        # Crear las pestañas
        self.pestana_seguimiento = PestanaSeguimiento(self.tab_panel)
        
        # Conectar la señal de PestanaSeguimiento
        self.pestana_seguimiento.id_avaluo_seleccionado.connect(self.recibir_id_avaluo)
        
        
        # Crear pestañas
        #PestanaSeguimiento(self.tab_panel)
        """ PestanaDatosSolicitud(self.tab_panel)        
        PestanaCaracteristicasSector(self.tab_panel)
        PestanaCaracteristicasConstruccion(self.tab_panel)
        PestanaCondicionesValuacion(self.tab_panel)
        agregar_pestana_imagenes(self.tab_panel)  """      
        
        
        main_layout.addWidget(self.tab_panel)
        
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)
    
    def recibir_id_avaluo(self, id_avaluo):
        """
        Maneja el id_avaluo recibido desde PestanaSeguimiento.
        """
        print(f"ID Avaluo recibido en Index: {id_avaluo}")
        # Pasar el id_avaluo a la pestaña Datos de Solicitud
        self.id_avaluo = id_avaluo
    
    def seleccionar_ubicacion(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
    def crea_proyecto(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
            
    def carga_proyecto(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar ubicación de guardado",
            self.default_save_path
        )
        if directory:
            self.default_save_path = directory
            QMessageBox.information(self, "Ubicación actualizada", 
                                   f"Los informes se guardarán en:\n{self.default_save_path}")
    
    def iniciar_generacion(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_progreso)
        self.timer.start(100)
    
    def actualizar_progreso(self):
        current = self.progress_bar.value()
        if current < 100:
            self.progress_bar.setValue(current + 10)
        else:
            self.timer.stop()
            self.procesar_informe()
            self.progress_bar.hide()
    
    def procesar_informe(self):
        
        print("El id avaluo actual es:", getattr(self, 'id_avaluo', None))
        self.id_avaluo = getattr(self, 'id_avaluo', None)
        
        # Conectar a la base de datos
        db = DB(host="localhost", database="postgres", user="postgres", password="ironmaiden")
        db.conectar()
        
        
            
        
        
        # Recolectar datos de todas las pestañas
        success, resultado = False, "No se ha iniciado la generación del informe." 
        try:
                        
            print(f"Cargando datos para el avalúo con ID: {self.id_avaluo}")
    
            # Consulta SQL para obtener los datos de la solicitud
            consulta = """
            select a.nombre_cliente , a.id_cliente , a.destinatario, a.fecha_visita ,a.fecha_avaluo , a.tipo_avaluo, a.file_path
            FROM "Avaluos" a 
            left join inmuebles i on a."Avaluo_id" = i.avaluo_id 
            WHERE a."Avaluo_id" = 2
            """.replace("2", str(self.id_avaluo))
            
            resultado = db.consultar(consulta)
            
            if self.default_save_path == "" and resultado[0][6] == None:
                QMessageBox.warning(self, "Ubicación no seleccionada", 
                                    "Por favor, selecciona una ubicación para guardar el informe.")
                self.crea_proyecto()
                
            
            
            # Verificar si se encontraron datos
            
            if self.file_path == None and resultado[0][6] == None:
                
                self.file_path = f"{self.default_save_path}/informe_{time.strftime('%Y%m%d-%H%M%S')}.tex"
                print("Guardando en:", self.file_path)
                db.insertar(
                    """UPDATE "Avaluos" SET file_path = %s WHERE "Avaluo_id" = %s"""
                    , (self.file_path, str(self.id_avaluo)))
                print("Path guardado:", self.file_path)
                
            else:
                self.file_path = resultado[0][6]
                print("Ruta del archivo:", self.file_path)
                
            if resultado:       
                  
                success, resultado = self.generar_informe(resultado, "./Base/Informe.tex",self.file_path)             

            else:
                print(f"No se encontraron datos para el avalúo con ID: {self.id_avaluo}")
    
        except Exception as e:
            print(f"Error al cargar los datos de la solicitud: {e}")
        
        # Obtener todas las matrículas
        """ matriculas = []
        for i in range(self.matricula_layout.count()):
            item = self.matricula_layout.itemAt(i)
            if item and isinstance(item, QHBoxLayout):
                line_edit = item.itemAt(0).widget()
                if line_edit and line_edit.text():
                    matriculas.append(line_edit.text()) """

        db.cerrar_conexion()
        
        if success:
            QMessageBox.information(self, "Éxito", f"Informe guardado en:\n{resultado}")
        else:
            QMessageBox.critical(self, "Error", f"Error al generar informe:\n{resultado}")

    def generar_informe(self, texto, template_path="Base/Informe.tex", output_name="../Resultados/informe"):
        """
        Genera un informe LaTeX desde una plantilla y texto dinámico.
        
        Args:
            texto (str): Contenido a insertar
            template_path (str): Ruta de la plantilla .tex
            output_name (str): Nombre base del archivo de salida
        """
        
        # Leer plantilla
        print("template_path", output_name)

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                plantilla = f.read()
        except FileNotFoundError:
            print(f"Error: No se encontró {template_path}")
            return

        # Escapar caracteres especiales de LaTeX
        #texto_procesado = texto.replace("&", "\&").replace("%", "\%").replace("$", "\$")
        cliente= texto[0][0]
        documento_id=str(texto[0][1])
        destinatario=texto[0][2]
        fecha_visita=texto[0][3].date().strftime("%d/%m/%Y")
        fecha_informe=texto[0][4].date().strftime("%d/%m/%Y") 
        tipo_avaluo = texto[0][5]
        # Reemplazar marcadores en la plantilla
        informe_final = plantilla.replace("%CLIENTE%", cliente)
        informe_final = informe_final.replace("%DOCUMENTO_ID%", documento_id)
        informe_final = informe_final.replace("%DESTINATARIO%", destinatario)
        informe_final = informe_final.replace("FECHA_VISITA%", fecha_visita)
        informe_final = informe_final.replace("FECHA_INFORME%", fecha_informe)
        informe_final = informe_final.replace("%TIPO_AVALUO%", tipo_avaluo)       
        
        # Guardar archivo .tex
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(informe_final)
            print(f"Archivo .tex guardado en {output_name}")
            
        # Compilar el archivo .tex a PDF
        try:
            print(f"Compilando {output_name} a PDF...")
            subprocess.run(["pdflatex", output_name], check=True,cwd=os.path.dirname(os.path.abspath(output_name)))  # Establecer el directorio de trabajo)
            subprocess.run(["pdflatex", output_name], check=True,cwd=os.path.dirname(os.path.abspath(output_name)))  # Se ejecuta dos veces para referencias cruzadas)
            print(f"PDF generado correctamente: {output_name}.pdf")

            # Retornar el archivo PDF generado
            return True, f"{output_name}.pdf"
        except subprocess.CalledProcessError as e:
            print(f"Error al compilar el archivo .tex: {e}")
            return False, None
        except FileNotFoundError:
            print("Error: El comando 'pdflatex' no se encontró. Asegúrate de que está instalado y en el PATH.")
            return False, None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False, None
            
            
        
        # Compilar a PDF
        try:
            subprocess.run(["pdflatex", f"{output_name}.tex"], check=True)
            print(f"\nPDF generado: {output_name}.pdf")
            
            # Limpiar archivos auxiliares
            for ext in [".aux", ".log", ".out"]:
                archivo = f"{output_name}{ext}"
                if os.path.exists(archivo):
                    os.remove(archivo)
            
                 
        except FileNotFoundError:
            print("\n¡Error! Necesitas LaTeX instalado (pdflatex)")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportApp()
    window.show()
    sys.exit(app.exec())
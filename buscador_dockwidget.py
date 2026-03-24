from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (QDockWidget, QVBoxLayout, QWidget, QLabel, 
                             QComboBox, QLineEdit, QListWidget, QListWidgetItem, QPushButton)
from qgis.utils import iface
from qgis.core import QgsProject, QgsFeatureRequest

class BuscadorDinamicoDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Buscador de Registros - Cota & Valor", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Contenedor principal
        self.container = QWidget()
        self.layout = QVBoxLayout()
        
        # Selección de Capa
        self.layout.addWidget(QLabel("Selecciona la Capa:"))
        capa_row = QVBoxLayout()
        self.combo_capa = QComboBox()
        self.btn_refresh = QPushButton("Actualizar Capas")
        self.btn_refresh.clicked.connect(self.cargar_capas)
        self.layout.addWidget(self.combo_capa)
        self.layout.addWidget(self.btn_refresh)
        
        # Selección de Campo
        self.layout.addWidget(QLabel("Campo de búsqueda:"))
        self.combo_campo = QComboBox()
        self.layout.addWidget(self.combo_campo)
        
        # Input de Búsqueda
        self.layout.addWidget(QLabel("Buscar valor:"))
        self.txt_buscar = QLineEdit()
        self.txt_buscar.textChanged.connect(self.ejecutar_busqueda)
        self.layout.addWidget(self.txt_buscar)
        
        # Lista de Resultados
        self.lista_resultados = QListWidget()
        self.lista_resultados.itemClicked.connect(self.zoom_al_registro)
        self.layout.addWidget(self.lista_resultados)
        
        # Configuración final
        self.container.setLayout(self.layout)
        self.setWidget(self.container)
        
        # Eventos de actualización
        self.combo_capa.currentIndexChanged.connect(self.cargar_campos)
        
        # Escuchar cambios en el proyecto de QGIS
        QgsProject.instance().layersAdded.connect(self.cargar_capas)
        QgsProject.instance().layersRemoved.connect(self.cargar_capas)
        
        # Carga inicial
        self.cargar_capas()

    def cargar_capas(self, *args):
        self.combo_capa.clear()
        capas = [layer.name() for layer in QgsProject.instance().mapLayers().values() if layer.type() == 0]
        self.combo_capa.addItems(capas)
        if self.combo_capa.count() > 0:
            self.cargar_campos()

    def cargar_campos(self):
        self.combo_campo.clear()
        nombre_capa = self.combo_capa.currentText()
        capas = QgsProject.instance().mapLayersByName(nombre_capa)
        if capas:
            capa = capas[0]
            campos = [campo.name() for campo in capa.fields()]
            self.combo_campo.addItems(campos)

    def ejecutar_busqueda(self):
        self.lista_resultados.clear()
        texto = self.txt_buscar.text()
        if len(texto) < 1: return
        
        nombre_capa = self.combo_capa.currentText()
        nombre_campo = self.combo_campo.currentText()
        capas = QgsProject.instance().mapLayersByName(nombre_capa)
        if not capas: return
        capa = capas[0]
        
        # Búsqueda de registros (Case Insensitive aproximado)
        expresion = f'"{nombre_campo}" LIKE \'%{texto}%\''
        request = QgsFeatureRequest().setFilterExpression(expresion)
        
        for feature in capa.getFeatures(request):
            item = QListWidgetItem(str(feature[nombre_campo]))
            item.setData(Qt.UserRole, feature.id()) # Guardamos el ID del registro
            self.lista_resultados.addItem(item)

    def zoom_al_registro(self, item):
        fid = item.data(Qt.UserRole)
        nombre_capa = self.combo_capa.currentText()
        capas = QgsProject.instance().mapLayersByName(nombre_capa)
        if not capas: return
        capa = capas[0]
        
        # Seleccionar y hacer zoom
        capa.selectByIds([fid])
        iface.mapCanvas().zoomToSelected(capa)
        iface.mapCanvas().refresh()

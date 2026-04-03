import os
from qgis.core import (
    QgsProcessingProvider,
    QgsApplication
)
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from qgis import processing

from .algorithm import SpatialRelationshipMapperAlgorithm


class SpatialRelationshipMapperProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        self.addAlgorithm(SpatialRelationshipMapperAlgorithm())

    def id(self):
        return "spatial_relationship_mapper"

    def name(self):
        return "Spatial Analysis Tools"

    def longName(self):
        return "Spatial Relationship Mapping Tools"

    def icon(self):
        return QgsApplication.getThemeIcon("/algorithms/mAlgorithmIntersect.svg")


class SpatialRelationshipMapperPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.provider = None
        self.action = None

    def initGui(self):
        self.provider = SpatialRelationshipMapperProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        icon = QIcon(icon_path)

        self.action = QAction(icon, "Spatial Relationship Mapper", self.iface.mainWindow())
        self.action.triggered.connect(self.run_tool)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("Spatial Analysis Tools", self.action)

    def run_tool(self):
        processing.execAlgorithmDialog(
            "spatial_relationship_mapper:spatial_relationship_mapper",
            {}
        )

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("Spatial Analysis Tools", self.action)

        QgsApplication.processingRegistry().removeProvider(self.provider)
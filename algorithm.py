import os
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsProcessingMultiStepFeedback,
    QgsSpatialIndex,
    QgsFeature,
    QgsField,
    QgsApplication
)
from qgis.PyQt.QtCore import QVariant


class SpatialRelationshipMapperAlgorithm(QgsProcessingAlgorithm):

    PARCEL_LAYER = "PARCEL_LAYER"
    BUILDING_LAYER = "BUILDING_LAYER"
    PARCEL_ID_FIELD = "PARCEL_ID_FIELD"
    BUILDING_ID_FIELD = "BUILDING_ID_FIELD"
    OUTPUT_PARCELS = "OUTPUT_PARCELS"
    OUTPUT_BUILDINGS = "OUTPUT_BUILDINGS"

    def createInstance(self):
        return SpatialRelationshipMapperAlgorithm()

    def name(self):
        return "spatial_relationship_mapper"

    def displayName(self):
        return "Spatial Relationship Mapper"

    def group(self):
        return "Spatial Analysis Tools"

    def groupId(self):
        return "spatial_analysis_tools"

    def shortHelpString(self):
        return (
            "Creates spatial relationships between two polygon layers.\n\n"
            "• User-selected layers\n"
            "• User-selected ID fields\n"
            "• Outputs layers with related IDs\n"
            "• Supports Temporary or Saved outputs"
        )

    def icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        return QgsApplication.getThemeIcon(icon_path)

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.PARCEL_LAYER,
                "Layer 1 (Parcel)",
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.PARCEL_ID_FIELD,
                "Layer 1 ID field",
                parentLayerParameterName=self.PARCEL_LAYER
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.BUILDING_LAYER,
                "Layer 2 (Building)",
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.BUILDING_ID_FIELD,
                "Layer 2 ID field",
                parentLayerParameterName=self.BUILDING_LAYER
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_PARCELS,
                "Output Layer 1 (with related IDs)"
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_BUILDINGS,
                "Output Layer 2 (with related IDs)"
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        layer1 = self.parameterAsVectorLayer(parameters, self.PARCEL_LAYER, context)
        layer2 = self.parameterAsVectorLayer(parameters, self.BUILDING_LAYER, context)

        layer1_id_field = self.parameterAsString(parameters, self.PARCEL_ID_FIELD, context)
        layer2_id_field = self.parameterAsString(parameters, self.BUILDING_ID_FIELD, context)

        feedback = QgsProcessingMultiStepFeedback(3, feedback)

        layer1_fields = layer1.fields()
        layer1_fields.append(QgsField("related_ids", QVariant.String))

        layer2_fields = layer2.fields()
        layer2_fields.append(QgsField("related_ids", QVariant.String))

        layer1_sink, layer1_dest = self.parameterAsSink(
            parameters,
            self.OUTPUT_PARCELS,
            context,
            layer1_fields,
            layer1.wkbType(),
            layer1.sourceCrs()
        )

        layer2_sink, layer2_dest = self.parameterAsSink(
            parameters,
            self.OUTPUT_BUILDINGS,
            context,
            layer2_fields,
            layer2.wkbType(),
            layer2.sourceCrs()
        )

        feedback.setCurrentStep(0)
        feedback.pushInfo("Creating spatial index...")

        index = QgsSpatialIndex()
        features2 = {}

        for f in layer2.getFeatures():
            index.insertFeature(f)
            features2[f.id()] = f

        feedback.setCurrentStep(1)
        feedback.pushInfo("Processing intersections...")

        rel_1_to_2 = {}
        rel_2_to_1 = {}

        total = layer1.featureCount()

        for i, f1 in enumerate(layer1.getFeatures()):
            if feedback.isCanceled():
                break

            id1 = f1[layer1_id_field]
            geom1 = f1.geometry()

            for fid2 in index.intersects(geom1.boundingBox()):
                f2 = features2[fid2]
                if geom1.intersects(f2.geometry()):
                    rel_1_to_2.setdefault(id1, []).append(f2[layer2_id_field])
                    rel_2_to_1.setdefault(f2[layer2_id_field], []).append(id1)

            feedback.setProgress(int((i / total) * 100))

        feedback.setCurrentStep(2)
        feedback.pushInfo("Writing outputs...")

        for f1 in layer1.getFeatures():
            f = QgsFeature(layer1_fields)
            f.setGeometry(f1.geometry())
            attrs = f1.attributes()
            attrs.append("|".join(map(str, rel_1_to_2.get(f1[layer1_id_field], []))))
            f.setAttributes(attrs)
            layer1_sink.addFeature(f)

        for f2 in layer2.getFeatures():
            f = QgsFeature(layer2_fields)
            f.setGeometry(f2.geometry())
            attrs = f2.attributes()
            attrs.append("|".join(map(str, rel_2_to_1.get(f2[layer2_id_field], []))))
            f.setAttributes(attrs)
            layer2_sink.addFeature(f)

        return {
            self.OUTPUT_PARCELS: layer1_dest,
            self.OUTPUT_BUILDINGS: layer2_dest
        }
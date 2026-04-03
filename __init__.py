from .provider import SpatialRelationshipMapperPlugin

def classFactory(iface):
    return SpatialRelationshipMapperPlugin(iface)
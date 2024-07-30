from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

groupname = 'CustomFunctions - intralayer'

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def Selected_Count(feature, parent):
    """
    Get the number of selected layers as intergers.
    <h2>Example usage:</h2>
    <ul>
      <li>Selected_Count() -> 2</li>
    </ul>
    """
    tgt_ly = iface.activeLayer()
    features = tgt_ly.selectedFeatures()
    return len(features)

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def Selected_FieldArray(fieldN , feature, parent):
    """
    gets field array of the selected feat of an active layer.
    <h2>Example usage:</h2>
    <ul>
      <li>Selected_FieldArray(fieldN, lvl)</li>
      <li>Selected_FieldArray('FieldA', 1) -> Array of values</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = iface.activeLayer()
    features = tgt_ly.selectedFeatures()
    rslt = [f[fieldN] for f in features]
    return rslt

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def geom_isin(featgeom, feature, parent):
    """
    check geom if its in.
    
    <h2>Example usage:</h2>
    <ul>
      <li>geom_isin(featgeom)</li>
    </ul>
    """
    if featgeom.within(feature.geometry()):
        return True

    return False

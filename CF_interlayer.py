from qgis.core import *
from qgis.gui import *

groupname = 'CustomFunctions - interlayer'

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def FeatPos(layerNm, Att, Pos, feature, parent):
    """
    get an attribute value of a index feature of another layer
    <h2>Example usage:</h2>
    <ul>
      <li>FeatPos(layerNm, Att, Pos)</li>
      <li>FeatPos('layerA', 'FieldA', 10) -> 'FieldA10'</li>
    </ul>
    """
    layer = QgsProject.instance().mapLayersByName(layerNm)[0]
    layerList = [feat[Att] for feat in layer.getFeatures()]
    layerList.sort()
    return layerList[Pos]

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_FeatDist(layerNm, type, feature, parent):
    """
    minimum distance from another layer.
    <h2>Example usage:</h2>
    <ul>
      <li>inter_FeatDist_Min(layerNm, type)</li>
      <li>inter_FeatDist_Min(layerNm, type) -> 20.2</li>
    </ul>
    types:
    <ul>
      <li>'min' : minimum</li>
      <li>'min' : maximum</li>
      <li>'avg' : average</li>
    </ul>
    """
    layer = QgsProject.instance().mapLayersByName(layerNm)[0]
    dst = None
    pto = feature.geometry()
    if type == 'min':
        for ft in layer.getFeatures():
            if feature != ft:
                ptd = ft.geometry()
                dd = pto.distance(ptd)
                if dst is None: dst = dd
                elif dd < dst: dst = dd
    elif type == 'max':
        for ft in layer.getFeatures():
            if feature != ft:
                ptd = ft.geometry()
                dd = pto.distance(ptd)
                if dst is None: dst = dd
                elif dd > dst: dst = dd
    elif type == 'avg':
        dst = []
        for ft in layer.getFeatures():
            if feature != ft:
                ptd = ft.geometry()
                dd = pto.distance(ptd)
                dst.append(dd)
        dst = sum(dst)/len(dst)
    return dst

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_sum_byfield(targetlayer, look_field, look_field_value, sum_field, feature, parent):
    """
    Sum the number inside all values in targetlayer sumfield.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_sum_byfield(targetlayer, look_field, look_field_value, sum_field)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    features = tgt_ly.getFeatures()
    rslt = 0
    
    for feat in features:
        look_value = feat[look_field]
        if look_value == look_field_value:
            rslt += feat[sum_field]
    
    return rslt

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def interly_getX(targetlayer, look_field, look_field_value, feature, parent):
    """
    Gets The X value of geometry centroid
    
    <h2>Example usage:</h2>
    <ul>
      <li>interly_getX(targetlayer, look_field, look_field_value)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    features = tgt_ly.getFeatures()
    rslt = None
    
    for feat in features:
        look_value = feat[look_field]
        if look_value == look_field_value:
            rslt = feat.geometry().centroid().asPoint()
            break

    return rslt[0]

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def interly_getY(targetlayer, look_field, look_field_value, feature, parent):
    """
    Gets The Y value of geometry centroid
    
    <h2>Example usage:</h2>
    <ul>
      <li>interly_getX(targetlayer, look_field, look_field_value)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    features = tgt_ly.getFeatures()
    rslt = None
    
    for feat in features:
        look_value = feat[look_field]
        if look_value == look_field_value:
            rslt = feat.geometry().centroid().asPoint()
            break

    return rslt[1]


@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_count_byfield(targetlayer, look_field, look_field_value, feature, parent):
    """
    Sum the number inside all values in targetlayer sumfield.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_sum_byfield(targetlayer, look_field, look_field_value)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    features = tgt_ly.getFeatures()
    rslt = 0
    
    for feat in features:
        look_value = feat[look_field]
        if look_value == look_field_value:
            rslt += 1
    
    return rslt

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_countinside(featgeom, targetlayer, feature, parent):
    """
    counts number of features inside.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_countinside(featgeom, targetlayer)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    rslt = 0
    
    for feat in tgt_ly.getFeatures():
        if feat.geometry().pointOnSurface().within(featgeom):
            rslt += 1

    
    return rslt

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_getvalue(targetlayer, match_field, match_field_value, look_field, feature, parent):
    """
    search value for the first value of a matching value from a field in the targeted layer.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_getvalue(targetlayer, match_field, match_field_value, look_field)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    rslt = None
    
    try:
        for feat in tgt_ly.getFeatures():
            if feat[match_field] == match_field_value: rslt = feat[look_field]
        
        return rslt
    except:
        return None

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_locfield(featgeom, targetlayer, out_field, feature, parent):
    """
    search value for the first value of within geometry.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_locfield(feat_geom', 'targetlayer, out_field)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    rslt = None
    ft_ctr = featgeom.pointOnSurface()
    
    for feat in tgt_ly.getFeatures():
        if ft_ctr.within(feat.geometry()):
            return feat[out_field]

    return ''


@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_locfield_insum(featgeom, targetlayer, out_field, feature, parent):
    """
    gets sum of a field from another point layer of wihtin geom collection
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_locfield_insum(featgeom, targetlayer, out_field)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    inlt = []
    
    for feat in tgt_ly.getFeatures():
        if feat.geometry().within(featgeom):
            inlt.append(feat[out_field])
    
    if len(inlt)==0:
        return 0
    else:
        return sum(inlt)
        
@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_locfield_insumCond(featgeom, targetlayer, out_field, check_field, check_values, feature, parent):
    """
    gets sum of a field from another point layer of wihtin geom collection
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_locfield_insumCond(featgeom, targetlayer, out_field, check_field, check_values)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    inlt = []
    
    for feat in tgt_ly.getFeatures():
        if feat.geometry().pointOnSurface().within(featgeom):
            if feat[check_field] in check_values:
                inlt.append(feat[out_field])
    
    if len(inlt) > 0:
        return sum(inlt)
    else:
        return 0

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_labelarea(targetlayer, TotalArea, check_field, check_area, noncounted, feature, parent):
    """
    Compiles area composition from features on another layer.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_locfield_insumCond(featgeom, targetlayer, out_field, check_field, check_values)</li>
      <li>field input with double tick, with the remaining use single tick</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    groupdict = {}
    joiner = '\n'
    
    for feat in tgt_ly.getFeatures():
        if feat[check_field] != noncounted:
            if feat[check_field] in groupdict:
                groupdict[feat[check_field]] += feat[check_area]
            else:
                groupdict[feat[check_field]] = feat[check_area]
    
    groupdict['others'] = TotalArea - sum(groupdict.values())
    
    return joiner.join([f'{k}   {v:,.2f}   {v/TotalArea*100:,.2f} %' for k, v in sorted(groupdict.items())])


@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_isin(featgeom, target_layer, target_field, target_value, feature, parent):
    """
    check if its in.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_locfield(feat_geom', 'targetlayer, out_field)</li>
      <li>inter_isin(featgeom, target_layer, target_field, target_value)</li>
    </ul>
    """
    root = QgsProject.instance().layerTreeRoot()
    tgt_ly = QgsProject.instance().mapLayersByName(target_layer)[0]
    rslt = None
    ft_ctr = featgeom.pointOnSurface()
    
    for feat in tgt_ly.getFeatures():
        if feat[target_field] in target_value:
            if feat.geometry().within(featgeom):
                return True

    return False

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_within(featgeom, target_layer, target_field, feature, parent):
    """
    check if its in.
    
    <h2>Example usage:</h2>
    <ul>
      <li>inter_within(featgeom, target_layer, target_field)</li>
    </ul>
    """
    tgt_ly = QgsProject.instance().mapLayersByName(target_layer)[0]

    
    for feat in tgt_ly.getFeatures():
        if featgeom.within(feat.geometry()):
            return feat[target_field]
    return False


@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def inter_getgems(target_layer, feature, parent):
    """
    nearest distance to a point.
    nearest_distance(featgeom, target_layer, crsID)
    """
    tgt_ly = QgsProject.instance().mapLayersByName(target_layer)[0]
    opt = [feat.geometry() for feat in tgt_ly.getFeatures()]

    return opt

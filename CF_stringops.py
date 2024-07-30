from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from string import ascii_lowercase, ascii_uppercase

groupname = 'CustomFunctions - stringoperations'

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def str_numbering(targetlayer, value, fid, fieldN, numtype, feature, parent):
    """
    numbers from a matching field.
    <h2>Example usage:</h2>
    <ul>
      <li>str_numbering(targetlayer, value, fid, fieldN, numtype)</li>
      <li>str_numbering('LayerA', 'TypeA', "FID", 'FieldA', numtype) -> 'TypeA.c'</li>
    </ul>
    numtype types:
    <ul>
      <li>'abc': ascii lowecase</li>
      <li>'ABC': ascii uppercase</li>
      <li> any intergernumber for leading zeros</li>
    </ul>
    """
    tgt_ly = QgsProject.instance().mapLayersByName(targetlayer)[0]
    features = tgt_ly.getFeatures()
    # return list(f.name() for f in tgt_ly.fields())
    look_I = []
    look_V = []
    for f in features:
        look_I.append(f['fid'])
        look_V.append(f[fieldN])
    sim_I = []
    for i, v in zip(look_I, look_V):
        if v == value: sim_I.append(i)
    
    if fid not in sim_I:
        return None
    
    if numtype == 'abc':
        return f'{value}.{ascii_lowercase[sim_I.index(fid)]}'
    elif numtype == 'ABC':
        return f'{value}.{ascii_uppercase[sim_I.index(fid)]}'
    else:
        return f'{value}.{sim_I.index(fid)+1:0{numtype}}'

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def Addup(Field, addstring, feature, parent):
    """
    Adds up string with a seperator while making sure no duplicates of string.
    coded separator is '.'
    <h2>Example usage:</h2>
    <ul>
      <li>Addup(Field, addstring)</li>
      <li>Addup(FieldA, 'aa1') -> 'ab2.aa1'</li>
    </ul>
    """
    if Field is None:
        return addstring
    separator='.'
    lt = Field.split(separator)
    if addstring not in lt: Field+=separator+addstring
    
    return Field

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def Subout(Field, addstring, feature, parent):
    """
    Pop out string with a seperator 
    coded separator is '.'
    <h2>Example usage:</h2>
    <ul>
      <li>Subout(Field, addstring)</li>
      <li>Subout(FieldA, 'aa1') -> 'ab2.aa1'</li>
    </ul>
    """
    separator='.'
    lt = Field.split(separator)
    while addstring in lt:
        for x in range(len(lt)):
            if lt[x] == addstring: 
                lt.pop[x]
                break
    separator.join(lt)
    
    return Field
    
@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def str_to_int(value, feature, parent):
    try:
        return int(value)
    except:
        return None

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def midstr_int(value, sep, num, feature, parent):
    """
    finds the number in the value on seperator and index and converts to int
    """
    try:
        val = int(value.split(sep)[num])
    except:
        val = None
    
    return val

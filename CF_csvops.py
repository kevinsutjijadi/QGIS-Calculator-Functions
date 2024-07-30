from qgis.core import *
from qgis.gui import *
import csv

groupname = 'CustomFunctions - CSV operations'

@qgsfunction(args='auto', group=groupname, referenced_columns=[])
def csv_lookup(csv_file, lookup, field_lookup, field_target, feature, parent):
    """
    lookup from csv.
    <h2>Example usage:</h2>
    <ul>
      <li>csv_lookup('C:\\sample.csv', "field_ID", 'csv_id', 'csv_target') -> 13</li>
    </ul>
    """
    with open(csv_file) as op:
        data = csv.reader(op, delimiter=',')
        data = list(data)
    
    header = data.pop(0)
    joiner = ', '
    
    fld_l = None
    fld_t = None
    for n in range(len(header)):
        if field_lookup == header[n]:
            fld_l = n
        if field_target == header[n]:
            fld_t = n
    
    if fld_t is None:
        return f'field target not found\n{joiner.join(header)}'
    if fld_l is None:
        fld_l = 0
    
    for dt in data:
        if dt[fld_l] == lookup:
            return dt[fld_t]
    
    return None

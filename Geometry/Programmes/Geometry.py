import numpy as np
import awkward as ak
import xml.etree.ElementTree as ET
from collections import defaultdict


def read_xml():
    tree = ET.parse('../Ressources/geometry.xml')
    root = tree.getroot()
    Modules = [[] for layer in range(47)]
    layer = 0
    for layer_element in root.findall('.//Plane'):
        layer = int(layer_element.get('id'))
        for motherboard_element in layer_element.findall('.//Motherboard'):
            for module_element in motherboard_element.findall('.//Module'):
                module_id = str(f'{int(module_element.get('id'),16) : 08x}')
                u = int(module_element.get('u'))
                v  = int(module_element.get('v'))
                x = float(module_element.get('x'))
                y = float(module_element.get('y'))
                verticesX,verticesY = vertices(module_element.get('vertices'))
                Modules[layer-1].append({'id':id,'u':u,'v':v,'verticesX' :verticesX,'verticesY' :verticesY})

    layer = 0
    for layer_element in root.findall('.//Plane'):
        layer = int(layer_element.get('id'))
        for motherboard_element in layer_element.findall('.//Motherboard'):
            for tile_element in motherboard_element.findall('.//TileBoard'):
                module_id = str(f'{int(tile_element.get('id'),16) : 08x}')
                u = int(tile_element.get('u'))
                v  = int(tile_element.get('v'))
                x = float(tile_element.get('x'))
                y = float(tile_element.get('y'))
                verticesX,verticesY = vertices(tile_element.get('vertices'))
                Modules[layer-1].append({'id':id,'u':u,'v':v,'verticesX' :verticesX,'verticesY' :verticesY})

        
                
  def vertices(x):  #Vertices of a module
    X = []
    Y = []
    xcourant = ''
    ycourant = ''
    res = 0
    for i in range(len(x)):
        if pos[i] ==';':
            res = 0
            X.append(float(xcourant))
            Y.append(float(ycourant))
            xcourant = ''
            ycourant = ''
        elif pos[i] == ',':
            res = 1
        elif res == 0:
            xcourant += pos[i]
        elif res == 1:
            ycourant += pos[i]
    X.append(xcourant)
    Y.append(ycourant)
    return(X,Y)

print(read_xml)

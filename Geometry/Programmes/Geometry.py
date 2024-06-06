import numpy as np
import awkward as ak
import xml.etree.ElementTree as ET
from collections import defaultdict
import json
import os


def read_xml():
    tree = ET.parse('../Ressources/Geometry.xml')
    print(tree)
    root = tree.getroot()
    Modules = [[] for layer in range(47)]
    layer = 0
    for layer_element in root.findall('.//Plane'):
        layer = int(layer_element.get('id'))
        for motherboard_element in layer_element.findall('.//Motherboard'):
            for module_element in motherboard_element.findall('.//Module'):
                int_id = int(module_element.get('id'),16)
                module_id = str(f'{int_id : 08x}')
                u = int(module_element.get('u'))
                v  = int(module_element.get('v'))
                x = float(module_element.get('x'))
                y = float(module_element.get('y'))
                verticesX,verticesY = vertices(module_element.get('Vertices'))
                Modules[layer-1].append({'id':module_id,'u':u,'v':v,'verticesX' :verticesX,'verticesY' :verticesY})

    layer = 0
    for layer_element in root.findall('.//Plane'):
        layer = int(layer_element.get('id'))
        for motherboard_element in layer_element.findall('.//Motherboard'):
            for tile_element in motherboard_element.findall('.//TileBoard'):
                int_id = int(tile_element.get('id'),16)
                tile_id = str(f'{int_id : 08x}')
                u = int(tile_element.get('u'))
                v  = int(tile_element.get('v'))
                x = float(tile_element.get('x'))
                y = float(tile_element.get('y'))
                verticesX,verticesY = vertices(tile_element.get('Vertices'))
                Modules[layer-1].append({'id':tile_id,'u':u,'v':v,'verticesX' :verticesX,'verticesY' :verticesY})
    return Modules

        
                
def vertices(x):
    X = []
    Y = []
    xcourant = ''
    ycourant = ''
    res = 0 
    for i in range(len(x)):
        if x[i] ==';':
            res = 0
            X.append(float(xcourant))
            Y.append(float(ycourant))
            xcourant = ''
            ycourant = ''
        elif x[i] == ',':
            res = 1
        elif res == 0:
            xcourant += x[i]
        elif res == 1:
            ycourant += x[i]
    X.append(float(xcourant))
    Y.append(float(ycourant))
    return(X,Y)

jsonlist = read_xml()
with open('../Ressources/Modules.json', 'w') as mon_fichier:
    json.dump(jsonlist, mon_fichier)

max = 0
for x in jsonlist:
    if len(x) >max:
        max = len(x)
        
G = np.zeros((len(jsonlist),max,2,6))

for i in range(len(jsonlist)):
    for  j in range(len(jsonlist[i])):
        for vertice_idx in range(len(jsonlist[i][j]['verticesX'])):
            G[i,j,0,vertice_idx] = jsonlist[i][j]['verticesX'][vertice_idx]
            G[i,j,0,vertice_idx] = jsonlist[i][j]['verticesY'][vertice_idx]

UV = np.zeros((len(jsonlist),max,2),dtype = int)
for i in range(len(jsonlist)):
    for j in range(len(jsonlist[i])):
        UV[i,j,0] = int(jsonlist[i][j]['u'])
        UV[i,j,1] = int(jsonlist[i][j]['v'])


#record the files
os.chdir("../Ressources")
np.save('ModulesGeometry',G)
np.save('UVModules.npy',UV)

os.chdir("../../ProgrammesRessources")
np.save('ModulesGeometry',G)
np.save('UVModules.npy',UV)


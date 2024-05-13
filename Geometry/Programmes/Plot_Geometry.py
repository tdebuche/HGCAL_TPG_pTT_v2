import numpy as np
import matplotlib.pyplot as plt
import os

from functions import etaphitoXY
from functions import etaphiRADtoXY
from functions import XYtoetaphi
from functions import polygontopoints
from functions import pointtopolygon
from functions import binetaphitoXY
from functions import binetaphiRADtoXY
from functions import etaphicentre
from functions import ModulestoVertices
from functions import BintoBinVertices
from functions import STCtoSTCVertices


os.chdir("../Ressources")
Z = np.load("Z.npy")
G = np.load('ModulesGeometry.npy')
UV = np.load('UVModules.npy')
Binetaphi2024 = np.load('Binetaphi2024.npy') 
Binetaphi2028 = np.load('Binetaphi2028.npy') 
STCLD = np.load('STCLD.npy')
STCHD = np.load('STCHD.npy')

#In this programme, you can choose to plot (or not) modules, bins, STCs, and put the numbering of modules : u,v numbering, numbering of the layer, numbering of the board

#Layer to draw
Layer = 40
zlay = Z[Layer-1]
Modules = G[Layer-1]
BinXY2024= binetaphitoXY(Binetaphi2024,zlay)
BinXY2028= binetaphitoXY(Binetaphi2028,zlay)
ModuleVertices = ModulestoVertices(Modules)
BinVertices = BintoBinVertices(BinXY)
uv = UV[Layer-1]

#for the numbering of input S1
min_numberingmod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 146, 198, 0, 52, 72, 95, 72, 95]
min_numberingscint = [132, 109, 136, 109, 104, 122, 110, 132, 118, 250, 114, 114, 95, 95]
IndminScint = [95,95,95,95,72,72,52,52,52,52,37,37,37,37]

plt.figure(figsize = (12,8))

#Modules
for i in range(len(ModuleVertices)):
    plt.plot(ModuleVertices[i][0] + [ModuleVertices[i][0][0]],ModuleVertices[i][1]+ [ModuleVertices[i][1][0]], color = 'black')
    eta,phi = etaphicentre(Modules[i],zlay)
    x,y = etaphitoXY(eta,phi,zlay)
    #plt.annotate(str(i),(x - 60,y -10),size =  '8')
print(str(i))


#Bins
for i in range(len(BinXY)):
   plt.plot(BinVertices[i][0] + [BinVertices[i][0][0]],BinVertices[i][1]+ [BinVertices[i][1][0]], color = 'red',linewidth = '0.5')

#STCs
if Layer >33:
    STC = STCLD[Layer-34]
    STCVertices = STCtoSTCVertices(STCLD[Layer-34])
if Layer <34 and Layer > 26:
    STC = STCHD[Layer-27]
    STCVertices = STCtoSTCVertices(STCHD[Layer-27])
if Layer > 26:
        for i in range(len(STCVertices)):
            for j in range(len(STCVertices[i])):
                stc = STCVertices[i][j]
                plt.plot(stc[0]+[stc[0][0]],stc[1]+[stc[1][0]],linewidth = 0.2,color  = 'blue')

#UV
for i in range(len(ModuleVertices)):
    eta,phi = etaphicentre(Modules[i],zlay)
    x,y = etaphitoXY(eta,phi,zlay)
    #plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',(x - 60,y -10),size =  '8')


#Numbering
for i in range(len(ModuleVertices)):
    eta,phi = etaphicentre(Modules[i],zlay)
    x,y = etaphitoXY(eta,phi,zlay)
    if Layer > 33:
        if i < IndminScint[Layer-34]:
            N = min_numberingmod[Layer-14]
            #plt.annotate(str(N + i),(x - 60,y -10),size =  '8')
        else:
            N = min_numberingscint[Layer -34]
            #plt.annotate(str(N + i - IndminScint[Layer-34]),(x - 60,y -10),size =  '8')
    else :
        N = min_numberingmod[Layer//2]
        #plt.annotate(str(N+i),(x - 60,y -10),size =  '8')


plt.title(label =  'pTT of layer '+str(Layer))
plt.xlabel('x (mm)')
plt.ylabel('y (mm)')
plt.show()

#numbering the eta,phi bins
"""
#marker phi
for i in range(24):
    x = (BinXY[i *20][0][0] + BinXY[i *20][0][3])/2
    y = (BinXY[i *20][1][0] + BinXY[i *20][1][3])/2
    if i > 14:
        x = x-20
        y = y +20
    if i > 16:
        x = x-20
        y = y +20
    if i > 19:
        x = x-20
    plt.annotate('phi='+str(i),(x,y),size =  '8')

#marker eta
for i in range(20):
    x = (BinXY[460+i][0][2] + BinXY[460+i][0][3])/2-150
    y = (BinXY[460+i][1][3] + BinXY[460+i][1][3])/2 -100
    plt.annotate('eta='+str(i),(x,y),size =  '8')"""


#record  all layers
"""
#choose the good directory
#os.chdir("./LayerswithbinswithSTCs")
#os.chdir("./LayerswithUV")  
#os.chdir("./Layerswithnumbering") 
#os.chdir("./Layerswithbins") 

for k in range(0,34):
    if k <13:
        Layer = 2 *k+1
    else :
        Layer = k + 14
    zlay = Z[Layer-1]
    Modules = G[Layer-1]
    BinXY= binetaphitoXY(Binetaphi,zlay)
    ModuleVertices = ModulestoVertices(Modules)
    BinVertices = BintoBinVertices(BinXY)
    uv = UV[Layer-1]
    if Layer >33:
        STC = STCLD[Layer-34]
        STCVertices = STCtoSTCVertices(STCLD[Layer-34])
    if Layer <34 and Layer > 26:
        STC = STCHD[Layer-27]
        STCVertices = STCtoSTCVertices(STCHD[Layer-27])
    plt.figure(figsize = (12,8))
    plt.title(label =  'Layer '+str(Layer))
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    for i in range(len(ModuleVertices)):
        plt.plot(ModuleVertices[i][0] + [ModuleVertices[i][0][0]],ModuleVertices[i][1]+ [ModuleVertices[i][1][0]], color = 'black')
        eta,phi = etaphicentre(Modules[i],zlay)
        x,y = etaphitoXY(eta,phi,zlay)


        #if numbering
        if Layer > 33:
            if i < IndminScint[Layer-34]:
                N = min_numberingmod[Layer-14]
                #plt.annotate(str(N + i),(x - 60,y -10),size =  '8')
            else:
                N = min_numberingscint[Layer -34]
                #plt.annotate(str(N + i - IndminScint[Layer-34]),(x - 60,y -10),size =  '8')
        else :
            N = min_numberingmod[Layer//2]
            #plt.annotate(str(N+i),(x - 60,y -10),size =  '8')

            
        #if uv
        #plt.annotate('(' + str(uv[i][0]) +','+str(uv[i][1])+')',(x - 60,y -10),size =  '8')


    #if withbins
    #for i in range(len(BinXY)):
         #plt.plot(BinVertices[i][0] + [BinVertices[i][0][0]],BinVertices[i][1]+ [BinVertices[i][1][0]], color = 'red',linewidth = '0.5')


    #if STCs
    if Layer > 26:
        for i in range(len(STCVertices)):
            for j in range(len(STCVertices[i])):
                stc = STCVertices[i][j]
                #plt.plot(stc[0]+[stc[0][0]],stc[1]+[stc[1][0]],linewidth = 0.2,color  = 'blue') #STC

                
    plt.savefig('Layer '+str(Layer)+'.png')"""

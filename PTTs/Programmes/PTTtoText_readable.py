
import numpy as np
import matplotlib.pyplot as plt
import os
from shapely.geometry import Polygon
import functions
import argparse
from reverse_pTTs import PTTarray
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path + '/../../ProgrammesRessources')

UV =  np.array(functions.item_list('Modules.json','uv'))
G =  np.array(functions.item_list('Modules.json','vertices'))
Module_type =  np.array(functions.item_list('Modules.json','type'))

Values2024 = np.load('ValuesBins2024.npy')
Values2028 = np.load('ValuesBins2028.npy')

Boards = [['0x64000000', 3, 34], ['0x64010000', 1, 36, 47], ['0x64020000', 33, 40, 41], ['0x64030000', 9, 39, 44], ['0x64040000', 7, 42, 43], ['0x64050000', 13, 38, 46], ['0x64060000', 17, 27], ['0x64070000', 25, 31], ['0x64080000', 23, 30], ['0x64090000', 15, 32], ['0x640A0000', 19, 29], ['0x640B0000', 21, 28], ['0x640C0000', 5, 35], ['0x640D0000', 11, 37, 45]]
Boards_scintillators = [['0x64000000', 47], ['0x64010000',41], ['0x64020000',43], ['0x64030000', 37], ['0x64040000', 38], ['0x64050000', 35], ['0x64060000', 40], ['0x64070000', 39], ['0x64080000',42], ['0x64090000', 36], ['0x640A0000', 44], ['0x640B0000',45], ['0x640C0000', 46], ['0x640D0000', 34]]
##########################################        Without STCs   #######################################


def PTTmodulestoTextnoSTC(Geometry,Board,edges):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    if edges:
        Values = Values2028
    else :
        Values = Values2024
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    pTTCEE,pTTCEH = PTTarraytoPTTboardnoSTC(Geometry,Board,edges,nb_binphi,nb_bineta)

    tCEE = ''
    tCEH = ''
    intmatrixE = 0
    intmatrixH = 0
    adderE = 0
    adderH = 0
    maxE = 0
    maxH = 0
    for i in range(nb_binphi):
        for j in range(nb_bineta):
            resE,intmatrixE,adderE,nbmodintowerE = OnepTTCEEnoSTC(pTTCEE,i,j,intmatrixE,adderE)
            if nbmodintowerE > maxE:
                maxE = nbmodintowerE
            resH,intmatrixH,adderH,nbmodintowerH = OnepTTCEHnoSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint)
            if nbmodintowerH > maxH:
                maxH = nbmodintowerH
            tCEE += resE + '\n'
            tCEH += resH + '\n'
    tCEE = '\n' + tCEE 
    tCEE = 'Number of Ptts = '+str(int(nb_binphi*nb_bineta)) + '\n' +tCEE
    tCEE = 'format module = (Layer,u,v),fraction of 1/16' + '\n' + tCEE
    tCEE = 'Board '+Boards[Board][0]+ ', Board number = ' +str(int(Board))+ '\n' +tCEE

    tCEH = '\n' + tCEH

    tCEH = 'Number of Ptts = '+str(int(nb_binphi*nb_bineta)) + '\n' +tCEH
    tCEH = 'format module = (Layer,u,v),fraction of 1/16' + '\n' + tCEH
    tCEH = 'Board '+Boards[Board][0]+ ', Board number = ' +str(int(Board))+ '\n' +tCEH

    return (tCEE,tCEH)


def PTTarraytoPTTboardnoSTC(Geometry,Board,edges,nb_binphi,nb_bineta):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    pTTCEE = [[[]for j in range(nb_bineta)]for i in range(nb_binphi)]
    pTTCEH = [[[]for j in range(nb_bineta)]for i in range(nb_binphi)]

    for i in range(1,len(Layers)):
        Layer = Layers[i]
        if Layer < 27:
            pTTlay = PTTarray(Layer,False,edges)
            for i in range(nb_binphi):
                for j in range(nb_bineta):
                    pTTCEE[i][j].append([Layer,pTTlay[i,j]])
        if Layer > 26:
            pTTlay = PTTarray(Layer,False,edges)
            for i in range(nb_binphi):
                for j in range(nb_bineta):
                    mods = []
                    for k in range(len(pTTlay[i,j])):
                        if not np.array_equal(pTTlay[i,j,k],np.zeros(4)):
                            type = pTTlay[i,j,k,0]
                            if Layer > 33:
                                if type == 'silicon' :
                                    mods.append(pTTlay[i,j,k])
                            else :
                                mods.append(pTTlay[i,j,k])
                    if mods != []:
                        pTTCEH[i][j].append([Layer,mods])

    Layer = Layers_Scint
    pTTscint = PTTarray(Layer,False,edges)
    for i in range(nb_binphi):
        for j in range(nb_bineta):
            sc = []
            for k in range(len(pTTscint[i,j])):
                if not np.array_equal(pTTscint[i,j,k],np.zeros(4)):
                    type = pTTscint[i,j,k,0]
                    if type == 'scintillator':
                        sc.append(pTTscint[i,j,k])
            if sc != []:
                pTTCEH[i][j].append([Layer,sc])

    return(pTTCEE,pTTCEH)

def OnepTTCEEnoSTC(pTTCEE,i,j,intmatrixE,adderE):
    res = ''
    nbmodintower = 0
    intmatrixE +=1    #pour le nbmodintower
    for lay in range(len(pTTCEE[i][j])):
        Layer = pTTCEE[i][j][lay][0]
        for k  in range(len(pTTCEE[i][j][lay][1])):
            if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                nbmodintower += 1
                mod = pTTCEE[i][j][lay][1][k]
                res +=  '('+str(int(Layer))+',Si,'+str(int(mod[1]))+','+str(int(mod[2]))+')'+', '+str(int(mod[3]))+', '
                intmatrixE += 2
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_em-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' +res
    adderE += nbmodintower
    return(res,intmatrixE,adderE,nbmodintower)


def OnepTTCEHnoSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint):
    res = ''
    intmatrixH +=1 #pour le nbmodintower
    nbmodintower = 0
    for lay in range(len(pTTCEH[i][j])):
        Layer = pTTCEH[i][j][lay][0]
        for k  in range(len(pTTCEH[i][j][lay][1])):
            if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(4)):
                mod = pTTCEH[i][j][lay][1][k]
                if Layer == Layers_Scint and mod[0] == 'scintillator':
                    nbmodintower += 1
                    res +=  '('+str(int(Layer))+',Sc,'+str(int(mod[1]))+','+str(int(mod[2]))+')'+', '+str(int(mod[3]))+', '
                    intmatrixH += 2
                if Layer <34:
                    res +=  '('+str(int(Layer))+',Si,'+str(int(mod[1]))+','+str(int(mod[2]))+')'+', '+str(int(mod[3]))+', '
                    intmatrixH += 2
                    nbmodintower += 1
                if  Layer >33 and Layer != Layers_Scint and mod[0] != 'scintillator' :
                    res +=  '('+str(int(Layer))+',Si,'+str(int(mod[1]))+','+str(int(mod[2]))+')'+', '+str(int(mod[3]))+', '
                    intmatrixH += 2
                    nbmodintower += 1
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_had-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' + res
    adderH += nbmodintower
    return(res,intmatrixH,adderH,nbmodintower)





#########################################################          WITH STCs        ###############################################


def PTTmodulestoTextwithSTC(Geometry,Board,edges):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    if edges:
        Values = Values2028
    else :
        Values = Values2024
    nb_binphi,nb_bineta,phimin,phimax,etamin,etamax = Values
    nb_binphi,nb_bineta = int(nb_binphi),int(nb_bineta)
    pTTCEE,pTTCEH = PTTarraytoPTTboardwithSTC(Geometry,Board,edges,nb_binphi,nb_bineta)

    

    tCEE = ''
    tCEH = ''
    intmatrixE = 0
    intmatrixH = 0
    adderE = 0
    adderH = 0
    maxE = 0
    maxH = 0
    for i in range(nb_binphi):
        for j in range(20):
            resE,intmatrixE,adderE,nbmodintowerE = OnepTTCEEwithSTC(pTTCEE,i,j,intmatrixE,adderE)
            if nbmodintowerE > maxE:
                maxE = nbmodintowerE
            resH,intmatrixH,adderH,nbmodintowerH = OnepTTCEHwithSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint)
            if nbmodintowerH > maxH:
                maxH = nbmodintowerH
            tCEE += resE + '\n'
            tCEH += resH + '\n'

    tCEE = '\n' + tCEE

    tCEE = 'Number of Ptts = '+str(int(nb_binphi*nb_bineta)) + '\n' +tCEE
    tCEE = 'format module = (Layer,u,v),fraction of 1/16' + '\n' + tCEE
    tCEE = 'Board '+Boards[Board][0]+ ', Board number = ' +str(int(Board))+ '\n' +tCEE

    tCEH = '\n' + tCEH
    tCEH = 'Number of Ptts = '+str(int(nb_binphi*nb_bineta)) + '\n' +tCEH
    tCEH = 'format module = (Layer,u,v,index_STC),fraction of 1/16' + '\n' + tCEH
    tCEH = 'Board '+Boards[Board][0]+ ', Board number = ' +str(int(Board))+ '\n' +tCEH


    return (tCEE,tCEH)

def PTTarraytoPTTboardwithSTC(Geometry,Board,edges,nb_binphi,nb_bineta):
    Layers = Boards[Board]
    Layers_Scint = Boards_scintillators[Board][1]
    pTTCEE = [[[]for j in range(nb_bineta)]for i in range(nb_binphi)]
    pTTCEH = [[[]for j in range(nb_bineta)]for i in range(nb_binphi)]

    for i in range(1,len(Layers)):
        Layer = Layers[i]
        if Layer < 27:
            pTTlay = PTTarray(Layer,True,edges)
            for i in range(nb_binphi):
                for j in range(nb_bineta):
                    pTTCEE[i][j].append([Layer,pTTlay[i,j]])
        if Layer > 26:
            pTTlay = PTTarray(Layer,True,edges)
            for i in range(nb_binphi):
                for j in range(nb_bineta):
                    stc = []
                    for k in range(len(pTTlay[i,j])):
                        if not np.array_equal(pTTlay[i,j,k],np.zeros(5)):
                            type = pTTlay[i,j,k,0]
                            if Layer > 33:
                                if type == 'silicon' :
                                    stc.append(pTTlay[i,j,k])
                            else :
                                stc.append(pTTlay[i,j,k])
                    if stc != []:
                        pTTCEH[i][j].append([Layer,stc])

    Layer = Layers_Scint
    pTTscint = PTTarray(Layer,True,edges)
    for i in range(nb_binphi):
        for j in range(nb_bineta):
            sc = []
            for k in range(len(pTTscint[i,j])):
                if not np.array_equal(pTTscint[i,j,k],np.zeros(4)):
                    type = pTTlay[i,j,k,0]
                    if type == 'scintillator' :
                        sc.append(pTTscint[i,j,k])
            if sc != []:
                pTTCEH[i][j].append([Layer,sc])

    return(pTTCEE,pTTCEH)

def OnepTTCEEwithSTC(pTTCEE,i,j,intmatrixE,adderE):
    res = ''
    nbmodintower = 0
    intmatrixE +=1    #pour le nbmodintower
    for lay in range(len(pTTCEE[i][j])):
        Layer = pTTCEE[i][j][lay][0]
        for k  in range(len(pTTCEE[i][j][lay][1])):
            if not np.array_equal(pTTCEE[i][j][lay][1][k],np.zeros(4)):
                nbmodintower += 1
                mod = pTTCEE[i][j][lay][1][k]
                res +=  '('+str(int(Layer))+',Si,'+str(int(mod[1]))+','+str(int(mod[2]))+')'+', '+str(int(mod[3]))+', '
                intmatrixE += 2
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_em-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' +res
    adderE += nbmodintower
    return(res,intmatrixE,adderE,nbmodintower)


def OnepTTCEHwithSTC(pTTCEH,i,j,intmatrixH,adderH,Layers_Scint):
    res = ''
    intmatrixH +=1 #pour le nbmodintower
    nbmodintower = 0
    for lay in range(len(pTTCEH[i][j])):
        Layer = pTTCEH[i][j][lay][0]
        for k  in range(len(pTTCEH[i][j][lay][1])):
            #if not np.array_equal(pTTCEH[i][j][lay][1][k],np.zeros(4)):  #Useless ??
            mod = pTTCEH[i][j][lay][1][k]
            if Layer == Layers_Scint and mod[0] == 'scintillator':
                nbmodintower += 1
                res +=  '('+str(int(Layer))+',Sc,'+str(int(mod[1]))+','+str(int(mod[2]))+','+str(int(mod[3]))+')'+', '+str(int(mod[4]))+', '
                intmatrixH += 3
            if Layer <34:
                res +=  '('+str(int(Layer))+',Si,'+str(int(mod[1]))+','+str(int(mod[2]))+','+str(int(mod[3]))+')'+', '+str(int(mod[4]))+', '
                intmatrixH += 3
                nbmodintower += 1
            if  Layer >33 and Layer != Layers_Scint and mod[0] == 'silicon':
                nbl = min_numberingmod[Layer - 14]
                res +=  '('+str(int(Layer))+',Si'+str(int(mod[1]))+','+str(int(mod[2]))+','+str(int(mod[3]))+')'+', '+str(int(mod[4]))+', '
                intmatrixH += 3
                nbmodintower += 1
    if i*20+j<10:
        nbzeros= '000'
    if i*20+j>9 and i*20+j<100:
        nbzeros='00'
    if i*20+j>=100:
        nbzeros= '0'
    res ='/* out'+nbzeros+str(int(i*20+j))+'_had-eta'+str(j)+'-phi'+str(i)+'*/'+'\t'+str(int(nbmodintower))+', ' + res
    adderH += nbmodintower
    return(res,intmatrixH,adderH,nbmodintower)






##################################################################################################################################
#Parameters:

parser = argparse.ArgumentParser()
parser.add_argument("Board", help="Layer to display",type=int)
parser.add_argument("--STCs",default = 'yes', help="With (yes) or without STCs (no)")
parser.add_argument("--Edges",default = 'no', help="With (yes) or without edges(no)")
parser.add_argument("--Record",default = 'no', help="Record all boards")
args = parser.parse_args()

# to test
os.chdir(dir_path+"/../Ressources/test")

Board = args.Board
if args.Edges == 'yes' and args.STCs == 'yes':
    textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,True)
    name ="PTTs_Board"+  str(Board) + 'Edges'+'STCs'
if args.Edges == 'no'and args.STCs == 'yes':
    name ="PTTs_Board"+  str(Board) + 'NoEdges'+'STCs'
    textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,False)
if args.Edges == 'yes' and args.STCs == 'no':
    name ="PTTs_Board"+  str(Board) + 'Edges'+'NoSTCs'
    textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,True)
if args.Edges == 'no'and args.STCs == 'no':
    name ="PTTs_Board"+  str(Board) + 'NoEdges'+'NoSTCs'
    textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,False)
    
file = open(name+"CEE"+".txt", "w")
file.write(textCEE)
file.close()
file = open(name+"CEH"+".txt", "w")
file.write(textCEH)
file.close()

# Record
if args.Record == 'yes':
    if args.Edges == 'yes' and args.STCs == 'yes':
        os.chdir(dir_path+"/../Ressources/Readable_files/28_Phi_Bins/with_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,True)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()
    if args.Edges == 'yes' and args.STCs == 'no':
        os.chdir(dir_path+"/../Ressources/Readable_files/28_Phi_Bins/without_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,True)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()
    if args.Edges == 'no' and args.STCs == 'yes':
        os.chdir(dir_path+"/../Ressources/Readable_files/24_Phi_Bins/with_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextwithSTC(G,Board,False)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()
    
    if args.Edges == 'no' and args.STCs == 'no':
        os.chdir(dir_path+"/../Ressources/Readable_files/24_Phi_Bins/without_STCs")
        for Board in range(14):
            textCEE,textCEH = PTTmodulestoTextnoSTC(G,Board,False)
            name = 'CE_E_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEE)
            file.close()
            name = 'CE_H_'+  str(Board)+ '_v1'
            file = open(name+".txt", "w")
            file.write(textCEH)
            file.close()



if args.Edges == 'yes' and args.STCs == 'yes':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''
    print('ok')
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextwithSTC(G,Board,True)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_Edges'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_Edges'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()

if args.Edges == 'no' and args.STCs == 'yes':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''        
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextwithSTC(G,Board,False)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_NoEdges'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_NoEdges'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()


if args.Edges == 'yes' and args.STCs == 'no':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''
    print('ok')
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextnoSTC(G,Board,True)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_EdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_EdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()

if args.Edges == 'no' and args.STCs == 'no':
    os.chdir(dir_path+"/../Ressources/Readable_files")
    textCEE,textCEH ='',''        
    for Board in range(14):
        print(Board)
        res1,res2 = PTTmodulestoTextnoSTC(G,Board,False)
        textCEE += res1
        textCEH += res2
    name = 'CE_E_allBoards_NoEdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEE)
    file.close()
    name = 'CE_H_allBoards_NoEdgesNoSTCs'
    file = open(name+".txt", "w")
    file.write(textCEH)
    file.close()





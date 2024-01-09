import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import preprocessing
from sklearn import metrics

pd.options.mode.chained_assignment = None  # default='warn'

def knn(base_Datos,compuesto,k):                              # Vecinos mas cercanos del nuevo compuesto
    distancias, vecinos_Planos, plasmones= [], [], []       # Almacena todas las distancias
    tam = len(base_Datos)
    for i in range(tam):
        objeto=pd.DataFrame([base_Datos.iloc[i,:]])
        dis = dis_Planos(objeto,compuesto,i)     # Llama a la funcion para obtener distancia euclidiana
        distancias.append(dis)
    distancias_tem = distancias.copy()                      # Obtiene una copia de la lista de distancias
    for i in range(k):                                      # Obtiene el numero de vecinos k-nn
        dis_min = min(distancias_tem)                       # Extrae el valor minimo de distancias
        indice  = distancias_tem.index(dis_min)             # Posicion de la distancia minima
        vecinos_Planos.append(indice)                       # Almacenas las posiciones de los vecinos
        distancias_tem[indice] = max(distancias_tem)        # Cambia el valor del vecino para no conflicto
    return distancias, vecinos_Planos                       # Retorna las distancias y las posiciones de los vecinos

def dis_Planos(objeto,Compuesto,j):                      # Funcion para sacar las distancias euclidianas 
    suma = 0
    for i in range(0,12,2):                                # Ciclo para obtener la distancia
        x1      = (objeto.loc[j][i]-Compuesto.loc[0][i])**2 + (objeto.loc[j][i+1]-Compuesto.loc[0][i+1])**2  # Distancia euclidiana
        suma    = suma + x1                        
    distancia   = np.sqrt(suma)
    obj1, obj2  = objeto.loc[j][12], objeto.loc[j][13]
    com1, com2  = Compuesto.loc[0][12], Compuesto.loc[0][13]
    

    dis1 = abs(com1-obj1)
    dis2 = abs(com1-obj2)
    dis3 = abs(com2-obj1)
    dis4 = abs(com2-obj2)
    if np.isnan(dis1) == True & np.isnan(dis2) == True:
        min1=np.nan
    else:
        if np.isnan(dis1) == True:
            min1 = dis2
        elif np.isnan(dis2) == True:
            min1 = dis1
        else:
            if dis1<dis2:
                min1=dis1
            else:
                min1 =dis2
 
    if np.isnan(dis3) == True & np.isnan(dis4) == True:
        min2=np.nan
    else:
        if np.isnan(dis3) == True:
            min2 = dis4
        elif np.isnan(dis4) == True:
            min2 = dis3
        else:
            if dis3<dis4:
                min2=dis3
            else:
                min2 =dis4

    if np.isnan(min1) == True:
        distancia_plas = min2
    elif np.isnan(min2) == True:
        distancia_plas = min1
    else:
        if min1<min2:
            distancia_plas = min1
        else:
            distancia_plas = min2
    #print(min1,min2)
    #print(distancia_plas)
    return distancia + distancia_plas                                   # Retorna la distancia

def graficador_planos(base_Datos,distancia, vecinos,nuevo_Compuesto): # Funcion para graficar los planos cristalograficos
    #fig, ax = plt.subplots()
    plt.figure(figsize=(12,7))                              # Tamaño de la grafica
    for i in vecinos:                                       # Obtiene los puntos para el eje X y Y
        x_points, y_points = [], []
        for j in range(0,12,2):                             # Graficador de compuestos
            x_points.append(base_Datos.loc[i][j])
            y_points.append(base_Datos.loc[i][j+1])
        plt.plot(x_points, y_points, marker='o',label=str(base_Datos.loc[i][-2])+':'+str(str(base_Datos.loc[i][-1])) + ':' + str(distancia[i])) # Graficador
    x_points, y_points = [], []
    for j in range(0,12,2):                                 # Graficador del nuevo compuesto
        x_points.append(nuevo_Compuesto.loc[0][j])
        y_points.append(nuevo_Compuesto.loc[0][j+1])
    plt.plot(x_points, y_points,marker='*',c='black',label='Nuevo Compuesto') 
    plt.xlabel("2 theta")                                   # Nombre eje X
    plt.ylabel("I max")                                     # Nombre eje Y
    plt.legend()
    plt.show()

def graficador_plasmones(base_Datos,distancia, vecinos,Compuesto):
    plt.figure(figsize=(12,7))
    cont=0
    for i in range(len(vecinos)):
        objeto = pd.read_csv("/Users/arturo/Desktop/Datos/Plasmones_COD/{}.csv".format(base_Datos.loc[vecinos[i]][-1]), names=['l_onda','abs'])
        objeto.drop(objeto[(objeto['l_onda'] <= 200)].index, inplace=True)
        objeto.drop(objeto[(objeto['l_onda'] >= 1000)].index, inplace=True)
        objeto.reset_index(inplace=True)
        xpoints = objeto['l_onda']
        ypoints = objeto['abs']
        plt.plot(xpoints, ypoints,label=str(base_Datos.loc[vecinos[i]][-2])+':'+str(str(base_Datos.loc[vecinos[i]][-1])) + ':' + str(distancia[vecinos[i]]))  #label=str(nomTotal[cont]
        cont += 1 
    
    objeto1 = pd.read_csv("/Users/arturo/Desktop/validacion/plasmones/{}.csv".format(int(Compuesto.loc[0][Compuesto.shape[1]-1])), names=['l_onda','abs'])
    print(objeto1)
    
    objeto1.drop(objeto1[(objeto1['l_onda'] <= 200)].index, inplace=True)
    objeto1.drop(objeto1[(objeto1['l_onda'] >= 1000)].index, inplace=True)
    objeto1.reset_index(inplace=True)
    xpoints = objeto1['l_onda']
    ypoints = objeto1['abs']
    plt.plot(xpoints, ypoints,label=str(int(Compuesto.iloc[0][Compuesto.shape[1]-1])))  #label=s|tr(nomTotal[cont]
    
    plt.xlabel("Longitud de onda (nm)")
    plt.ylabel("Absorbancia (a.u.)")
    ax= plt.gca()
    ax.axes.yaxis.set_ticklabels([])
    plt.legend()
    plt.show()

entrada_DB  = pd.read_csv("/Users/arturo/Desktop/Proyecto/Base_de_datos.csv")       # Ingresa la base de e_DB_Etiquetados como un data frame df
base_Datos = entrada_DB[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1','FormQuimica', 'ID']]  # Elimina las columnas no necesarias del df
base_Datos.drop(base_Datos.loc[(np.isnan(entrada_DB['l_onda']) == True) & (np.isnan(entrada_DB['l_onda.1'])==True)].index,inplace=True)
base_Datos.reset_index(inplace=True)
base_Datos.drop(['index'], axis='columns', inplace= True)
compuesto1  = pd.DataFrame([[36.88803924,10.41574658,42.85477543,100,42.96654147,50,62.21468205,52.42823491,62.3865746,26.21411745,78.50748447,14.70624313,215.5999612,base_Datos['l_onda.1'].mean(),9000492]])
compuesto  = pd.DataFrame([[36.88803924,10.41574658,42.85477543,100,42.96654147,50,62.21468205,52.42823491,62.3865746,26.21411745,78.50748447,14.70624313,215.5999612,base_Datos['l_onda.1'].mean()]])
#compuesto  = pd.DataFrame([[28.09806346,100,28.16932102,50,32.55694204,86.91097665,32.64009794,43.45548832,46.70820749,61.06970077,55.39908576,47.00516442,364.3158414,base_Datos['l_onda.1'].mean()]])
#compuesto  = pd.DataFrame([[36.33446047,38.03076671,38.39618046,71.57155706,38.39618046,100,38.49534102,35.78577853,38.49534102,50,60.19659452,32.12171944,564.5704425,256.7609978]]) 
#compuesto  = base_Datos.sample().reset_index(inplace=False)
#compuesto.drop(['index'], axis='columns', inplace= True)
k = 5
if __name__ == '__main__':                               # Funcion principal, siempre se ejecuta
    distancia, pos_Vecinos =knn(base_Datos, compuesto,k) # Vecinos mas cercanos de planos cristalograicos
    #print(base_Datos.to_string())
    #print(len(base_Datos))
    print(pos_Vecinos,"\n\n\n")
    graficador_planos(base_Datos,distancia,pos_Vecinos,compuesto)
    graficador_plasmones(base_Datos,distancia,pos_Vecinos,compuesto1)

#print(int(compuesto1.iloc[0][compuesto1.shape[1]-1]))


# DBSCAN, este algoritmo agrupa los e_DB_Etiquetados por medio de la caracteristica PLASMON
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import preprocessing
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors

def normalizacion(df):                                                          # Funcion para estandarizar                                     
    normal  = preprocessing.MinMaxScaler().fit_transform(df)                    # Escala Min_Max
    normal  = pd.DataFrame(normal, columns=['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1'])                                   # Columnas escaladas
    return normal                                                               # Retoruna el nuevo DataFrame normalizado

def best_eps(df):                                                               # Función para encontrar los eps optimos
    ns = 28 - 1                                                                 # Numero de vecinos para evaluar cada elemento del data frame (2*Dimenciones-1) 
    nbrs = NearestNeighbors(n_neighbors=ns).fit(df)                             # LLama a la funcion de KNN
    distances, indices = nbrs.kneighbors(df)                                    # Obtiene las distancias y los indices
    distanceDec = sorted(distances[:,ns-1], reverse=True)                       # Ordena las distancias
    plt.plot(indices[:,0], distanceDec)                                         # Grafica el algoritmo.
    plt.ylabel("Eps")
    plt.xlabel("Muestra")
    plt.grid()
    plt.show()

def coef_Silhuoette(df_Norm):                                                   # Funcion para evaluar el coeficiente de Silhuoette
    x, y = [], []                                                               # Variables de tipo lista para graficar
    eps = np.arange(0.1,0.8,0.05)
    for i in eps:                                                               # Ciclo para evaluar diferentes eps
        cluster     = DBSCAN(eps=i, min_samples=14).fit(df_Norm[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']])            # Aplica DBSCAN 
        etiqueta    = cluster.labels_                                           # Extrae las etiquetas asignadas por DBSCAN
        n_clusters_ = len(set(etiqueta)) - (1 if -1 in etiqueta else 0)         # Numero de grupos 
        silhuoette  = "%0.3f" % metrics.silhouette_score(df_Norm[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']], etiqueta) # Evalua el coeficiente de Silhuoette
        print(" Eps: ",i,"\n","No. Clusters: ",n_clusters_,"\n","Coef. Silhuoette: ",silhuoette,"\n")  # Imprime todos los ciclos
        x.append(n_clusters_)                                                   # Datos numero de cluster
        y.append(silhuoette)                                                    # Datos coeficiente de Silhuoette                                                    
    
    plt.plot(eps,y,marker='o')                                                  # Grafica el algoritmo.
    #plt.yscale('linear')
    plt.grid()
    plt.ylabel("Co. Silhouette")
    plt.xlabel("Eps")
    plt.show()
    value_eps = float(input("Ingrese el eps: "))
    return value_eps

def DBSCAN_FUN(df_Norm_prev, e_DB):                                             # Funcion para combinar los plasmones
    c_eps = coef_Silhuoette(df_Norm_prev)                                       # Evalua el mejor Coeficiente de Silhuoette
    cluster = DBSCAN(eps=c_eps, min_samples=14).fit(df_Norm_prev[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']])            # Aplica DBSCAN 
    etiquetas = cluster.labels_                                                 # Extrae las etiquetas asignadas por DBSCAN
    n_clusters_ = len(set(etiquetas)) - (1 if -1 in etiquetas else 0)           # Numero de grupos 
    silhuoette =  "%0.3f" % metrics.silhouette_score(df_Norm_prev[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']], etiquetas)# Evalua el coeficiente de Silhuoette
    print("\n\nDBSCAN")
    print(" Eps: ",c_eps,"\n","No. Clusters: ",n_clusters_,"\n","Coef. Silhuoette: ",silhuoette,"\n")  # Imprime todos los ciclos
    df_DBSCAN1 = df_Norm_prev.assign(Etiqueta= etiquetas)
    df_DBSCAN = e_DB.assign(Etiqueta= etiquetas)                                 # Asigna la etiqueta al dataframe de DBSCAN
    df_DBSCAN.to_csv('DBSCAN.csv', header=True, index=False) 
    print(df_DBSCAN)
    

############## INICIA EL PROGRAMA ##############
entrada_DB  = pd.read_csv("/Users/arturo/Desktop/Proyecto/Base_de_datos.csv")    # Ingresa la base de e_DB_Etiquetados como un data frame df
salidaDB = pd.read_csv("/Users/arturo/Desktop/Proyecto/Base_de_datos.csv")
entrada_DB_Temp = entrada_DB[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']]  # Elimina las columnas no necesarias del df
mean_2 = entrada_DB_Temp['l_onda.1'].mean()
entrada_DB_Temp.fillna({'l_onda.1': mean_2}, inplace=True)
salidaDB = entrada_DB
salidaDB.fillna({'l_onda.1': mean_2}, inplace=True)

if __name__ == '__main__':                                                       # Funcion principal, siempre se ejecuta
    df_normalizada = normalizacion(entrada_DB_Temp) 
    best_eps(df_normalizada)
    DBSCAN_FUN(df_normalizada, salidaDB)


    
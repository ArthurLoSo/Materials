# DBSCAN, este algoritmo agrupa los e_DB_Etiquetados por medio de la caracteristica PLASMON
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn import preprocessing
from sklearn import metrics

def normalizacion(df):                                                              # Funcion para estandarizar 
    modo = "maxmin"                                                                 # Escalamiento o Normalizacion: (maxmin/media)
    if modo == "maxmin":                                                            
        normal  = preprocessing.MinMaxScaler().fit_transform(df)                    # Escala Min_Max
        normal  = pd.DataFrame(normal, columns=['Abs','l_onda','Abs.1','l_onda.1','Oxigenos','plasmon_MG']) # Columnas escaladas
    elif modo == "media":
        normal  = preprocessing.RobustScaler().fit_transform(df)                    # Normalizacion media
        normal  = pd.DataFrame(normal, columns=['Abs','l_onda','Abs.1','l_onda.1','Oxigenos','plasmon_MG']) # Columnas Normalizadas
    #print(normal)
    return normal                                                                   # Retoruna el nuevo DataFrame normalizado

def coef_Silhuoette(df_Norm,opcion):                                                # Funcion para evaluar el coeficiente de Silhuoette
    x, y = [], []                                                                   # Variables de tipo lista para graficar
    if opcion == 0:                                                                 # eps para el plasmon mas grande
        eps=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2]
    elif opcion == 1:                                                               # eps para todos los plasmones
        eps=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2]
    for i in eps:                                                                   # Ciclo para evaluar diferentes eps
        cluster     = DBSCAN(eps=i, min_samples=10).fit(df_Norm[['Oxigenos','plasmon_MG']]) # Aplica DBSCAN 
        etiqueta    = cluster.labels_                                               # Extrae las etiquetas asignadas por DBSCAN
        n_clusters_ = len(set(etiqueta)) - (1 if -1 in etiqueta else 0)             # Numero de grupos 
        silhuoette  =  "%0.3f" % metrics.silhouette_score(df_Norm[['Oxigenos','plasmon_MG']], etiqueta) # Evalua el coeficiente de Silhuoette
        print(" Eps: ",i,"\n","No. Clusters: ",n_clusters_,"\n","Coef. Silhuoette: ",silhuoette,"\n")  # Imprime todos los ciclos
        x.append(n_clusters_)                                                       # Datos numero de cluster
        y.append(silhuoette)                                                        # Datos coeficiente de Silhuoette

    grafica = "no"                                                                  # Graficar coeficiente de Silhuoette (si/no)
    if grafica == "si":                                                            
        #print(df_Norm)
        fig = plt.figure(figsize = (8,5))
        ax1 = fig.add_subplot(1,1,1)
        ax1.set_title("Coeficiente de Silhouette")
        ax1.plot(eps, y, marker='o')
        plt.show()
    else:
        pass
    x= float(input("Ingrese el eps: "))
    return x

def graficador(df_DBSCAN,nombre):
    fig = plt.figure(figsize = (8,5))
    #ax1 = fig.add_subplot(1,1,1)
    #ax1.set_title(nombre)
    #ax1.scatter(df_DBSCAN[df_DBSCAN.columns[0]], df_DBSCAN[df_DBSCAN.columns[1]], c = df_DBSCAN[df_DBSCAN.columns[2]])
    #plt.show()
    ax=sns.scatterplot(data=df_DBSCAN, x=df_DBSCAN[df_DBSCAN.columns[0]], 
                    y=df_DBSCAN[df_DBSCAN.columns[1]],hue=df_DBSCAN[df_DBSCAN.columns[2]], palette = "Paired")
    sns.move_legend(ax, "upper left",bbox_to_anchor=(1, 1))
    ax.set(xlabel=None)
    ax.set(ylabel=None)
    plt.show()

def generador_grupos(e_DB_Etiquetados):
    atipicos = e_DB_Etiquetados[e_DB_Etiquetados['Etiqueta']== -1]                  # Datos atipicos
    atipicos.reset_index(inplace=True)                                              # Reinicia los Datos atipicos
    x = e_DB_Etiquetados['Etiqueta'].max() + 1                                      # Busca el numero de grupos
    for n in range(0,x,1):                                                          # Ciclo para separar los grupos
        globals()['grupo%s' % n] = e_DB_Etiquetados[e_DB_Etiquetados['Etiqueta']== n] # Crea y busca variables con la etiqueta correcta
        globals()['grupo%s' % n].reset_index(inplace=True)                          # Reinicia los indices de los grupos
        globals()['grupo%s' % n].drop(['index'], axis='columns', inplace= True)     # Elimina columna index 
        print(globals()['grupo%s' % n])                                             # Imprime los grupos
    print(atipicos)                                                                  # Imprime los outliers

def plasmon_mas_Grande(df_Norm, e_DB):
    c_eps       = coef_Silhuoette(df_Norm,0)                                        # Evalua el mejor Coeficiente de Silhuoette
    cluster     = DBSCAN(eps=c_eps, min_samples=10).fit(df_Norm[['Oxigenos','plasmon_MG']]) # Aplica DBSCAN 
    etiquetas   = cluster.labels_                                                   # Extrae las etiquetas asignadas por DBSCAN
    n_clusters_ = len(set(etiquetas)) - (1 if -1 in etiquetas else 0)               # Numero de grupos 
    silhuoette  =  "%0.3f" % metrics.silhouette_score(df_Norm[['Oxigenos','plasmon_MG']], etiquetas) # Evalua el coeficiente de Silhuoette
    print("\n\nDBSCAN")
    print(" Eps: ",c_eps,"\n","No. Clusters: ",n_clusters_,"\n","Coef. Silhuoette: ",silhuoette,"\n")  # Imprime todos los ciclos
    df_DBSCAN   = df_Norm.assign(Etiqueta= etiquetas)                               # Asigna la etiqueta al dataframe de DBSCAN
    df_DBSCAN.drop(df_DBSCAN[(df_DBSCAN['Etiqueta'] == -1)].index, inplace=True)    # Elimina los Outliers del df_DBSCAN
    e_DB_Etiquetados = e_DB.assign(Etiqueta= etiquetas)                             # Asigna las etiquetas a la base de e_DB_Etiquetados principal
    e_DB_Etiquetados.to_csv('DBSCAN_PMG.csv', header=True, index=False)             # Genera el archivo de salida
    generador_grupos(e_DB_Etiquetados)                                              # Genera los grupos y exporta los resultados
    graficador(df_DBSCAN[['plasmon_MG','Oxigenos','Etiqueta']],"Plasmon mas grande")# Funcion para graficar los grupos

def todos_Plasmones(df_Norm_prev, e_DB):                                            # Funcion para combinar los plasmones
    plasmon_update, oxigeno_update, form, id        = [], [], [], []                # Variables para combinar los plasmones
    theta1, theta2, theta3, theta4, theta5, theta6  = [], [], [], [], [], []        # Varibales para aculumar las theta
    imax1, imax2, imax3, imax4, imax5, imax6        = [], [], [], [], [], []        # Variables para acumular imax
    l_on1, l_on2, abs1, abs2, oxi                   = [], [], [], [], []            # Varibales de plasmones y oxigeno
    for i in range(len(df_Norm_prev)):                                              # Ciclo para combinar los plasmones y extraer los datos para los nuevos DF
        x = df_Norm_prev['l_onda'][i]
        y = df_Norm_prev['l_onda.1'][i]
        if np.isnan(x) == True:
            pass
        else:
            plasmon_update.append(df_Norm_prev['l_onda'][i])
            oxigeno_update.append(df_Norm_prev['Oxigenos'][i])
            form.append(e_DB['FormQuimica'][i])
            id.append(e_DB['ID'][i])
            theta1.append(e_DB['2theta'][i])
            theta2.append(e_DB['2theta.1'][i])
            theta3.append(e_DB['2theta.2'][i])
            theta4.append(e_DB['2theta.3'][i])
            theta5.append(e_DB['2theta.4'][i])
            theta6.append(e_DB['2theta.5'][i])
            imax1.append(e_DB['Imax'][i])
            imax2.append(e_DB['Imax.1'][i])
            imax3.append(e_DB['Imax.2'][i])
            imax4.append(e_DB['Imax.3'][i])
            imax5.append(e_DB['Imax.4'][i])
            imax6.append(e_DB['Imax.5'][i])
            l_on1.append(e_DB['l_onda'][i])
            abs1.append(e_DB['Abs'][i])
            l_on2.append(e_DB['l_onda.1'][i])
            abs2.append(e_DB['Abs.1'][i])
            oxi.append(e_DB['Oxigenos'][i])
        if np.isnan(y) == True:
            pass
        else:
            plasmon_update.append(df_Norm_prev['l_onda.1'][i])
            oxigeno_update.append(df_Norm_prev['Oxigenos'][i])
            form.append(e_DB['FormQuimica'][i])
            id.append(e_DB['ID'][i])
            theta1.append(e_DB['2theta'][i])
            theta2.append(e_DB['2theta.1'][i])
            theta3.append(e_DB['2theta.2'][i])
            theta4.append(e_DB['2theta.3'][i])
            theta5.append(e_DB['2theta.4'][i])
            theta6.append(e_DB['2theta.5'][i])
            imax1.append(e_DB['Imax'][i])
            imax2.append(e_DB['Imax.1'][i])
            imax3.append(e_DB['Imax.2'][i])
            imax4.append(e_DB['Imax.3'][i])
            imax5.append(e_DB['Imax.4'][i])
            imax6.append(e_DB['Imax.5'][i])
            l_on1.append(e_DB['l_onda'][i])
            abs1.append(e_DB['Abs'][i])
            l_on2.append(e_DB['l_onda.1'][i])
            abs2.append(e_DB['Abs.1'][i])
            oxi.append(e_DB['Oxigenos'][i])
        
    df_Norm = pd.DataFrame()                                                        # DF con los plamones combinados normalizados
    df_Norm['plasmon_MG']   = plasmon_update    
    df_Norm['Oxigenos']     = oxigeno_update
    e_DB1   = pd.DataFrame()                                                        # DF con la informacion y el tamaño de nuevo DF normalizado
    e_DB1['2theta']       = theta1
    e_DB1['Imax']         = imax1
    e_DB1['2theta.1']     = theta2
    e_DB1['Imax.1']       = imax2
    e_DB1['2theta.2']     = theta3
    e_DB1['Imax.2']       = imax3
    e_DB1['2theta.3']     = theta4
    e_DB1['Imax.3']       = imax4
    e_DB1['2theta.4']     = theta5
    e_DB1['Imax.4']       = imax5
    e_DB1['2theta.5']     = theta6
    e_DB1['Imax.5']       = imax6
    e_DB1['l_onda']       = l_on1
    e_DB1['Abs']          = abs1
    e_DB1['l_onda.1']     = l_on2
    e_DB1['Ans.1']        = abs2
    e_DB1['Oxigenos']     = oxi
    e_DB1['FormQuimica']  = form
    e_DB1['ID']           = id

    c_eps = coef_Silhuoette(df_Norm,1)                                              # Evalua el mejor Coeficiente de Silhuoette
    cluster = DBSCAN(eps=c_eps, min_samples=10).fit(df_Norm[['Oxigenos','plasmon_MG']]) # Aplica DBSCAN 
    etiquetas = cluster.labels_                                                     # Extrae las etiquetas asignadas por DBSCAN
    n_clusters_ = len(set(etiquetas)) - (1 if -1 in etiquetas else 0)               # Numero de grupos 
    silhuoette =  "%0.3f" % metrics.silhouette_score(df_Norm[['Oxigenos','plasmon_MG']], etiquetas) # Evalua el coeficiente de Silhuoette
    print("\n\nDBSCAN")
    print(" Eps: ",c_eps,"\n","No. Clusters: ",n_clusters_,"\n","Coef. Silhuoette: ",silhuoette,"\n")  # Imprime todos los ciclos
    df_DBSCAN = df_Norm.assign(Etiqueta= etiquetas)                                 # Asigna la etiqueta al dataframe de DBSCAN
    df_DBSCAN.drop(df_DBSCAN[(df_DBSCAN['Etiqueta'] == -1)].index, inplace=True)    # Elimina los Outliers del df_DBSCAN
    e_DB_Etiquetados = e_DB1.assign(Etiqueta= etiquetas)                            # Asigna las etiquetas a la base de e_DB_Etiquetados principal
    e_DB_Etiquetados.to_csv('DBSCAN_TP.csv', header=True, index=False)              # Genera el archivo de salida
    generador_grupos(e_DB_Etiquetados)                                              # Genera los grupos y exporta los resultados
    graficador(df_DBSCAN[['plasmon_MG','Oxigenos','Etiqueta']],"Plasmones-Todos", )# Funcion para graficar los grupos
    #print(df_DBSCAN)

############## INICIA EL PROGRAMA ##############
entrada_DB  = pd.read_csv("/Users/arturo/Desktop/Proyecto/Base_de_datos.csv")       # Ingresa la base de e_DB_Etiquetados como un data frame df
entrada_DB.drop(entrada_DB[(entrada_DB['Oxigenos'] >= 7)].index, inplace=True)      # Filtra el df y eliminar los compuestos con mas de 6 oxigenos
entrada_DB.reset_index(inplace = True)                                              # Reinicia el indice del df
entrada_DB.drop(['index'], axis = 'columns', inplace = True)                        # Elimina la columna creada index despues del reinicio del indice
entrada_DB_Temp = entrada_DB[['Abs','l_onda','Abs.1','l_onda.1','Oxigenos','plasmon_MG']]  # Elimina las columnas no necesarias del df

if __name__ == '__main__':                                          # Funcion principal, siempre se ejecuta
    df_normalizada = normalizacion(entrada_DB_Temp)
    #plasmon_mas_Grande(df_normalizada, entrada_DB)
    todos_Plasmones(df_normalizada, entrada_DB)

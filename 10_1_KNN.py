import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import metrics
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
pd.options.mode.chained_assignment = None                   # default='warn'      

def knn(k,base_Datos,nuevoDato):                            # Vecinos mas cercanos del nuevo compuesto
    distancias, posicion    =   [], []                      # Almacena todas las distancias y posiciones de indice
    for i in range(len(base_Datos)):
        dato    = base_Datos[i]
        dis     = distancia_Euclidiana(dato,nuevoDato)      # Llama a la funcion para obtener distancia euclidiana
        distancias.append(dis)
    distancias_tem = distancias.copy()                      # Obtiene una copia de la lista de distancias
    
    for i in range(k):                                      # Obtiene el numero de vecinos k-nn
        dis_min = min(distancias_tem)                       # Extrae el valor minimo de distancias
        indice  = distancias_tem.index(dis_min)             # Posicion de la distancia minima
        posicion.append(indice)                             # Almacenas las posiciones de los vecinos
        distancias_tem[indice] = max(distancias_tem)        # Cambia el valor del vecino para no conflicto
    return distancias, posicion                             # Retorna las distancias y las posiciones de los vecinos

def distancia_Euclidiana(dato,nuevoDato):                   # Funcion para sacar las distancias euclidianas 
    suma = 0
    for i in range(0,14):                                   # Ciclo para obtener la distancia
        productoAtributo      = (dato[i]-nuevoDato[0][i])**2   # Distancia euclidiana
        suma    = suma + productoAtributo                        
    distancia   = np.sqrt(suma)
    return distancia                                        # Retorna la distancia

def graficador_planos(base_Datos,distancia, vecinos,nuevo_Compuesto): # Funcion para graficar los planos cristalograficos
    plt.figure(figsize=(12,7))                              # Tamaño de la grafica
    for i in vecinos:                                       # Obtiene los puntos para el eje X y Y
        x_points, y_points = [], []
        for j in range(0,12,2):                             # Graficador de compuestos
            x_points.append(base_Datos.iloc[i][j])
            y_points.append(base_Datos.iloc[i][j+1])
        plt.plot(x_points, y_points, marker='o',label=str(base_Datos.iloc[i]['FormQuimica'])+':'+str(str(base_Datos.iloc[i]['ID'])))# + ':' + str(distancia[i])) # Graficador
    x_points, y_points = [], []
    for j in range(0,12,2):                                 # Graficador del nuevo compuesto
        x_points.append(nuevo_Compuesto[0][j])
        y_points.append(nuevo_Compuesto[0][j+1])
    plt.plot(x_points, y_points,marker='o',label="KO2"+":"+"2310803") 
    plt.xlabel("2 theta")                                   # Nombre eje X
    plt.ylabel("I max")                                     # Nombre eje Y
    plt.legend()
    plt.show()

def graficador_plasmones(base_Datos,distancia, vecinos,id):
    plt.figure(figsize=(12,7))
    cont=0
    for i in range(len(vecinos)):
        objeto  = pd.read_csv("/Users/arturo/Desktop/Datos/Plasmones_COD/{}.csv".format(base_Datos.loc[vecinos[i]][-2]), names=['l_onda','abs'])
        objeto.drop(objeto[(objeto['l_onda'] <= 200)].index, inplace=True)
        objeto.drop(objeto[(objeto['l_onda'] >= 1000)].index, inplace=True)
        objeto.reset_index(inplace=True)
        xpoints = objeto['l_onda']
        ypoints = objeto['abs']
        plt.plot(xpoints, ypoints,label=str(base_Datos.loc[vecinos[i]]['FormQuimica'])+':'+str(str(base_Datos.loc[vecinos[i]]['ID'])))# + ':' + str(distancia[vecinos[i]]))  #label=str(nomTotal[cont]
        cont += 1 

    objeto1 = pd.read_csv("/Users/arturo/Desktop/validacion/plasmones/{}.csv".format(id), names=['l_onda','abs'])
    #objeto1 = pd.read_csv("/Users/arturo/Desktop/Datos/Plasmones_COD/{}.csv".format(id), names=['l_onda','abs'])
    objeto1.drop(objeto1[(objeto1['l_onda'] <= 200)].index, inplace=True)
    objeto1.drop(objeto1[(objeto1['l_onda'] >= 1000)].index, inplace=True)
    objeto1.reset_index(inplace=True)
    xpoints = objeto1['l_onda']
    ypoints = objeto1['abs']
    plt.plot(xpoints, ypoints,label="KO2"+":"+str(id))  #label=s|tr(nomTotal[cont]
    
    plt.xlabel("wavelength (nm)")
    plt.ylabel("absorbance (a.u.)")
    ax= plt.gca()
    ax.axes.yaxis.set_ticklabels([])
    plt.legend()
    plt.show()





#########-------->   Base de datos    <---------############
entrada_DB  = pd.read_csv("/Users/arturo/Desktop/Proyecto/DBSCAN.csv")       # Ingresa la base de e_DB_Etiquetados como un data frame df
base_Datos = entrada_DB[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1','FormQuimica', 'ID','Etiqueta']]  # Elimina las columnas no necesarias del df
base_Datos.drop(base_Datos[(base_Datos['Etiqueta'] == -1)].index,inplace=True)
base_Datos.reset_index(inplace=True)
base_Datos.drop(['index'], axis='columns', inplace= True)
k = 1
#########-------->   Validación   <---------############
datosValidacion = pd.read_csv("/Users/arturo/Desktop/Proyecto/Base_de_datos_validacion.csv")
datosValidacion = datosValidacion[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']]  # Elimina las columnas no necesarias del df
mean_2 = datosValidacion['l_onda.1'].mean()
datosValidacion.fillna({'l_onda.1': mean_2}, inplace=True)
print(mean_2)
#########-------->   Entrada   <---------############
datos = base_Datos[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']] # Datos sin etiquetar
etiquetas = base_Datos[['Etiqueta']]            # Etiquetas de clase
validacion = [['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']]
compuesto_nuevo  = [[26.5904874923757,40.1065706394414,31.3385905580942,100.0,31.4184699844099,50.0,41.5534468922931,41.7502466981764,44.9099336316066,31.0410009942794,46.4435720171582,24.1295497870938,895.9618454709927,217.035818863844]] # 2310803
#compuesto_nuevo  = [[23.5035288755944,47.3872341234564,26.5351531188492,71.4139226235105,28.4424900744436,76.9489541051423,29.6715019374183,100.0,29.7469296361692,50.0,35.8053550834002,41.0542160861529,884.7121909217377,268.532365167226]] # 1008196
#compuesto_nuevo  =  [[27.20686076,66.63799507,28.57649518,89.13340301,35.73982343,100,35.83163806,50,45.48954735,63.54943879,48.93593118,53.59523076,226.3249607,base_Datos['l_onda.1'].mean()]]
id = 2310803
#########-------->   Normalización   <---------############
normalizacion = preprocessing.MinMaxScaler()                    # Funcion para normalizar
datos = normalizacion.fit_transform(datos)                      # Normalizacion de datos
nuevo = normalizacion.transform(compuesto_nuevo)                # Normalizacion del nuevo dato

#vali  = preprocessing.MinMaxScaler().fit_transform(datosValidacion)
#vali  = pd.DataFrame(vali, columns=['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1'])
#print(vali)

############ Rule of NN   ############
distancia, posicion = knn(k, datos, nuevo)
for i in posicion:
    print(base_Datos.loc[i]['FormQuimica'], base_Datos.loc[i]['ID'],base_Datos.loc[i]['Etiqueta'],distancia[i])
graficador_planos(base_Datos,distancia,posicion,compuesto_nuevo)
graficador_plasmones(base_Datos,distancia,posicion,id)



######   KNN    ######
datos, X_test, etiquetas, y_test = train_test_split(datos, etiquetas, test_size=0.20, stratify=etiquetas) #random_state=42
clasificador = KNeighborsClassifier(n_neighbors=27)             # Clasificador
clasificador.fit(datos,etiquetas)                              
y_pred = clasificador.predict(X_test)
print("Clase: ", clasificador.predict(nuevo))
print("probabilidad: ", clasificador.predict_proba(nuevo))


####### Metricas de evaluacion ########
# Matriz de confusion
matriz = confusion_matrix(y_test,y_pred)
print(matriz)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = matriz, display_labels = None)
cm_display.plot()
plt.show()
# Exactitud
exactitud = accuracy_score(y_test,y_pred)
print("Exactitud: ",exactitud)
# Presición
precision = precision_score(y_test,y_pred,average='macro')
print("Presicion: ",precision)
# Sensibilidad
sensibilidad = recall_score(y_test,y_pred,average='macro')
print("Sensibilidad: ",sensibilidad)
# F1 score
f1 = f1_score(y_test,y_pred,average='macro')
print("f1_Score: ",f1)

###
print(list(y_test["Etiqueta"]))
y = list(y_pred)
print(y)
tn, fp, fn, tp = confusion_matrix(y_test["Etiqueta"], y, labels=[0,1]).ravel()
print(tp,fp,tn,fn)


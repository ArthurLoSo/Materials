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
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
pd.options.mode.chained_assignment = None                   # default='warn'   



def perf_measure(y_test, y_pred):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    y_actual = y_test["Etiqueta"].tolist()
    print(y_actual,y_pred)
    for i in range(len(y_pred)): 
        if y_actual[i]==y_pred[i]==1:
           TP += 1
        if y_pred[i]==1 and y_actual[i]!=y_pred[i]:
           FP += 1
        if y_actual[i]==y_pred[i]==0:
           TN += 1
        if y_pred[i]==0 and y_actual[i]!=y_pred[i]:
           FN += 1
    return(TP, FP, TN, FN)

#########-------->   Base de datos    <---------############
entrada_DB  = pd.read_csv("/Users/arturo/Desktop/Proyecto/DBSCAN.csv")       # Ingresa la base de e_DB_Etiquetados como un data frame df
base_Datos = entrada_DB[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1','FormQuimica', 'ID','Etiqueta']]  # Elimina las columnas no necesarias del df
base_Datos.drop(base_Datos[(base_Datos['Etiqueta'] == -1)].index,inplace=True)
base_Datos.reset_index(inplace=True)
base_Datos.drop(['index'], axis='columns', inplace= True)

#########-------->   Validación   <---------############
datosValidacion = pd.read_csv("/Users/arturo/Desktop/Proyecto/Base_de_datos_validacion.csv")
datosValidacion = datosValidacion[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']]  # Elimina las columnas no necesarias del df
mean_2 = datosValidacion['l_onda.1'].mean()
datosValidacion.fillna({'l_onda.1': mean_2}, inplace=True)


#########-------->   Entrada   <---------############
datos = base_Datos[['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']] # Datos sin etiquetar
etiquetas = base_Datos[['Etiqueta']]            # Etiquetas de clase
validacion = [['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1']]
#########-------->   Normalización   <---------############
normalizacion = preprocessing.MinMaxScaler()                    # Funcion para normalizar
datos = normalizacion.fit_transform(datos)                      # Normalizacion de datos

vali  = preprocessing.MinMaxScaler().fit_transform(datosValidacion)
vali  = pd.DataFrame(vali, columns=['2theta','Imax','2theta.1','Imax.1','2theta.2','Imax.2','2theta.3','Imax.3','2theta.4','Imax.4','2theta.5','Imax.5','l_onda','l_onda.1'])
#print(vali)


######   KNN    ######
datos, X_test, etiquetas, y_test = train_test_split(datos, etiquetas, test_size=0.2, stratify=etiquetas) #random_state=42
clasificador = KNeighborsClassifier(n_neighbors=27)             # Clasificador
clasificador.fit(datos,etiquetas)                              
y_pred = clasificador.predict(X_test)
print(len(y_test))

"""
###### validacion #####
y1_test=[]
for i in range(len(vali)):
    y1_test.append(int(clasificador.predict([list(vali.iloc[i])])))
#vali["Etiqueta"] = y1_test
vali, X_vali, y1_test, y_vali = train_test_split(vali, y1_test, test_size=0.5, stratify=y1_test) #random_state=42
y1_pred =clasificador.predict(X_vali)

"""
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

print(len(y_test),len(y_pred))

TP, FP, TN, FN = perf_measure(y_test, y_pred)

print("TP: ", TP )
print("TN: ", TN )
print("FP: ", FP )
print("FN: ", FN )
"""
matriz = confusion_matrix(y_vali,y1_pred)
print(matriz)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = matriz, display_labels = None)
cm_display.plot()
plt.show()

# Exactitud
exactitud = accuracy_score(y_vali,y1_pred)
print("Exactitud: ",exactitud)
# Presición
precision = precision_score(y_vali,y1_pred,average='macro')
print("Presicion: ",precision)
# Sensibilidad
sensibilidad = recall_score(y_vali,y1_pred,average='macro')
print("Sensibilidad: ",sensibilidad)
# F1 score
f1 = f1_score(y_vali,y1_pred,average='macro')
print("f1_Score: ",f1)


##### cross validation ###3

modelo = DecisionTreeClassifier()
modelo.fit(datos, etiquetas)
resultado = modelo.score(X_test, y_test)
print(resultado)
modelo = DecisionTreeClassifier()
kfold_validacion = KFold(5)
resultados = cross_val_score(modelo, datos, etiquetas, cv = kfold_validacion)
print(resultados)
resultados.mean()


"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.mode.chained_assignment = None  # default='warn'

archivo  = pd.read_csv("/Users/arturo/Desktop/Proyecto/DBSCAN.csv")
#archivo.drop(archivo[(archivo['Etiqueta'] == -1)].index, inplace=True)  # Elimina los datos Atipicos
archivo.reset_index(inplace=True)                                       # Reinicia el indice
n_grupos = max(archivo['Etiqueta']) + 1                                     # Numero de grupos
print(n_grupos)
for n in range(-1,n_grupos,1):
    globals()['grupo%s' % n] = archivo[archivo['Etiqueta']== n]             # Crea y busca variables con la etiqueta correcta
    globals()['grupo%s' % n].drop(['index'], axis='columns', inplace= True) # Elimina columna index 
    globals()['grupo%s' % n].reset_index(inplace=True)                      # Resetea los indices por cada grupo
    globals()['grupo%s' % n].drop(['index'], axis='columns', inplace= True) # Elimina columna index 
    #print(globals()['grupo%s' % n])

for n in range(0,n_grupos,1):
    tam_grupo = len(globals()['grupo%s' % n])
    #print("*********************************")
    for i in range(tam_grupo):
        id_or =  globals()['grupo%s' % n]['ID'][i]
        for j in range(i+1,tam_grupo,1):
            id_com =  globals()['grupo%s' % n]['ID'][j]
            if id_or == id_com:
                globals()['grupo%s' % n].drop([i],axis=0, inplace=True)
                #print(id_or, id_com)
    globals()['grupo%s' % n].reset_index(inplace=True)                      # Resetea los indices por cada grupo
    #print(tam_grupo,len(globals()['grupo%s' % n]))

x_grupo=int(input("Eliga un grupo: "))
n_Elementos=10
print(len(globals()['grupo%s' % x_grupo]))

#######     Filtro grupo   ########
#entrada_DB.drop(entrada_DB[(entrada_DB['Oxigenos'] >= 7)].index, inplace=True)
#globals()['grupo%s' % x_grupo].drop(globals()['grupo%s' % x_grupo][globals()['grupo%s' % x_grupo]['FormQuimica']  'Ag'].index, inplace=True)
#globals()['grupo%s' % x_grupo].reset_index(inplace=True)

########      GRAFICAS     #########
plt.figure(figsize=(12,7))
cont=0
for i in range(len(globals()['grupo%s' % x_grupo])):
    objeto = pd.read_csv("/Users/arturo/Desktop/Datos/Plasmones_COD/{}.csv".format(globals()['grupo%s' % x_grupo]['ID'][i]), names=['l_onda','abs'])
    objeto.drop(objeto[(objeto['l_onda'] <= 200)].index, inplace=True)
    objeto.drop(objeto[(objeto['l_onda'] >= 900)].index, inplace=True)
    objeto.reset_index(inplace=True)
    xpoints = objeto['l_onda']
    ypoints = objeto['abs']
    plt.yticks([])
    plt.plot(xpoints, ypoints)  #label=str(nomTotal[cont]
    cont += 1  
plt.xlabel("Longitud de onda (nm)")
plt.ylabel("Absorbancia")
plt.legend()
plt.show()

#####################################
plt.figure(figsize=(12,7))
cont=0
for i in range(len(globals()['grupo%s' % x_grupo])):
    objeto = pd.read_csv("/Users/arturo/Desktop/Datos/Planos_COD/{}.csv".format(globals()['grupo%s' % x_grupo]['ID'][i]))#, names=['2-theta','I / I max'])
    objeto.reset_index(inplace=True)
    xpoints = objeto['2-theta']
    ypoints = objeto['I / I max']
    plt.plot(xpoints, ypoints)  #label=str(nomTotal[cont], label=str(globals()['grupo%s' % x_grupo]['ID'][i])
    cont += 1
plt.xlabel("2 theta")
plt.ylabel("Imax")
plt.legend()
plt.show()
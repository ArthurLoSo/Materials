""" Programa para eliminar archivos que son inconsistentes despues del scrip perl """
import os                                                       # Importar os
from os import remove                                           # Importar remove de os

plasmones, cif_planos, planos, cif = [], [], [], []             # Variables vacias tipo lista
for filename in os.listdir(r"/Users/arturo/Desktop/Datos/Plasmones_COD"): # Ruta donde se encuentran todas los plasmones
    name = filename                                             # Lee el nombre de cada archivo
    plasmones.append(name)                                      # Agrega el nombre a la variable 

for filename in os.listdir(r"/Users/arturo/Desktop/Datos/Planos_COD"): # Ruta donde se encuentran todas las planos
    name = filename                                             # Lee el nombre de cada archivo
    cif_planos.append(name)                                     # Agrega el nombre a la variable 

for i in range(len(cif_planos)):                                # Ciclo para eliminar los archivos que fueron inconsistentes
    if cif_planos[i] not in plasmones:                          # Comparamos los archivos de los planos y cif contra los plasmones
        planos.append(cif_planos[i])                            # Agrega el nombre de los archivos inconcistentes .csv
        cif.append(cif_planos[i].replace(".csv",".cif"))        # Agrega el nombre de los archivos inconcistentes .cif

for i in range(len(planos)):                                    # Revisa el archivo de inconsistencia
    remove(r"/Users/arturo/Desktop/Datos/Planos_COD/{}".format(planos[i]))    #Elimina el archivo .csv de planos_COD
    remove(r"/Users/arturo/Desktop/Datos/COD/{}".format(cif[i]))#Elimina el archivo .cif de COD
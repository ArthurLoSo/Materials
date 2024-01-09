""" Programa para eliminar archivos que son inconsistentes despues del scrip perl,
    se ejecuta un archivo .txt que contiene las insconsistencias                    """
from os import remove                                           # Importar remove de os
import shutil

archivo= open(r"/Users/arturo/Desktop/Proyecto/recursos/Inconsistencias_planos.txt", 'r')           # Abre el archivo inconsistencias.txt
lineas = archivo.read().splitlines()                            # Fragmenta el archivo en datos

for line in lineas:                                             # Revisa el archivo de inconsistencias
    compuesto =line[-11:]                                       # Busca el nombre del archivo
    #print(compuesto)
    remove(r"/Users/arturo/Desktop/Datos/COD/{}".format(compuesto))     #Elimina el archivo .cif de dioxidos
archivo.close()                                                 # Cierra archivo

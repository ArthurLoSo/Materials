""" Programa para filtrar los compuestos erroneos, si el compuesto no contiene algun metal lo elimina """

import os                                                       # Importar os
from os import remove                                           # Importar remove de os

def main(tarjeta):                                              # Función main
    elementos=[ "Sc",  "Y",   "Ti",  "Zr",  "Hf",  "Rf",  "V",   "Nb",  "Ta",  "Db",  "Cr",  "Mo",
                "W",   "Sg",  "Mn",  "Tc",  "Re",  "Bh",  "Fe",  "Ru",  "Os",  "Hs",  "Co",  "Rh", 
                "Ir",  "Mt",  "Ni",  "Pd",  "Pt",  "Ds",  "Cu",  "Ag",  "Au",  "Rg",  "Zn",  "Cd", 
                "Hg",  "Cn",  "O"]                              # Lista con elementos que deben contener las tarjetas cristalograficas
    caracteres = "1234567890"                                   # El programa no toma en cuenta estos caracteres
    f = open ('Tarjetas_eliminadas_filtro1.txt','a')                           # Crea un archivo que contendra las tarjetas con compuestos no metalicos (borrar en cada ejecución)
    linea1 = open(r"/Users/arturo/Desktop/Datos/COD/{}".format(tarjeta), 'r')  # Abre y lee cada tarjeta 
    Datos1 = linea1.readlines()                                 # Asigna el archivo a Datos1 para posteriormente validar la informacion
    for line in Datos1:                                         # Valida la informacion del compuesto
        if "_chemical_formula_sum" in line:                     # Busca el renglon que contenga la formula quimica
            compuesto1 =line.replace("_chemical_formula_sum"," ") # Reemplaza el texto del renglon
            compuesto1 =compuesto1.replace("","")               #  
            compuesto1 =compuesto1.lstrip().rstrip()            # Quita espacios a la derecha y a la izquierda
            compuesto1 =compuesto1.replace("'","")              #
            compuesto1 =list(compuesto1.split(" "))             # Convierte el compuesto en lista
            if len(compuesto1) == 2:                            # Valida la formula tenga dos elementos
                elemento1 = ''.join([i for i in compuesto1[0] if i not in caracteres])                        # Elemento 1: separo  
                elemento2 = ''.join([i for i in compuesto1[1] if i not in caracteres])                        # Elemento 2: separo
            else:
                elemento1 =compuesto1[0]                        # Elemento 1: solo contiene oxigeno
                elemento2 = " "                                 # Elemento 2: añado cadena vacia para decartar el compuesto
    if elemento1 in elementos and elemento2 in elementos:       # Valida los elementos en la lista 
        #print(tarjeta, "---> ", elemento1,elemento2)           # Control de salida
        pass
    else:                                                      
        #print(tarjeta, "---> ", elemento1,elemento2)           # Control de salida
        f.write("\n" + str(tarjeta))                            # Escribe el archivo erroneo al filtro 
        remove(r"/Users/arturo/Desktop/Datos/COD/{}".format(tarjeta))  #Elimina el archivo .cif con compuesto erroneo
    linea1.close()                                              # Cierra el archivo
    f.close() 


nombres = []                                                    # Variables vacias tipo lista
for filename in os.listdir(r"/Users/arturo/Desktop/Datos/COD"): # Ruta donde se encuentran todas las tarjetas
    name = filename                                             # Lee el nombre de cada tarjeta
    nombres.append(name)                                        # Agrega el nombre a la variable 

if __name__ == '__main__':                                      # Crea una funcion principal
    for i in range(len(nombres)):                               # Ciclo para evaluar cada tarjeta
	    main(nombres[i])                                        # Ejecuta la funcion main()

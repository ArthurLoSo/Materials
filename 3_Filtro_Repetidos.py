""" Programa para filtrar los compuestos repetidos """

import os                                                       # Importar os
from os import remove                                           # Importar remove de os

def main(tarjeta1,tarjeta2,salida1):                            # Función main
    global volumen2, volumen1                                   # Variables globales
    f = open ('Tarjetas_eliminadas_filtro2.txt','a')            # Crea un archivo que contendra las tarjetas con compuestos repetidos eliminados (borrar en cada ejecución)
    linea1 = open(r"/Users/arturo/Desktop/Datos/COD/{}".format(tarjeta1), 'r')  # Abre y lee cada tarjeta 
    Datos1 = linea1.readlines()                                 # Asigna el archivo a Datos1 para posteriormente validar la informacion
    linea2 = open(r"/Users/arturo/Desktop/Datos/COD/{}".format(tarjeta2), 'r')  # Abre y lee cada tarjeta a comparar 
    Datos2 = linea2.readlines()                                 # Asigna el archivo a Datos1 para posteriormente validar la informacion
    for linea in Datos1:                                        # Valida la formula del compuesto
        if "_chemical_formula_sum" in linea:                    # Busca el renglon que contenga la formula quimica
            compuesto1 = linea.replace("_chemical_formula_sum"," ") # Reemplaza el texto del renglon
            compuesto1 = compuesto1.replace("","")                
            compuesto1 = compuesto1.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
            compuesto1 = compuesto1.replace("'","")             
            compuesto1 = list(compuesto1.split(" "))            # Convierte el compuesto en lista
    for linea in Datos2:                                        # Valida la informacion del compuesto
        if "_chemical_formula_sum" in linea:                    # Busca el renglon que contenga la formula quimica
            compuesto2 = linea.replace("_chemical_formula_sum"," ") # Reemplaza el texto del renglon
            compuesto2 = compuesto2.replace("","")                
            compuesto2 = compuesto2.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
            compuesto2 = compuesto2.replace("'","")             
            compuesto2 = list(compuesto2.split(" "))            # Convierte el compuesto en lista
            elemento1  = compuesto2[0]                          # Elemento 1: separo  
            elemento2  = compuesto2[1]                          # Elemento 2: separo
    if elemento1 in compuesto1 and elemento2 in compuesto1:     ### Valida los elementos en la lista del compuesto1. Primer primer filtro de repetidos ###
        for linea in Datos1:                                    # Valida la informacion del compuesto
            if "_cell_volume" in linea:                         # Busca el renglon que contenga el volumen de celda
                volumen1 = linea.replace("_cell_volume"," ")    # Reemplaza el texto del renglon
                volumen1 = volumen1.replace("","")                
                volumen1 = volumen1.replace("_cod_original"," ")
                volumen1 = volumen1.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
                if '(' in volumen1:                             # Si contiene informacion adicional, la elimina
                     for k in range(3):
                        volumen1 = volumen1[:-1]
        for linea in Datos2:                                    # Valida la informacion del compuesto
            if "_cell_volume" in linea:                         # Busca el renglon que contenga el volumen de celda
                volumen2 = linea.replace("_cell_volume"," ")    # Reemplaza el texto del renglon
                volumen2 = volumen2.replace("","")                
                volumen2 = volumen2.replace("_cod_original"," ")
                volumen2 = volumen2.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
                if '(' in volumen1:                             # Si contiene informacion adicional, la elimina
                     for k in range(3):
                        volumen2 = volumen2[:-1]
        if volumen1 == volumen2:                                ### Valida que el volumen sea igual. Segundo filtro de repetidos ###
            for linea in Datos1:                                # Valida la informacion del compuesto
                if "_cell_angle_alpha " in linea:               # Busca el renglon que contenga el angulo alpha
                    alpha1 = linea.replace("_cell_angle_alpha "," ") # Reemplaza el texto del renglon
                    alpha1 = alpha1.replace("","")                
                    alpha1 = alpha1.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
                    if '(' in alpha1:                           # Si contiene informacion adicional, la elimina
                        for k in range(3):
                            alpha1 = alpha1[:-1]
            for linea in Datos1:                                # Valida la informacion del compuesto
                if "_cell_angle_beta" in linea:                 # Busca el renglon que contenga el angulo beta
                    beta1 = linea.replace("_cell_angle_beta"," ") # Reemplaza el texto del renglon
                    beta1 = beta1.replace("","")                  
                    beta1 = beta1.lstrip().rstrip()             # Quita espacios a la derecha y a la izquierda
                    if '(' in beta1:                            # Si contiene informacion adicional, la elimina
                        for k in range(3):
                            beta1 = beta1[:-1]
            for linea in Datos1:                                # Valida la informacion del compuesto
                if "_cell_angle_gamma" in linea:                # Busca el renglon que contenga el angulo gamma
                    gamma1 = linea.replace("_cell_angle_gamma"," ") # Reemplaza el texto del renglon
                    gamma1 = gamma1.replace("","")                
                    gamma1 = gamma1.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
                    if '(' in gamma1:                           # Si contiene informacion adicional, la elimina
                        for k in range(3):
                            gamma1 = gamma1[:-1]
            for linea in Datos2:                                # Valida la informacion del compuesto
                if "_cell_angle_alpha " in linea:               # Busca el renglon que contenga el angulo alpha
                    alpha2 = linea.replace("_cell_angle_alpha "," ")  # Reemplaza el texto del renglon
                    alpha2 = alpha2.replace("","")                
                    alpha2 = alpha2.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
                    if '(' in alpha2:                           # Si contiene informacion adicional, la elimina
                        for k in range(3):
                            alpha2 = alpha2[:-1]
            for linea in Datos2:                                # Valida la informacion del compuesto
                if "_cell_angle_beta" in linea:                 # Busca el renglon que contenga el angulo beta
                    beta2 = linea.replace("_cell_angle_beta"," ") # Reemplaza el texto del renglon
                    beta2 = beta2.replace("","")                  
                    beta2 = beta2.lstrip().rstrip()             # Quita espacios a la derecha y a la izquierda
                    if '(' in beta2:                            # Si contiene informacion adicional, la elimina
                        for k in range(3):
                            beta2 = beta2[:-1]
            for linea in Datos2:                                # Valida la informacion del compuesto
                if "_cell_angle_gamma" in linea:                # Busca el renglon que contenga el angulo gamma
                    gamma2 = linea.replace("_cell_angle_gamma"," ") # Reemplaza el texto del renglon
                    gamma2 = gamma2.replace("","")                
                    gamma2 = gamma2.lstrip().rstrip()           # Quita espacios a la derecha y a la izquierda
                    if '(' in gamma2:                           # Si contiene informacion adicional, la elimina
                        for k in range(3):
                            gamma2 = gamma2[:-1]
            if alpha1 == alpha2 and beta1 == beta2 and gamma1 == gamma2:  ### Valida que los angulos sean iguales. Tercer filtro de repetidos ###
                if tarjeta2 not in salida1:                     # Si la tarjeta2 no se encuentra en la 'salida1', se agrega como elemento a dicha variable
                        salida1.append(tarjeta2)                # Agrega la tarjeta2 a salida1 para evitar repetir tarjetas en la salida
                        f.write("\n" + str(tarjeta2))           # Escribe el archivo erroneo al filtro2
                        #print(tarjeta2)                         # Control de salida
    linea1.close()                                              # Cierra el archivo
    linea2.close()                                              # Cierra el archivo
    f.close()


nombres, salida1 = [], []                                       # Variables vacias tipo lista
for filename in os.listdir(r"/Users/arturo/Desktop/Datos/COD"): # Ruta donde se encuentran todas las tarjetas
    name = filename                                             # Lee el nombre de cada tarjeta
    nombres.append(name)                                        # Agrega el nombre a la variable 

if __name__ == '__main__':                                      # Crea una funcion principal  
	for i in range(0,len(nombres)-1,1):                         # Ciclo para obtener la primera tarjeta
            for j in range(i+1,len(nombres),1):                 # ciclo para obtener las tarjetas restantes 
                main(nombres[i], nombres[j],salida1)            # Ejecuta la funcion main()

for tarjeta in salida1:                                         # ciclo para eliminar los compuestos con estructuras repetidas
    remove(r"/Users/arturo/Desktop/Datos/COD/{}".format(tarjeta))  #Elimina el archivo .cif con compuesto repetido
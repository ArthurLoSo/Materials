""" Crea la vista minable en forma de base de datos """

import os                                                           # Importar os
import numpy as np
def main():
    nombres, nombresCIF, nombresCSV  = [], [], []                   # Variables vacias tipo lista, contiene los nombres con extenciones CIF y CSV
    for filename in os.listdir(r"/Users/arturo/Desktop/Datos/Planos_COD"):  # Ruta donde se encuentran todas las tarjetas para obtener el nombre de los compuestos
        name = filename                                             # Lee el nombre de cada CSV
        nombres.append(name)                                        # Agrega el nombre a la variable 
    nombresCSV = list(nombres)                                      # Copia la lista original
    for i in range(len(nombres)):
        nombresCIF.append(nombres[i].replace('.csv', '.cif'))       # Cambia la extencion por CIF
        nombres[i] = nombres[i].replace('.csv', '')                 # Elimina la extencion
    return nombres, nombresCIF, nombresCSV                          # Retorna las tres listas

def formula_quimica():                                              # Buscar el nombre del compuesto
    compuestos = []
    for i in range(len(nombresCIF)):                                # Ciclo para validar cada tarjeta cristalografica
        linea = open(r"/Users/arturo/Desktop/Datos/COD/{}".format(nombresCIF[i]), 'r')   # Abre y lee cada tarjeta 
        Datos = linea.readlines()                                   # Asigna el archivo a Datos para posteriormente validar la informacion
        for line in Datos:                                          # Lee cada linea del archivo
            if "_chemical_formula_sum" in line:                     # Busca el renglon que contenga la formula quimica
                formula = line.replace("_chemical_formula_sum"," ") # Reemplaza el texto del renglon
                formula = formula.replace("","")
                formula = formula.lstrip().rstrip()                 # Quita espacios a la derecha y a la izquierda
                formula = formula.replace("'","")
                formula = list(formula.split(" "))                  # Convierte el compuesto en lista
                if "O" in formula[0]:                               # Coloca la formula en orden correcto
                    formula = str(formula[1])+str(formula[0])
                else:
                    formula = str(formula[0])+str(formula[1])
        linea.close()                                               # Cierra el archivo
        compuestos.append(formula)                                  # Contiene la lista de las formulas quimicas
    return compuestos                                               # Retorna la variable de compuestos que contiene la formula quimica

def planos_cristalograficos():                                      # Planos Cristalograficos
    salidaPicos, picosIncompletos = [], []                          # Almacena los archivos que contienen los picos que los requeridos
    for i in range(len(nombresCSV)):
        linea = open(r"/Users/arturo/Desktop/Datos/Planos_COD/{}".format(nombresCSV[i]), 'r')
        Datos = linea.readlines()
        Datos.pop(0)                                                # Elimina el encabezado
        picos_completos = []
        for line in Datos:                                          # Hace el tratamiento de los picos
            picos = line.split(",")                                 # Convierte en lista cada renglon del archivo   
            picos = [float(picos[0]),float(picos[1].replace("\n",""))] # Elimina "\n"
            picos_completos.append(picos)                           # Crea una lista de todos los picos
        if len(picos_completos)>6:
            while len(picos_completos) > 6:                         # Ciclo para limitar el numero de picos
                max=100                                             # Variable para comparar la primera iteracion
                for k in range(len(picos_completos)):               # Ciclo de para buscar y reducir los picos mas pequeños
                    temp     = picos_completos[k]                   # Extrae el primer conjunto de picos
                    imax     = temp[1]                              # Contiene el Imax de cada conjunto
                    if imax <= max:                                 # Condicion para eliminar el conjunto de picos minimos
                        max  = imax                                 # Picos eliminados
                        pos  = k                                    # Posicion del pico a eliminar
                picos_completos.pop(pos)                            # Eliminacion del pico 
        elif len(picos_completos) < 6:                              # Guarda los nombres que tienen menos picos solicitados
            picosIncompletos.append(nombresCSV[i])                  # Acumula los nombres con menos picos
        salidaPicos.append(picos_completos)                         # Acumula los picos de cada archivo
        linea.close() 
    return salidaPicos                                              # Salida con picos cristalograficos homogeneos                                    

def plasmones():
    incon_plas, salidaPlas = [], []                                 # Variable que contiene las posiciones que no contienen plamones y la salida de plasmones
    for i in range(len(nombresCSV)):                                # Ciclo para validar los plamones
        linea = open(r"/Users/arturo/Desktop/Datos/Plasmones_COD/{}".format(nombresCSV[i]), 'r')
        Datos = linea.readlines()                                   # Lee el archivo
        pos, linea_tem  = [], []                                    # Variables temporales
        temp, max, min = 0, 0, 0                                    # Variables temporales
        for line in Datos:                                          # Ciclo para tratar los plasmones
            plas = line.split(",")                                  # Convierte en lista cada renglon del archivo   
            plas = [float(plas[0]),float(plas[1].replace("\n",""))] # Covierte en flotante los datos
            if plas[0] >= 200 and plas[0] <= 900:                  # Condicional para control de longitud de onda
                if plas[1] == 0:                                    # Reset a las variables
                    temp, max, min = 0, 0, 0
                elif plas[1] > temp:                                # Obtiene los plasmones minimos
                    if min != 0:
                        min = 0
                        #pos.append(linea_tem)                      # Almacena los valles de la curva
                    temp      = plas[1]
                    linea_tem = plas
                    max       = 1
                elif plas[1]  < temp:                               # Obtiene los plasmones minimos
                    if max   != 0:
                        max   = 0
                        pos.append(linea_tem)                       # Almacena los plasmones (crestas de la curva)
                    temp      = plas[1]
                    linea_tem = plas
                    min       = 1
        if len(pos) == 0:                                           # Obtine las posiciones con cero plasmones
            nombre_tem    = nombresCSV[i]
            nombre_indice = nombresCSV.index(nombre_tem)
            incon_plas.append(nombre_indice)
        elif len(pos) <= 2:                                         # Si tiene menos o igual plasmones que se indiquen
            salidaPlas.append(pos)
        elif len(pos)  > 2:                                         # Si tiene mas picos elimina los mas bajos hasta homogeinizar 
            while len(pos) > 2:
                min_pos = pos[0]                                    # Elimina el plasmon con longitud de onda mas grande
                indice  = pos.index(min_pos)
                pos.pop(indice)
            salidaPlas.append(pos)                                  # Salida de plasmones
        linea.close()
    return salidaPlas, incon_plas                                   # Salida con plasmones

def contadorOxigeno(compuestos):                                    # Funcion para revisar el numero de oxigenos del compuesto
    oxigenos=[]
    for i in range(len(compuestos)):                                # Recorre cada compuesto
        temp        = "".join(reversed(compuestos[i]))
        posicion    = temp.find("O")
        temp1   = temp[0:posicion:1]                                # Busca el numero de oxigenos
        temp2 = "".join(reversed(str(temp1)))
        if temp2 == '':
            temp2 = '1'
        oxigenos.append(temp2)
    #print(len(oxigenos))
    return oxigenos                                                 # Retorna una lista con el numero de oxigenos de cada compuesto

def plasmon_mas_grande(plasmones):
    plasmon_MG =[]
    for i in range(len(plasmones)):
        plasmon = plasmones[i]
        try:
            longitud_1  = float(plasmon[0][0])
        except:
            longitud_1  = 0
        try:
            longitud_11 = float(plasmon[0][1])
        except:
            longitud_11 = 0
        try:
            longitud_2  = float(plasmon[1][0])
        except:
            longitud_2  = 0
        try:
            longitud_22 = float(plasmon[1][1])
        except:
            longitud_22 = 0
        vector1     = [longitud_11,longitud_22]
        plasmon_max = max(vector1)
        indice = vector1.index(plasmon_max)
        if indice == 0:
            plasmon_MG.append(longitud_1)
        elif indice == 1:
            plasmon_MG.append(longitud_2)
    return plasmon_MG 

def generador_BD(compuestos,salidaPicos,salidaPlas,nombres,oxigenos,plasmon_MG):
    f = open ('Base_de_datos.csv','w')                              # Crea un archivo que almacenara la base de datos
    encabezado = str("2theta,Imax,2theta,Imax,2theta,Imax,2theta,Imax,2theta,Imax,2theta,Imax,l_onda,Abs,l_onda,Abs,Oxigenos,plasmon_MG,FormQuimica,ID")
    f.write(encabezado)                                             # Escribe el encabezado en la base de datos
    for i in range(len(salidaPicos)):                               # Ciclo para crear el tamaño de la base de datos
        s = str('')                                                 # Variable que contendra cada observación
        for j in range(len(salidaPicos[i])):                        # Ciclo para planos cristalograficos
            x1 = str(salidaPicos[i][j][0])                          # 2 theta
            x2 = str(salidaPicos[i][j][1])                          # I max
            s += x1 + ',' + x2 + ','                                # Observacion editada planos cristalograficos
        if len(salidaPlas[i]) == 2:                                 # Ciclo para plasmones   
            for k in range(len(salidaPlas[i])):                     
                x3 = str(salidaPlas[i][k][0]) if salidaPlas[i][k][0]<=950  else ""                   # Longitud de onda (nm)
                x4 = str(salidaPlas[i][k][1]) if salidaPlas[i][k][0]<=950  else ""                      # Absortion
                s += x3 + ',' + x4 + ','                            # Observacion editada plasmones
        else:
            cont = len(salidaPlas[i])
            for k in range(len(salidaPlas[i])):
                x3 = str(salidaPlas[i][k][0]) if salidaPlas[i][k][0]<=950  else ""
                x4 = str(salidaPlas[i][k][1]) if salidaPlas[i][k][0]<=950  else ""
                s += x3 + ',' + x4 + ','
            while cont < 2:                                         # Homogeniza los plasmones para que la base de datos tenga el mismo tamaño
                x3 = ""
                x4 = ""
                s += x3 + ',' + x4 + ','                            # Observacion editada plasmones
                cont += 1
        x5 = str(oxigenos[i])                                       # Numero de oxigenos
        x8 = str(plasmon_MG[i])
        x6 = str(compuestos[i])                                     # Formula quimica
        x7 = str(nombres[i])                                        # Nombre cif
        s += x5 + ',' + x8 + ',' + x6 + ',' + x7                               # Observacion editada formula quimica y CIF
        f.write("\n" + str(s))                                      # Ecribe la observación
    f.close()
    return "Base de datos finalizada"

if __name__ == '__main__':                                          # 
    nombres, nombresCIF, nombresCSV = main()
    compuestos                      = formula_quimica() 
    salidaPicos                     = planos_cristalograficos()
    salidaPlas, incon_plas          = plasmones()
    oxigenos                        = contadorOxigeno(compuestos)
    plasmon_MG                      = plasmon_mas_grande(salidaPlas)
    for data in reversed(incon_plas):                               # Elimina las inconsistencias en las salidas anteriores a plasmon
        oxigenos.pop(data)
        compuestos.pop(data)
        salidaPicos.pop(data)
        nombres.pop(data)
        nombresCIF.pop(data)
        nombresCSV.pop(data)  
    terminar=generador_BD(compuestos,salidaPicos,salidaPlas,nombres,oxigenos,plasmon_MG)
    print(terminar)

"""	Este archivo buscara en la pagina de COD los compuestos y descarga el archivo 
	'COD-selection' que contiene la ruta de cada compuesto """

from selenium import webdriver                          # Importar selenium  
from selenium.webdriver.common.keys import Keys         # Importar las Keys para validar cada comando
from selenium.webdriver.chrome.options import Options   # Importar options de webdriver
import time                                             # Importar time

def main(elem,min,max):                                 # Funcion para configurar las opciones
    chromeOptions = Options()                           # Asignar Opciones() a chromeOptions
    chromeOptions.add_experimental_option("prefs",{
        "download.default_directory" : r"/Users/arturo/Desktop/Datos"})   # Ruta para descargar el archivo
    driver = webdriver.Chrome(executable_path = r"/Users/arturo/Desktop/Proyecto/recursos/chromedriver",
        chrome_options = chromeOptions)                 # Ruta donde se encuentra chromedriver(descargar desde google)                                   
    driver.get("http://www.crystallography.net/cod/")   # Ingresa a la pagina web
    search1=driver.find_element('xpath',"//html/body/div/div[4]/ul/li[2]/ul/li[2]/a") # Ruta de boton de pagina web
    search1.click()                                     # Hace clic en boton de pagina
    entrada1=driver.find_element('xpath',"//html/body/div/div[5]/div[1]/form[3]/table/tbody/tr[11]/td/input[1]") # Ruta de cuadro de texto
    entrada1.send_keys(elem)                            # Ingresa texto, compuestos que contengan oxigeno
    entrada3=driver.find_element('xpath',"//html/body/div/div[5]/div[1]/form[3]/table/tbody/tr[14]/td/input[1]") # Ruta de cuadro de texto
    entrada3.send_keys(min)                             # Ingresa texto min de elementos
    entrada4=driver.find_element('xpath',"//html/body/div/div[5]/div[1]/form[3]/table/tbody/tr[14]/td/input[2]") # Ruta de cuadro de texto
    entrada4.send_keys(max)                             # Ingresa texto max de elementos
    search2=driver.find_element('xpath',"//html/body/div/div[5]/div[1]/form[3]/table/tbody/tr[16]/td/input") # Ruta de boton
    search2.click()                                     # Hace clic en boton de pagina sends
    descarga1=driver.find_element('xpath',"//html/body/div/div[5]/p[1]/a[4]") # Ruta de boton de pagina web
    descarga1.click()                                   # Hace clic en boton para descargar el archivo que contiene los compuestos en formato zip
    time.sleep(120)                                     # Tiempo de descarga de archivo (segun velocidad de internet)

elem = "O"                                              # Elemento buscado (compuestos con oxigeno)
min  = "1"                                              # Minimo de elementos en el compuesto
max  = "2"                                              # Maximo de elementos en el compuesto

if __name__ == '__main__':                              # Crea una funcion principal
	main(elem,min,max)                                  # Ejecutamos la funcion main()
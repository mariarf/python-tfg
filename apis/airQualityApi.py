import requests
import json
import os
from urllib.request import urlopen

#if _name_ =='_airQualityApi_':
url= 'https://api.waqi.info/feed/newyork/?token=c889c21d8944202ace2d717bb97db9ab84160449'
response=requests.get(url)
print(response)
print("pepeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
if response.status_code == 200:


    #colocando en json para acceder a una variable con json
    
    response_json = json.loads(response.text)
    city = response_json["data"]["city"]["name"]
    print(city)
    
    #se concadenan las variables y [2] seria entrando al 3er parametro de o3
    data = response_json["data"]["forecast"]["daily"]["o3"][0]
    print("pepeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    
    """
    #colocando en json para acceder a una variable con request
    response_json = response.json()  #esto es un diccionario
    status = response_json["status"]
    print(status)
    """

    #guardando datos de la pagina en un archivo de escritura binaria
    #import os

    current_dir = os.getcwd().split("\TFG")[0] 
    filename = current_dir + "/TFG/pruebas_maria/pepe.csv"

    content = response.content
    
    file = open(filename,'wb')
    file.write(content)
    file.close()
    

    def probandoAPI():
        #MÉTODO DE PRUEBA PARA PROBAR A UTILIZAR LAS API

        #response = requests.get("https://aqicn.org/city/usa/newyork/")
        response = urlopen("https://aqicn.org/city/usa/newyork/")
        #text = json.dumps(response,sort_keys=True, indent=4)
        #print(text)
        html_bytes = response.read()
        html = html_bytes.decode("utf-8")
        print(html)
        #print(response.json())
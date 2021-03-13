import requests
import json

#if _name_ =='_airQualityApi_':
url= 'https://aqicn.org/snapshot/usa/newyork/20210313-16/?cs'
response=requests.get(url)
print(response)
if response.status_code == 200:


    #colocando en json para acceder a una variable con json
    """
    response_json = json.loads(response.text)
    city = response_json["data"]["city"]["name"]
    print(city)
    #se concadenan las variables y [2] seria entrando al 3er parametro de o3
    data = response_json["data"]["forecast"]["daily"]["o3"][2]
    print(data)
    """
"""
    #colocando en json para acceder a una variable con request
    response_json = response.json()  #esto es un diccionario
    status = response_json["status"]
    print(status)
"""
"""
    #guardando datos de la pagina en un archivo de escritura binaria
    content = response.content
    file = open('nombrearchivo de escritura binaria','wb')
    file.write(content)
    file.close()
"""
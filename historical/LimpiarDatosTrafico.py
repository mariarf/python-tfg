
import csv
import datetime
from pathlib import Path
#import requests
import json
from urllib.request import urlopen
import os


def acotarDatosNY(): 

    #ESTE MÉTODO ES PARA COGER LOS DATOS DEL .CSV DE TRÁFICO INICIAL Y ACOTARLOS A SÓLO LOS DATOS DE MANHATTAN, QUE SERÁN LOS UTILIZADOS PARA EL TFG

 
    data_folder = Path(os.getcwd().split("\TFG")[0] + "/TFG/originals")
    file_to_open = data_folder + "/DOT_Traffic_Speeds_NBE.csv"
    #file_to_open = data_folder / "condicionesClimaticas.csv"

    data_result = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"

    with open(file_to_open) as csv_file:
        with open(data_result, mode='w', newline='') as salida:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rellenarSalida = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            manhattan_counter = 0
            for row in csv_reader:
                if row[11] == 'Manhattan':
                    rellenarSalida.writerow(row)
                    manhattan_counter +=1 
                line_count += 1
                if line_count%1000000==0:
                    print(f'{line_count}')
                
                
            print(f'Processed {line_count} lines.')
            print(f'Total Manhattan: {manhattan_counter}')
            
def diaSemana(año,mes,dia):
    #ESTE MÉTODO DEVUELVE EL DÍA DE LA SEMANA DADO EL AÑO, MES Y DÍA
    week_days=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    week_num=datetime.date(año,mes,dia).weekday()
    return(week_days[week_num])

def columnasAcotadas():
    #ESTE MÉTODO UTILIZA EL FICHERO QUE SE CREÓ EN EL ACOTARDATOSNY() PARA COGER Y PREPARAR LAS FILAS QUE HARÁN FALTA DEL FICHERO DE TRÁFICO.
    
    file_to_open =  os.getcwd().split("\TFG")[0] + "/TFG/historical_data/salidaManhattan.csv"
    data_result = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/UnionManhattan.csv"

    with open(file_to_open) as csv_file:
        with open(file_to_open, mode='r', newline='') as csv_file1:
            with open(data_result, mode='w', newline='') as salida:
                csv_reader = csv.reader(csv_file, delimiter=',')
                rellenarSalida = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                line_count = 0
                columnas_acotadas=["ID", "Speed" , "TravelTime", "Status", "Date", "Time", "Weekday" , "Borough", "Link_name"]
                #rellenarSalida.writerow(columnas_acotadas)
                for row in csv_reader:
                    
                    
                    fecha_split=row[4].split(" ")

                    dia_split=fecha_split[0].split("/")[1] + "/" + fecha_split[0].split("/")[0] + "/" + fecha_split[0].split("/")[2]
                   
                    hora_split=fecha_split[1] + " " + fecha_split[2]
                    fecha_año=int(dia_split.split("/")[2])
                    fecha_dia=int(dia_split.split("/")[0])
                    fecha_mes=int(dia_split.split("/")[1])

                    #Esto es porque hay unos registros de 1978 que no se utilizarán. Hay que evitar que aparezcan 
                    if fecha_año != 1978:
                        columnas_acotadas[0]=row[0]
                        columnas_acotadas[1]=row[1]
                        columnas_acotadas[2]=row[2]
                        columnas_acotadas[3]=row[3]
                        columnas_acotadas[4]=dia_split
                        columnas_acotadas[5]=hora_split
                        columnas_acotadas[6]=diaSemana(fecha_año,fecha_mes,fecha_dia)
                        columnas_acotadas[7]=row[11]
                        columnas_acotadas[8]=row[12]
                        rellenarSalida.writerow(columnas_acotadas)
                    else: 
                        
                        continue
                    
                    
                    if line_count%100000==0:
                        print(line_count)
                    line_count += 1
                    
                print(f'Processed {line_count} lines.')


            
def unirContaminacion():
    #ESTE MÉTODO UNE EL FICHERO RESULTANTE DEL MÉTODO COLUMNASACOTADAS() AL FICHERO DE CONTAMINACIÓN, UNIENDO LA CONTAMINACIÓN DE CADA UNA DE LAS FILAS
    #DEL FICHERO A LA CONTAMINACIÓN CORRESPONDIENTE EN ESE DÍA
    
    data_folder = Path(os.getcwd().split("\TFG")[0] + "/TFG/originals")
    fileContaminacion = data_folder / "calidadAire.csv"
    line_count=0
    file_to_open = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/UnionManhattan.csv"
    data_result = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/Traffic+AirQuality.csv"


    with open(file_to_open, mode='r', newline='') as csv_file:
            with open(data_result, mode="w", newline='') as salida:
                csv_reader = csv.reader(csv_file, delimiter=',')
                
                rellenarSalida = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                for row in csv_reader:
                    
                    with open(fileContaminacion, mode="r", newline='') as csv_contaminacion:
                        contaminacion_reader = csv.reader(csv_contaminacion, delimiter=',')

                        for filaContaminacion in contaminacion_reader:
                            
                            fechaSplit=filaContaminacion[0].split("/")
                            año=fechaSplit[0]   
                            mes=fechaSplit[1]
                            dia=fechaSplit[2]
                            valorContaminacion = filaContaminacion[1]
                            #print(valorContaminacion)

                            if len(mes) == 1:
                                mes = "0" + mes
                            
                            if len(dia) == 1:
                                dia = "0" + dia
                            
                            fechaContaminacion= dia + "/" + mes +"/" + año

                            if fechaContaminacion == row[4]:
                                row.insert(len(row),fechaContaminacion)
                                row.insert(len(row),valorContaminacion)
                                rellenarSalida.writerow(row)
                                #print("llegó")
                                if line_count%100000==0:
                                    print(line_count)
                                line_count+=1
                                break
                #print(f'Processed {line_count} lines.')            
                        
                        
def numeroLineasArchivo(ruta, nombrearchivo):
    #DADA UNA RUTA Y EL NOMBRE DEL ARCHIVO, DEVUELVE EL NÚMERO DE LÍNEAS TOTALES DEL FICHERO. SE CREÓ PARA INTENTAR REALIZAR EL 
    #ÁRBOL BINARIO DE BÚSQUEDA, PARA EL QUE SE NECESITA SABER EL TAMAÑO DEL ARCHIVO.
    data_folder = Path(ruta)
    fileContaminacion = data_folder / nombrearchivo
    file = open(fileContaminacion)
    reader = csv. reader(file)
    lines= len(list(reader))
    print(lines)
    return lines

def arbolUnionContaminacion():

    #MÉTODO EN PROCESO - INTENTAR CREAR UN ÁRBOL BINARIO DE BÚSQUEDA QUE SIRVA COMO ALTERNATIVA AL MÉTODO UNIRCONTAMINACION() Y QUE SE EJECUTE COMPLETAMENTE EN UN ORDEN 
    #LOGARÍTMICO MUCHÍSIMO MENOR AL TARDADO POR EL OTRO MÉTODO - ADEMÁS PODRÍA SERVIR COMO BASE PARA HACER EL MÉTODO DE UNIÓN DEL .CSV AL FICHERO DE DATOS DEL CLIMA. 
    data_folder = Path(os.getcwd().split("\TFG")[0] + "/TFG/originals")
    nombrearchivo = "calidadAire.csv"
    fileContaminacion = data_folder + "/calidadAire.csv"
    line_count=0
    
    numLineas = numeroLineasArchivo(data_folder, nombrearchivo)
    
    file_to_open = os.getcwd().split("\TFG")[0] + "/TFG/historical_data/UnionManhattan.csv"
    data_result = os.getcwd().split("\TFG")[0] + "/TFG/pruebas_juanma/unidosArbol.csv"
    
    with open(file_to_open, mode='r', newline='') as csv_file:
            with open(data_result, mode="w", newline='') as salida:
                csv_reader = csv.reader(csv_file, delimiter=',')
                
                rellenarSalida = csv.writer(salida, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                file_variable = open(fileContaminacion)
                all_lines_variable = file_variable.readlines()
                numeroLineaIntermedia = int((numLineas - 1)/2)
                añoIntermedio = all_lines_variable[numeroLineaIntermedia].split(",")[0].split("/")[0] 
                print(all_lines_variable[numeroLineaIntermedia])
                mes = "0" + all_lines_variable[numeroLineaIntermedia].split(",")[0].split("/")[1]
                print(all_lines_variable[numeroLineaIntermedia].split(",")[0].split("/")[1])
                print(mes)

                for row in csv_reader:

                    #with open(fileContaminacion, mode="r", newline='') as csv_contaminacion:

                    #contaminacion_reader = csv.reader(csv_contaminacion, delimiter=',')

                    if row[4].split("/")[2]==añoIntermedio: #mismo año
                        print(row[4])
                        if row[4].split("/")[1] == mes: #mismo mes
                            print("mismo mes")
                            break
                        
                    else:
                        if row[4].split("/")[2] > añoIntermedio:
                            continue
                        else:
                            continue

                        #print(row[4])
                        """
                        for filaContaminacion in contaminacion_reader:
                            
                            fechaSplit=filaContaminacion[0].split("/")
                            año=fechaSplit[0]   
                            mes=fechaSplit[1]
                            dia=fechaSplit[2]
                            valorContaminacion = filaContaminacion[1]
                            #print(valorContaminacion)

                            if len(mes) == 1:
                                mes = "0" + mes
                            
                            if len(dia) == 1:
                                dia = "0" + dia
                            
                            fechaContaminacion= dia + "/" + mes +"/" + año

                            if fechaContaminacion == row[4]:
                                row.insert(len(row),fechaContaminacion)
                                row.insert(len(row),valorContaminacion)
                                rellenarSalida.writerow(row)
                                #print("llegó")
                                if line_count%100000==0:
                                    print(line_count)
                                line_count+=1
                                break
                            """
                #print(f'Processed {line_count} lines.')    
        
def comprobarRelleno(ruta,archivo):
    #MÉTODO QUE SE HA CREADO PARA COMPROBAR SI TODOS LOS DATOS HAN SIDO RELLENADOS CORRECTAMENTE/ NO HAY NINGUNA FILA QUE SE HAYA QUEDADO VACÍA
    data_folder = Path(ruta)
    csvComprobar = data_folder / archivo
    
    with open(csvComprobar, mode="r", newline='') as csv_comprobar:
        csv_reader = csv.reader(csv_comprobar, delimiter=',')

        for row in csv_reader:
            if (len(row[10])<2):
                print(row)
    
def listaCallesDistintas():
    #LISTADO DE CALLES DISTINTAS QUE UTILIZA LA API DE TRÁFICO PARA EL DISTRITO DE MANHATTAN - 
    # EL RESULTADO DE LA EJECUCIÓN DA 35 CALLES ÚNICAS.
    with open("unidos1.csv", mode="r", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        streets = set(map(lambda row: row[8], csv_reader))
        print(streets)
        print(len(streets))

 

            
                
    
#columnasAcotadas()

#unirContaminacion()

#probandoAPI()

#arbolUnionContaminacion()

#comprobarRelleno("","unidos1.csv")

#listaCallesDistintas()

prueba()
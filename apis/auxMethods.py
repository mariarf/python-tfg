import datetime, os
import pandas as pd

## metodo que agrega en historical el contenido de new, las cabeceras deben coincidir
def apiHistoricalData(new, historical):

    #RESULTADO DE COLUMNASACOTADAS/FORMAT
    file_to_open = os.getcwd().split("\TFG")[0] + f"/TFG/apis_data/{new}" 
    #EL HISTORICO DE DATOS DE LA API 
    data_result = os.getcwd().split("\TFG")[0] + f"/TFG/apis_data/{historical}"

    results_DI = pd.read_csv(file_to_open)
    results_AH = pd.read_csv(data_result)
    results_AH = pd.concat([results_AH,results_DI])

    print(results_AH)
    results_AH.to_csv(data_result, index=False)

def weekDay(year,month,day):
    week_days=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    week_num=datetime.date(year, month, day).weekday()
    return(week_days[week_num])


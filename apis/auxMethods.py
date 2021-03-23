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



def timeFormat(time):
    #format 00:00:00 to 00:00:00 PM
    hour = int(time.split(":")[0])
    minuts = time.split(":")[1]
    seconds= time.split(":")[2]

    if hour >= 00 and hour < 12 :
        var = "AM"
    else:
        var = "PM"
        if hour == 13:
            hour = "01"
        if hour == 14:
            hour = "02"
        if hour == 15:
            hour = "03"
        if hour == 16:
            hour = "04"
        if hour == 17:
            hour = "05"
        if hour == 18:
            hour = "06"
        if hour == 19:
            hour = "07"
        if hour == 20:
            hour = "08"
        if hour == 21:
            hour = "09"
        if hour == 22:
            hour = "10"
        if hour == 23:
            hour = "11"     
    
    time = str(hour) + ":" + minuts + ":" + seconds + var
    return time


def dateOrderSeries(date):
    #mm/dd/yyyy to yyyy/mm/dd for Series
    split_Date = date.str.split("/")
    date = split_Date.str.get(2) + "/" + split_Date.str.get(0) + "/" + split_Date.str.get(1)
    return date


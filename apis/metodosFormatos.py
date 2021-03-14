import datetime

def diaSemana(año,mes,dia):
    week_days=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    week_num=datetime.date(año,mes,dia).weekday()
    return(week_days[week_num])

def horaFormato(time):
    #format 00:00:00.000 to 00:00:00 PM
    hora = int(time.split(":")[0])
    minutos = time.split(":")[1]
    segundos = time.split(":")[2].replace(".000", " ")

    if hora >= 00 and hora < 12 :
        var = "AM"
    else:
        var = "PM"
        if hora == 13:
            hora = "01"
        if hora == 14:
            hora = "02"
        if hora == 15:
            hora = "03"
        if hora == 16:
            hora = "04"
        if hora == 17:
            hora = "05"
        if hora == 18:
            hora = "06"
        if hora == 19:
            hora = "07"
        if hora == 20:
            hora = "08"
        if hora == 21:
            hora = "09"
        if hora == 22:
            hora = "10"
        if hora == 23:
            hora = "11"     
    
    time = str(hora) + ":" + minutos + ":" + segundos + var
    return time
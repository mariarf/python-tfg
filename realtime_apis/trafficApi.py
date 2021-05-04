# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

#datetime format: yyyy-mm-ddThh:mm:ss
#devuelve false si el dataframe esta vacio y true si se escribe algo
def trafficDataIngestion(datalimit, start_datetime, file_dir):

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    date = f"data_as_of>'{start_datetime}'"  #se define la fecha de inicio de la consulta
    date = date.replace(" ", "T")
    print(date)
    
    columns = "data_as_of, id, speed, travel_time, link_name"  #columnas que se pediran a la api

    results = client.get("i4gi-tjb9", limit=datalimit, borough = "Manhattan", where = date, select = columns) 
    
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    
    if results_df.empty:
        return False
    #-----------------------------------------datetime - time_hour --------------------------------------#
    results_df["datetime"] = results_df["data_as_of"].str[:-9] + "00:00"
    results_df["datetime_traffic"] = results_df["data_as_of"].str[:-4]
    
    results_df["datetime"] = pd.to_datetime(results_df["datetime"])
    results_df["weekday"] = results_df['datetime'].dt.day_name()
    results_df["datetime"] = results_df["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    # se añaden nuevas columnas
    results_df = results_df[["datetime", "datetime_traffic", "weekday", "id", "speed", "travel_time", "link_name"]]

    #se guarda en la direccion del archivo pasado como parametro
    results_df.to_csv(file_dir, index=False)
    print(f"TrafficApi: {file_dir}")
    return True


#print(trafficDataIngestion(100000000, "2021-05-03T18:39:02", "borrame.csv"))
#trafficDataIngestion(1000000, "2021-03-01T00:00:00", "2021-03-31T23:59:59")



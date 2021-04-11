import socket, urllib3, json, certifi
import pandas as pd
# crea un socket INET de tipo STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ahora se conecta al servidor web en el puerto 80 (http)
#s.connect(("www.mcmillan-inc.com", 80))
#print(s)

start_datetime= "2021-04-11T00:00:00"
end_datetime= "2021-04-11T11:05:00"

url="https://www.airnowapi.org/aq/observation/latLong/current/?format=application/json&latitude=40.7485&longitude=-73.9839&distance=25&API_KEY=7FD50518-C721-4C9A-861F-883367594091"
# handle certificate verification and SSL warnings
# https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
#url="https://api.weather.gov/points/40.7485,-73.9839/forecast"
# get data from the API
url = f"https://www.airnowapi.org/aq/data/?startDate={start_datetime}&endDate={end_datetime}&parameters=OZONE,PM25&BBOX=-74.020308,40.700155,-73.940657,40.827572&dataType=B&format=application/json&verbose=0&nowcastonly=0&includerawconcentrations=0&API_KEY=7FD50518-C721-4C9A-861F-883367594091"
url = "https://www.airnowapi.org/aq/data/?startDate=2021-04-11T14&endDate=2021-04-11T17&parameters=OZONE,PM25,PM10,CO,NO2,SO2&BBOX=-74.020308,40.700155,-73.940657,40.827572&dataType=A&format=application/json&verbose=0&nowcastonly=0&includerawconcentrations=0&API_KEY=7FD50518-C721-4C9A-861F-883367594091"
response = http.request('GET', url)


# decode json data into a dict object
data = json.loads(response.data.decode('utf-8'))
#print(data)
results_df = pd.json_normalize(data)
print(results_df.head(20))
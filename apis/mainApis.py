#from .trafficApi import dataIngestion
from trafficApi import dataIngestion
#from .airQualityApi import *

# limite de datos, ultimafecha
lastRegister = dataIngestion(1000, "2021-03-12T00:00:00.000")
print(lastRegister)
print("pepe")
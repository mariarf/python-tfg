#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from pandas._testing import assert_frame_equal
from realtimeApis import *


class test_realtimeApis(unittest.TestCase):
        list_airQuality = ["datetime","AQI_PM2.5","Parameter_PM2.5","Unit_PM2.5","Value_PM2.5","Category_PM2.5","AQI_OZONE","Parameter_OZONE","Unit_OZONE","Value_OZONE","Category_OZONE"]
        list_weather = ["datetime","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Heat Index","Wind Speed","Wind Gust","Wind Direction","Wind Chill","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]

        def test(self):
                print("pepeeeeeeeeeeeeee")
                list = ["1T_W_F/1T", "1T_W_F/2T", "2T_W_F/1T", "2T_W_F/2T", "3T_W_F"]

                for i in list:
                        test = i
                        dir = "unittest/test_realtime_apis"
                        new = f"{dir}/{test}/new.csv"
                        merge = f"{dir}/{test}/merge.csv"
                        res = write(new, merge, list_airQuality)
                        merge_res = pd.read_csv(merge)
                        expected = pd.read_csv(f"{dir}/{test}/expected.csv")

                        #self.assertEqual(res, True)
                        assert_frame_equal(merge_res, expected)
                        
                        #se restablece el valor del original
                        merge_original = pd.read_csv(f"{dir}/{test}/merge_original.csv")
                        merge_res.to_csv(f"{dir}/{test}/merge_res.csv", index = False)
                        merge_original.to_csv(merge, index = False)

#        """ 1T_W: SE REGISTRAN VALORES DE TRÁFICO
#            
#        """  
#        def register_traffic_datetime(self):
#                standard_model_test(self, [], "1T_W", True)
#                print("1T_W: SE REGISTRAN VALORES DE TRÁFICO")
#
#        """2T_W: NO HAY VALORES DE TRÁFICO EN MERGE
#                * se espera para guardar cualquier otro valor distinto a los de tráfico
#        """
#        def register_traffic_datetime(self):
#                standard_model_test(self, [], "1T_W", False)
#                print("2T_W: NO HAY VALORES DE TRÁFICO EN MERGE")

#        """ 1T_W_F: AUN FALTAN VALORES DE TRÁFICO 
#                -- Hasta que no se registre la hora entera de tráfico no se guardan los datos
#                * return false, se espera a que esten todos los valores para la hora a registrar
#                > Hora tráfico menor
#                > Hora tráfico igual               
#                
#        """
#        def register_traffic_datetime(self):
#                standard_model_test(self, list_airQuality, "1T_W_F/1T", False)
#                standard_model_test(self, list_airQuality, "1T_W_F/2T", False)
#                print("1T_W_F: AUN FALTAN VALORES DE TRÁFICO")
#
#        """ 2T_W: SALTO EN VALORES DE TRÁFICO
#                -- Hay valores de tráfico mayores a la hora consulta pero NO se encontraron coincidencias
#                        *return true, se registran los nuevos valores
#                > Primera hora para tráfico NaN
#                > Hora del medio para tráfico NaN
#        """
#        def register_traffic_datetime(self):
#                standard_model_test(self, list_airQuality, "2T_W_F/1T", True)
#                standard_model_test(self, list_airQuality, "2T_W_F/2T", True)
#                print("2T_W: SALTO EN VALORES DE TRÁFICO")
#
#        """ 3T_W: REGISTRO CORRECTO
#                -- Se pasa una lista de valores y se registran cuando @datetime coincida
#        """
#        def register_traffic_datetime(self):
#                standard_model_test(self, list_airQuality, "3T_W_F", True)
#                print("3T_W: REGISTRO CORRECTO")
      

if __name__ == "__main__":
    unittest.main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from pandas._testing import assert_frame_equal
from realtimeApis import *
class test_realtimeApis(unittest.TestCase):

    list_airQuality = ["datetime","AQI_PM2.5","Parameter_PM2.5","Unit_PM2.5","Value_PM2.5","Category_PM2.5","AQI_OZONE","Parameter_OZONE","Unit_OZONE","Value_OZONE","Category_OZONE"]
    list_weather = ["datetime","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Heat Index","Wind Speed","Wind Gust","Wind Direction","Wind Chill","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]
   

#    """ 1T: 
#            --> Si es la PRIMERA VEZ que se ejecuta el código y no se encuentran valores para tráfico
#                *se registra el valor correspondiente
#    """
#    def test_first_hour(self):
#        dir = "unittest/test_realtime_apis"
#        new = f"{dir}/1T/new.csv"
#        merge = f"{dir}/1T/merge.csv"
#
#        res = write(new, merge, list_airQuality)
#
#        merge_res = pd.read_csv(merge)
#        expected = pd.read_csv(f"{dir}/1T/expected.csv")
#
#        self.assertEqual(res, True)
#        assert_frame_equal(merge_res, expected)
#        
#        #se restablece el valor del original
#        merge_original = pd.read_csv(f"{dir}/1T/merge_original.csv")
#        merge_res.to_csv(f"{dir}/1T/merge_res.csv", index = False)
#        merge_original.to_csv(merge, index = False)
#    
#
#    """ 2T: probar con 3T QUE LO MATA
#            2T-1: Tráfico no esta completo por lo que no se guardan
#            2T-2: Tráfico hora justo hh:59:59 se escribe
#    """
#    def test_datetime_equals(self):
#        """ 2T-1
#        """
#        dir = "unittest/test_realtime_apis"
#        new = f"{dir}/2T/2T-1/new.csv"
#        merge = f"{dir}/2T/2T-1/merge.csv"
#
#        res = write(new, merge, list_airQuality)
#
#        merge_res = pd.read_csv(merge)
#        expected = pd.read_csv(f"{dir}/2T/2T-1/expected.csv")
#
#        self.assertEqual(res, False)
#        assert_frame_equal(merge_res, expected)
#
#        #se restablece el valor del original
#        merge_original = pd.read_csv(f"{dir}/2T/2T-1/merge_original.csv")
#        merge_original.to_csv(merge, index = False)
#
#        """ 2T-2 
#        """
#        dir = "unittest/test_realtime_apis"
#        new = f"{dir}/2T/2T-2/new.csv"
#        merge = f"{dir}/2T/2T-2/merge.csv"
#
#        res = write(new, merge, list_airQuality)
#
#        merge_res = pd.read_csv(merge)
#        expected = pd.read_csv(f"{dir}/2T/2T-2/expected.csv")
#
#        self.assertEqual(res, True)
#        assert_frame_equal(merge_res, expected)
#
#        #se restablece el valor del original
#        merge_original = pd.read_csv(f"{dir}/2T/2T-2/merge_original.csv")
#        merge_original.to_csv(merge, index = False)
#
#
#    """ 3T:
#            --> Se consulta y no consigue valores fecha mayor
#    """
#    def test_datetime_highest(self):
#    
#        dir = "unittest/test_realtime_apis"
#        new = f"{dir}/3T/new.csv"
#        merge = f"{dir}/3T/merge.csv"
# 
#        res = write(new, merge, list_airQuality)
# 
#        merge_res = pd.read_csv(merge)
#        expected = pd.read_csv(f"{dir}/3T/expected.csv")
# 
#        self.assertEqual(res, False) 
#        assert_frame_equal(merge_res, expected)
# 
#        #se restablece el valor del original
#        merge_original = pd.read_csv(f"{dir}/3T/merge_original.csv")
#        merge_original.to_csv(merge, index = False)
#
#
    """ 4T:
            4T-1: Se registran los valores sin problema
            4T-2: Los valores ya estaban registrados no se vuelven a guardar
                --> Para comprobarlo se cambiará el contenido del valor nuevo
                    y en el archivo de merge debe mantenerse los valores originales

    """
    def test_register_value(self):
        """4T-1
        """
        dir = "unittest/test_realtime_apis"
        new = f"{dir}/4T/4T-1/new.csv"
        merge = f"{dir}/4T/4T-1/merge.csv"

        res = write(new, merge, list_airQuality)

        merge_res = pd.read_csv(merge)
        expected = pd.read_csv(f"{dir}/4T/4T-1/expected.csv")

        self.assertEqual(res, True)
        assert_frame_equal(merge_res, expected)

        #se restablece el valor del original
        merge_original = pd.read_csv(f"{dir}/4T/4T-1/merge_original.csv")
        merge_original.to_csv(merge, index = False)


    """ 5t:
            --> Se detecta un salto en los datos de tráfico (no se registro valores para una hora dada)
            --> Se escribe la nueva fila en el lugar donde corresponda (ordenado por fecha)
    """
    #def test_jump():
    #    print("Hacemos un test")

if __name__ == "__main__":
    unittest.main()
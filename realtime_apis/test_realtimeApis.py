#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from realtimeApis import *
class test_realtimeApis():

    """ 1T: 
            --> Si es la PRIMERA VEZ que se ejecuta el código y no se encuentran valores para tráfico
                *se registra el valor correspondiente
    """
    def test_first_hour():
        print("Hacemos un test")

    """ 2T: probar con 3T QUE LO MATA
            2T-1: Tráfico no esta completo por lo que no se guardan
                --> _2 se actualiza merge a fecha mayor, deberían guardarse los nuevos datos
            2T-2: Tráfico hora justo hh:59:59 se escribe
    """
    def test_datetime_equals():
        print("Hacemos un test")
    """ 3T:
            --> Se consulta y no consigue valores
            --> _2 se actualiza merge con nuevos valores 
    """
    def test_datetime_highest():
        print("Hacemos un test")

    """ 4T:
            4T-1: Se registran los valores sin problema
            4T-1: Los valores ya estaban registrados no se vuelven a guardar
                --> Para comprobarlo se cambiará el contenido del valor nuevo
                    y en el archivo de merge debe mantenerse los valores originales

    """
    def test_register_value():
        print("Hacemos un test")

    """ 5t:
            --> Se detecta un salto en los datos de tráfico (no se registro valores para una hora dada)
            --> Se escribe la nueva fila en el lugar donde corresponda (ordenado por fecha)
    """
    def test_jump():
        print("Hacemos un test")

if __name__ == "__main__":
    unittest.main()
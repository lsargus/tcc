# Importacao de modulos
import numpy as np

"""
Classe que deve fazer a conversão dos valores bases para o PU para um sistema trifásico. 
"""


class ParametrosPU:
    def __init__(self, tensao: int, potencia=100000000):
        self.s_base = potencia
        self.v_base = tensao

        self.i_base = self.s_base / (self.v_base * np.sqrt(3))
        self.z_base = self.v_base**2 / self.s_base
        self.y_base = 1 / self.z_base

    def tensao_to_pu(self, tensao_volt):
        """
        realiza a conversão do valor da tensão de Volts para PU

            Parametros:
            -------------
            tensao_base:
                valor da tensão à ser convertida
            -------------
            returns : float
                valor da tensão em PU
        """
        # mesmo se for uma divisão de inteiros o python3 retorna um float
        return tensao_volt / self.v_base

    def tensao_to_volt(self, tensao_pu):
        """
        realiza a conversão do valor da tensão de PU para Volts

            Parametros:
            -------------
            tensao_base:
                valor da tensão à ser convertida
            -------------
            returns : float
                valor da tensão em Volts
        """
        # mesmo se for uma divisão de inteiros o python3 retorna um float
        return tensao_pu * self.v_base

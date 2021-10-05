"""
    Arquivo basico para implementação dos elementos do circuito

    Classe abstrata pois não deve ser implementada, srá usada como base para criação dos demais elementos.
"""

from abc import ABC
from src.tcc.util import constantes_numericas as const


class Elemento(ABC):
    __nome = ""
    __z_120 = const.H6x6
    __sofreu_falta = False
    __analisa_falta = False

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def z_120(self):
        return self.__z_120

    @z_120.setter
    def z_120(self, z_120):
        self.__z_120 = z_120

    @property
    def sofreu_falta(self):
        return self.__sofreu_falta

    @sofreu_falta.setter
    def sofreu_falta(self, falta):
        self.__sofreu_falta = falta

        # caso tenha sofrido falta marca o elemento para analise
        if falta:
            self.__analisa_falta = True

    @property
    def analisa_falta(self):
        return self.__analisa_falta

    @analisa_falta.setter
    def analisa_falta(self, analisa_falta):
        self.__analisa_falta = analisa_falta

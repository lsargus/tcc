from abc import ABC, abstractmethod
from src.tcc.calculos import faltas as flt


class Elemento(ABC):
    __z_120 = flt.H6x6
    __sofreu_falta = False

    def __init__(self):
        pass

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

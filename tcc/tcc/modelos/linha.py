# equivalente.py
from src.tcc.calculos import faltas as flt
from src.tcc.modelos.elemento import Elemento

"""
Classe que deve representar as linhas de transmissão
"""


class Linha(Elemento):
    def __init__(self, comprimento: float, z_1: complex, z_0: complex, y_1: complex, y_0: complex, nome: str):
        self.compr = comprimento
        self.z_1 = z_1
        self.z_0 = z_0
        self.y_1 = y_1
        self.y_0 = y_0
        self.parametros_linha_totais()
        self.z_abc = flt.z_120abc(self.z_120, '120')
        self.nome = nome

    def parametros_linha_totais(self):
        if self.compr > 100:
            self.z_120 = flt.zLine_120_6x6(self.z_1, self.y_1, self.z_0, self.y_0, self.compr)
        else:
            self.z_120 = flt.z_120_6x6(self.compr * self.z_1, self.compr * self.z_0)

    def parametros_linha_frac(self, fracao):
        if self.compr > 100:
            # Impedancia da linha do lado esquerdo
            zlp1 = flt.zLine_120_6x6(self.z_1, self.y_1, self.z_0, self.y_0, self.compr * fracao)
            # Impedancia da linha do lado direito
            zlp2 = flt.zLine_120_6x6(self.z_1, self.y_1, self.z_0, self.y_0, self.compr * (1 - fracao))
        else:
            # Impedancia da linha do lado esquerdo
            zlp1 = flt.z_120_6x6(self.compr * fracao * self.z_1, self.compr * fracao * self.z_0)
            # Impedancia da linha do lado direito
            zlp2 = flt.z_120_6x6(self.compr * (1 - fracao) * self.z_1, self.compr * (1 - fracao) * self.z_0)

        return zlp1, zlp2

    def get_falta(self):
        return self.sofreu_falta

# equivalente.py

from src.tcc.calculos import faltas as flt

"""
Classe que deve representar os equivalentes de thevenin
"""


class Equivalente:

    def __init__(self, v_mag, z_1, z_0):
        self.v_mag = v_mag
        self.v_ang = 0.0
        self.i_mag = 0.0
        self.i_ang = 0.0
        self.z_1 = z_1
        self.z_0 = z_0

    def monta_matrizes(self):
        self.v_abc = flt.valor_abc(self.v_mag / 3 ** (1 / 2), self.v_ang)
        self.i_abc = flt.valor_abc(self.i_mag, self.i_ang)
        self.z_120 = flt.z_120_6x6(self.z_1, self.z_0)
        self.z_abc = flt.z_120abc(self.z_120, '120')

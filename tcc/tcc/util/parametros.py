# equivalente.py

"""
Classe que deve representar as linhas de transmissão
"""

from src.tcc.enums.tpFalta import TpFalta
from src.tcc.enums.tpRele import TpRele


class Parametros:

    def __init__(self, tf: TpFalta, rele: TpRele, rf=0.01, delta_m=0.01):
        self.tf = tf
        self.rele = rele

        # validação para que delta_m não seja zero
        if delta_m == 0:
            self.delta = 0.01
        else:
            self.delta = delta_m

        # validação para que a resistencia não seja zero
        if rf == 0:
            self.rf = 0.01
        else:
            self.rf = rf

    @property
    def tipo_falta(self):
        return self.tf

    @property
    def tipo_rele(self):
        return self.rele

    @property
    def intervalo_tempo(self):
        return self.delta

    @property
    def resistencia_falta(self):
        return self.rf

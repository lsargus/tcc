# falta.py

import numpy as np
from ..enums.tpFalta import TpFalta

# Matrizes base - 3x3
from ..util.matriz import Matriz

Zeros3 = Matriz(np.zeros((3, 3)))
I3x3 = Matriz(np.eye(3))

"""
Classe que deve representar os elementos de faltas
"""


class Falta:

    def __init__(self, tipo: TpFalta, rf: float):
        """tipo de falta (1-mono, 2-bi, 3-biterra, 4-tri, 5-triterra, default: mono)"""
        # todo: arrumar bifasica para usar B C
        if tipo == TpFalta.BI:
            # matriz de falta bifasica
            z_falta = Matriz([[1.0 / rf, -1.0 / rf, 0.00000],
                              [-1.0 / rf, 1.0 / rf, 0.00000],
                              [0.00000, 0.00000, 0.00000]])

        elif tipo == TpFalta.BI_TERRA:
            # matriz de falta bifasica  terra
            z_falta = Matriz([[2.0 / rf, -1.0 / rf, 0.00000],
                              [-1.0 / rf, 2.0 / rf, 0.00000],
                              [0.00000, 0.00000, 0.00000]])
        elif tipo == TpFalta.TRI:
            # matriz de falta trifasica
            z_falta = Matriz([[1.0 / rf, 0.00000, 0.00000],
                              [0.00000, 1.0 / rf, 0.00000],
                              [0.00000, 0.00000, 1.0 / rf]])
        elif tipo == TpFalta.TRI_TERRA:
            # matriz de falta trifasica a terra
            z_falta = Matriz([[3 / rf, -1 / rf, -1 / rf],
                              [-1 / rf, 3 / rf, -1 / rf],
                              [-1 / rf, -1 / rf, 3 / rf]])
        else:
            # matriz de falta monofasica
            z_falta = Matriz([[1.0 / rf, 0.00000, 0.00000],
                              [0.00000, 0.00000, 0.00000],
                              [0.00000, 0.00000, 0.00000]])

        self.z = Matriz.concatena_vertical(Matriz.concatena_horizontal(I3x3, Zeros3),
                                           Matriz.concatena_horizontal(z_falta, I3x3))

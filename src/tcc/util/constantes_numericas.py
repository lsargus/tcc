# constantes_numericas.py

import numpy as np
from src.tcc.util.matriz import Matriz

'''
Matrizes para transformacao de sequencia de fase para componentes de sequencia
e vice-versa pelo teorema de Fortescue
'''

# Definicao da constante a
alpha = complex(np.cos(120 * np.pi / 180), np.sin(120 * np.pi / 180))

# Matriz H - converte de componentes de fase para componentes simetricas
# Caso trifasico - H3x3
H3x3 = Matriz([[1, alpha, alpha ** 2],
               [1, alpha ** 2, alpha],
               [1, 1, 1]])
H3x3 = H3x3 / 3

# Matriz T - converte de componentes de sequencia para componentes de fase
T3x3 = H3x3.inv()

# Matrizes base - 3x3
Zeros3 = Matriz(np.zeros((3, 3)))
I3x3 = Matriz(np.eye(3))

# Matrizes para quadripolos trifasicos - 6x6
H6x6 = Matriz.concatena_vertical(Matriz.concatena_horizontal(H3x3, Zeros3), Matriz.concatena_horizontal(Zeros3, H3x3))
T6x6 = H6x6.inv()

# Matriz para corrigir os angulos da corrente do rele R - 6x6
I_ang_correcao = Matriz.concatena_vertical(Matriz.concatena_horizontal(I3x3, Zeros3),
                                           Matriz.concatena_horizontal(Zeros3, -1 * I3x3))

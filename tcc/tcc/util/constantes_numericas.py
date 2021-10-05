# constantes_numericas.py

import numpy as np

'''
Matrizes para transformação de sequencia de fase para componentes de sequencia
e vice-versa pelo teorema de Fortescue
'''

# Definicao da constante a
alpha = complex(np.cos(120 * np.pi / 180), np.sin(120 * np.pi / 180))

# Matriz H - converte de componentes de fase para componentes simétricas
# Caso trifásico - H3x3
H3x3 = np.matrix([[1, alpha, alpha ** 2],
                  [1, alpha ** 2, alpha],
                  [1, 1, 1]])
H3x3 = H3x3 / 3

# Matriz T - converte de componentes de sequencia para componentes de fase
T3x3 = np.linalg.inv(H3x3)

# Matrizes base - 3x3
Zeros3 = np.matrix(np.zeros((3, 3)))
I3x3 = np.matrix(np.eye(3))

# Matrizes para quadripólos trifásicos - 6x6
H6x6 = np.vstack((np.hstack((H3x3, Zeros3)),
                 np.hstack((Zeros3, H3x3))))
T6x6 = np.linalg.inv(H6x6)

# Matriz para corrigir os ângulos da corrente do rele R - 6x6
I_ang_correcao = np.vstack((np.hstack((I3x3, Zeros3)),
                           np.hstack((Zeros3, -1 * I3x3))))

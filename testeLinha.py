from tcc.modelos.linha import Linha
from tcc.util.constantes_numericas import T3x3, H3x3
from decimal import Decimal
import numpy as np


def compara(l1, l2):
    for i in range(0, l1.shape[0]):
        for j in range(0, l1.shape[1]):
            print('-----------Posição ', i, ' ', j, '-------------')
            print('L1 ', l1[i, j], ' - - L2 ', l2[i, j])
            print('Diferença = ', l1[i, j] - l2[i, j])
            print('---------------------------')


z1 = 0.0976 + 0.520j
z0 = 0.794 + 1.61634j
#z120 = [[z1], [z1], [z0]]
#zabc = T3x3 @ z120
#zabc = zabc / 3
#z120 = H3x3 @ zabc

y1 = 3.178e-6j
y0 = 2.1752e-6j
#y120 = [[y1], [y1], [y0]]
#yabc = T3x3 @ y120
#yabc = yabc / 3
#y120 = H3x3 @ yabc

linha1 = Linha(110 * 3, z1, z0, y1, y0, "Linha 1")

linha2 = Linha(110, z1, z0, y1, y0, "Linha 2")
linha3 = Linha(110, z1, z0, y1, y0, "Linha 3")
linha4 = Linha(110, z1, z0, y1, y0, "Linha 4")

Vi = np.matrix([[13800], [13800], [13800], [50], [50], [50]])
vvv = [[13800, 13800], [13800, 13800], [13800, 13800], [50, 50], [50, 50], [50, 50]]

linhat = linha2.z_abc * linha3.z_abc * linha4.z_abc

compara(linha1.z_abc, linhat)
linha1.z_abc[1, 1] == linhat[1, 1]

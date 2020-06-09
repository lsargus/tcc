'''
Este arquivo contem:
    Calculos e aplicacao das faltas
Versao 1.2 - data 13 de maio de 2019

Alteracoes:
Foi separado o arquivo de aplicacao de faltas do de calculos das funcoes 67
'''

# Importacao de modulos
import numpy as np
from src.tcc.enums.tpFalta import TpFalta

'''
Matrizes para transformacao de sequencia de fase para componentes de sequencia
e vice-versa pelo teorema de Fortescue
'''
# Definicao da constante a
alpha = complex(np.cos(120 * np.pi / 180), np.sin(120 * np.pi / 180))

# Matriz H - converte de componententes de fase para componentes simetricas
# Caso trifasico - H3x3
H3x3 = np.matrix([[1, alpha, alpha ** 2],
                  [1, alpha ** 2, alpha],
                  [1, 1, 1]])
H3x3 = H3x3 / 3

# Matriz T - converte de componentes de sequencia para componentes de fase
T3x3 = H3x3.getI()

# Matrizes base - 3x3
Zeros3 = np.matrix(np.zeros((3, 3)))
I3x3 = np.matrix(np.eye(3))

# Matrizes para quadripolos trifasicos - 6x6
H6x6 = np.vstack((np.hstack((H3x3, Zeros3)),
                  np.hstack((Zeros3, H3x3))))
T6x6 = H6x6.getI()

# Matriz para corrigir os angulos da corrente do rele R - 6x6
I_ang_correcao = np.vstack((np.hstack((I3x3, Zeros3)),
                            np.hstack((Zeros3, -1 * I3x3))))

"""
Funcao definida para receber quadripolo em sequencia de fases e converte-la em
componentes de sequencia ou vice-versa
"""


def z_120abc(z, conv):
    """Converte matriz entre componentes de fase e de sequencia"""
    if conv == '120':
        zabc120 = T6x6 * z * H6x6
    elif conv == 'abc':
        zabc120 = H6x6 * z * T6x6
    else:
        zabc120 = z
    return zabc120


"""
Funcao definida para receber valores de magnitude e angulos e gerar uma
matriz complexa em sequencia de fases
"""


def valor_abc(mag, ang):
    valor_a = complex(mag * np.cos((ang + 0) * np.pi / 180), mag * np.sin((ang + 0) * np.pi / 180))
    valor_b = complex(mag * np.cos((ang - 120) * np.pi / 180), mag * np.sin((ang - 120) * np.pi / 180))
    valor_c = complex(mag * np.cos((ang + 120) * np.pi / 180), mag * np.sin((ang + 120) * np.pi / 180))
    valor_abc = np.matrix([[valor_a],
                           [valor_b],
                           [valor_c]])
    return valor_abc


"""
Funcao definida para receber valores de impedancia de sequencia, considerando
sequencia negativa igual a sequencia positiva.
Gera uma matriz de impedancia trifasica 6x6 - quadripolos
"""


def z_120_6x6(z_1, z_0):
    Z_120 = np.matrix([[z_1, 0.00000, 0.00000],
                       [0.00000, z_1, 0.00000],
                       [0.00000, 0.00000, z_0]])
    z_120_6x6 = np.vstack((np.hstack((I3x3, Z_120)),
                           np.hstack((Zeros3, I3x3))))
    return z_120_6x6


"""
Funcao definida para receber valores de impedancia e admitancia de sequencia
positiva e sequencia zero, considerando sequencia negativa igual a sequencia
positiva.
Gera uma matriz de impedancia de linha longa utilizada como quadripolos
trifasicos - 6x6
"""


def zLine_120_6x6(z_1, y_1, z_0, y_0, leng):
    zc_1 = np.sqrt(z_1 / y_1)
    gama_1 = np.sqrt(z_1 * y_1)
    zc_0 = np.sqrt(z_0 / y_0)
    gama_0 = np.sqrt(z_0 * y_0)

    A_1 = np.cosh(gama_1 * leng)
    B_1 = zc_1 * np.sinh(gama_1 * leng)
    C_1 = np.sinh(gama_1 * leng) / zc_1
    D_1 = np.cosh(gama_1 * leng)
    A_0 = np.cosh(gama_0 * leng)
    B_0 = zc_0 * np.sinh(gama_0 * leng)
    C_0 = np.sinh(gama_0 * leng) / zc_0
    D_0 = np.cosh(gama_0 * leng)

    A_120 = np.matrix([[A_1, 0, 0], [0, A_1, 0], [0, 0, A_0]])
    B_120 = np.matrix([[B_1, 0, 0], [0, B_1, 0], [0, 0, B_0]])
    C_120 = np.matrix([[C_1, 0, 0], [0, C_1, 0], [0, 0, C_0]])
    D_120 = np.matrix([[D_1, 0, 0], [0, D_1, 0], [0, 0, D_0]])

    zl_120_6x6 = np.vstack((np.hstack((A_120, B_120)),
                            np.hstack((C_120, D_120))))
    return zl_120_6x6


"""
Funcao definida para receber o tipo de falta e a resistencia
"""


def falta(tipo, rf):
    """tipo de falta (1-mono, 2-bi, 3-biterra, 4-tri, 5-triterra, default: mono)"""
    if tipo == TpFalta.BI:
        # matriz de falta bifasica
        zF = np.matrix([[1.0 / rf, -1.0 / rf, 0.00000],
                        [-1.0 / rf, 1.0 / rf, 0.00000],
                        [0.00000, 0.00000, 0.00000]])
    elif tipo == TpFalta.BI_TERRA:
        # matriz de falta bifasica  terra
        zF = np.matrix([[2.0 / rf, -1.0 / rf, 0.00000],
                        [-1.0 / rf, 2.0 / rf, 0.00000],
                        [0.00000, 0.00000, 0.00000]])
    elif tipo == TpFalta.TRI:
        # matriz de falta trifasica
        zF = np.matrix([[1.0 / rf, 0.00000, 0.00000],
                        [0.00000, 1.0 / rf, 0.00000],
                        [0.00000, 0.00000, 1.0 / rf]])
    elif tipo == TpFalta.TRI_TERRA:
        # matriz de falta trifasica a terra
        zF = np.matrix([[3 / rf, -1 / rf, -1 / rf],
                        [-1 / rf, 3 / rf, -1 / rf],
                        [-1 / rf, -1 / rf, 3 / rf]])
    else:
        # matriz de falta monofasica
        zF = np.matrix([[1.0 / rf, 0.00000, 0.00000],
                        [0.00000, 0.00000, 0.00000],
                        [0.00000, 0.00000, 0.00000]])

    zF = np.vstack((np.hstack((I3x3, Zeros3)),
                    np.hstack((zF, I3x3))))
    return zF


def Ir(Z, vs, Vr):
    """Calculo da corrente do lado receptor"""
    A = Z[:3, :3]
    B = Z[:3, 3:]
    b_inv = B.getI()
    Ir = b_inv * (vs - A * Vr)
    return Ir


def aplica_falta(vs_abc, zs_abc, zlp1, zlp2, m, zf, zr_abc, vr_abc):
    """Aplica falta ao longo da linha"""

    # Converte Z da linha de abc para 120
    Zlp1_abc = z_120abc(zlp1, '120')
    Zlp2_abc = z_120abc(zlp2, '120')

    # Calcula a Z da linha com a falta
    if (m == 0):
        Zl_abc = zf * Zlp2_abc
    elif (m == 1):
        Zl_abc = Zlp1_abc * zf
    else:
        Zl_abc = Zlp1_abc * zf * Zlp2_abc

    # Calcula a Z total entre as duas fontes
    Ztotal_abc = zs_abc * Zl_abc * zr_abc

    # Calcula a corrente de falta da fonte R
    Ir_abc = Ir(Ztotal_abc, vs_abc, vr_abc)
    # Monta o vetor VI com componentes abc da fonte R
    VIr_abc = np.vstack((vr_abc,
                         Ir_abc))
    # Calcula VI com componentes abc para o rele R - I com tombo de 180 graus
    VIreler_abc = I_ang_correcao * (zr_abc * VIr_abc)
    # Calcula VI com componentes abc para o rele S
    VIreles_abc = (Zl_abc * zr_abc) * VIr_abc
    # Calcula VI com componentes 120 para os reles R e S
    VIreler_120 = H6x6 * VIreler_abc
    VIreles_120 = H6x6 * VIreles_abc

    return VIreles_abc, VIreler_abc, VIreles_120, VIreler_120


def aplica_falta_atras(Vs_abc, Zs_abc, Zl_120, Zf, Zr_abc, Vr_abc):
    """Aplica a falta reversa ao rele"""

    # Converte Z da linha de abc para 120
    Zl_abc = z_120abc(Zl_120, '120')
    # Calcula a Z total entre as duas fontes
    Ztotal_abc = Zs_abc * Zf * Zl_abc * Zr_abc

    # Calcula a corrente de falta da fonte R
    Ir_abc = Ir(Ztotal_abc, Vs_abc, Vr_abc)
    # Monta o vetor VI com componentes abc da fonte R
    VIr_abc = np.vstack((Vr_abc,
                         Ir_abc))
    # Calcula VI com componentes abc para o rele R - I com tombo de 180 graus
    VIreler_abc = I_ang_correcao * (Zr_abc * VIr_abc)
    # Calcula VI com componentes abc para o rele S
    VIreles_abc = (Zl_abc * Zr_abc) * VIr_abc
    # Calcula VI com componentes 120 para os reles R e S
    VIreler_120 = H6x6 * VIreler_abc
    VIreles_120 = H6x6 * VIreles_abc

    return VIreles_abc, VIreler_abc, VIreles_120, VIreler_120

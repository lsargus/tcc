"""
Este arquivo contem:
    Calculos e aplicacao das faltas
Versao 1.2 - data 13 de maio de 2019

Alteracoes:
Foi separado o arquivo de aplicacao de faltas do de calculos das funcoes 67
"""

# Importacao de modulos
import numpy as np
import math
from src.tcc.calculos import faltas as flt
from src.tcc.enums.tpFalta import TpFalta
from src.tcc.modelos.elemento import Elemento
from src.tcc.modelos.equivalente import Equivalente
from src.tcc.modelos.falta import Falta
from src.tcc.modelos.transformador import Transformador
from src.tcc.util.parametros import Parametros
from src.tcc.util import constantes_numericas as const

"""
Funcao definida para receber quadripolo em sequencia de fases e converte-la em
componentes de sequencia ou vice-versa
"""

DEC = 10


def z_120abc(z, conv):
    """
    Converte matriz entre componentes de fase e de sequencia
    :param z: matriz a ser convertida
    :param conv: <br>'120' caso seja passado uma matriz de sequencia a ser convertida para fase
                 <br>'abc' caso seja passado uma matriz de fase a ser convertida para sequencia
    :return:
    """
    if conv == '120':
        z_abc_120 = const.T6x6 * z * const.H6x6
    elif conv == 'abc':
        z_abc_120 = const.H6x6 * z * const.T6x6
    else:
        z_abc_120 = z
    return z_abc_120


"""
Funcao definida para receber valores de magnitude e angulos e gerar uma
matriz complexa em sequencia de fases
"""


def valor_abc(mag, ang):
    valor_a = complex(mag * np.cos((ang + 0) * np.pi / 180), mag * np.sin((ang + 0) * np.pi / 180))
    valor_b = complex(mag * np.cos((ang - 120) * np.pi / 180), mag * np.sin((ang - 120) * np.pi / 180))
    valor_c = complex(mag * np.cos((ang + 120) * np.pi / 180), mag * np.sin((ang + 120) * np.pi / 180))
    return np.matrix([[valor_a],
                      [valor_b],
                      [valor_c]])


"""
Funcao definida para receber valores de impedancia de sequencia, considerando
sequencia negativa igual a sequencia positiva.
Gera uma matriz de impedancia trifasica 6x6 - quadripolos
"""


def z_120_6x6(z_1, z_0):
    z_120 = np.matrix([[z_1, 0.00000, 0.00000],
                       [0.00000, z_1, 0.00000],
                       [0.00000, 0.00000, z_0]])
    return np.vstack((np.hstack((const.I3x3, z_120)),
                     np.hstack((const.Zeros3, const.I3x3))))


def zLine_120_6x6(z_1, y_1, z_0, y_0, leng):
    """
    Funcao definida para receber valores de impedancia e admitancia de sequencia
    positiva e sequencia zero, considerando sequencia negativa igual a sequencia
    positiva.
    Gera uma matriz de impedancia de linha longa utilizada como quadripolos
    trifasicos - 6x6
    """

    zc_1 = np.sqrt(z_1 / y_1)
    gama_1 = np.sqrt(z_1 * y_1)
    zc_0 = np.sqrt(z_0 / y_0)
    gama_0 = np.sqrt(z_0 * y_0)

    a_1 = np.cosh(gama_1 * leng)
    b_1 = zc_1 * np.sinh(gama_1 * leng)
    c_1 = np.sinh(gama_1 * leng) / zc_1
    d_1 = np.cosh(gama_1 * leng)
    a_0 = np.cosh(gama_0 * leng)
    b_0 = zc_0 * np.sinh(gama_0 * leng)
    c_0 = np.sinh(gama_0 * leng) / zc_0
    d_0 = np.cosh(gama_0 * leng)

    a_120 = np.matrix([[a_1, 0, 0], [0, a_1, 0], [0, 0, a_0]])
    b_120 = np.matrix([[b_1, 0, 0], [0, b_1, 0], [0, 0, b_0]])
    c_120 = np.matrix([[c_1, 0, 0], [0, c_1, 0], [0, 0, c_0]])
    d_120 = np.matrix([[d_1, 0, 0], [0, d_1, 0], [0, 0, d_0]])

    zl_120_6x6 = np.vstack((np.hstack((a_120, b_120)),
                           np.hstack((c_120, d_120))))
    return zl_120_6x6


"""
Funcao definida para receber o tipo de falta e a resistencia
"""


def falta(tipo, rf):
    """tipo de falta (1-mono, 2-bi, 3-biterra, 4-tri, 5-triterra, default: mono)"""
    if tipo == TpFalta.BI:
        # matriz de falta bifasica
        z_falta = np.matrix([[1.0 / rf, -1.0 / rf, 0.00000],
                             [-1.0 / rf, 1.0 / rf, 0.00000],
                             [0.00000, 0.00000, 0.00000]])
    elif tipo == TpFalta.BI_TERRA:
        # matriz de falta bifasica  terra
        z_falta = np.matrix([[2.0 / rf, -1.0 / rf, 0.00000],
                             [-1.0 / rf, 2.0 / rf, 0.00000],
                             [0.00000, 0.00000, 0.00000]])
    elif tipo == TpFalta.TRI:
        # matriz de falta trifasica
        z_falta = np.matrix([[1.0 / rf, 0.00000, 0.00000],
                             [0.00000, 1.0 / rf, 0.00000],
                             [0.00000, 0.00000, 1.0 / rf]])
    elif tipo == TpFalta.TRI_TERRA:
        # matriz de falta trifasica a terra
        z_falta = np.matrix([[3 / rf, -1 / rf, -1 / rf],
                             [-1 / rf, 3 / rf, -1 / rf],
                             [-1 / rf, -1 / rf, 3 / rf]])
    else:
        # matriz de falta monofasica
        z_falta = np.matrix([[1.0 / rf, 0.00000, 0.00000],
                             [0.00000, 0.00000, 0.00000],
                             [0.00000, 0.00000, 0.00000]])

    z_falta = np.vstack((np.hstack((const.I3x3, const.Zeros3)),
                        np.hstack((z_falta, const.I3x3))))
    return z_falta


def Ir(z, vs, vr):
    """
    Calculo da corrente do lado receptor

        Parametros:
        -------------
        z: matriz
            Matriz das impedancias totais do sistema
        vs: matriz
            Matris com valores de tensão abc do equivalente S
        vr: matriz
            Matris com valores de tensão abc do equivalente R
        -------------
        returns
            Corrente de falta na fonte R
    """
    a = z[:3, :3]
    b = z[:3, 3:]
    b_inv = b.inv()
    return b_inv * (vs - a * vr)


def aplica_falta(vs_abc, zs_abc, zlp1, zlp2, m, zf, zr_abc, vr_abc, falta: bool, pre_falta: bool):
    """Aplica falta ao longo da linha"""

    # Converte Z da linha de abc para 120
    z_lp1_abc = zlp1
    z_lp2_abc = zlp2

    # Calcula a Z da linha com a falta
    # if m == 0:
    #    z_l_abc = zf * z_lp2_abc
    # elif m == 1:
    #    z_l_abc = z_lp1_abc * zf
    # else:
    #    z_l_abc = z_lp1_abc * zf * z_lp2_abc

    z_l_abc = np.around(z_lp1_abc * zf * z_lp2_abc, decimals=DEC)
    # Calcula a Z total entre as duas fontes
    z_total_abc = np.around(zs_abc * z_l_abc * zr_abc, decimals=DEC)

    return calculo_falta(vs_abc, zr_abc, vr_abc, z_l_abc, z_total_abc, falta, pre_falta)


'''
def aplica_falta_atras(vs_abc, zs_abc, zl_120, zf, zr_abc, vr_abc):
    """Aplica a falta reversa ao rele"""

    # Converte Z da linha de abc para 120
    z_l_abc = z_120abc(zl_120, '120')
    # Calcula a Z total entre as duas fontes
    z_total_abc = zs_abc * zf * z_l_abc * zr_abc

    return calculo_falta(vs_abc, zr_abc, vr_abc, z_l_abc, z_total_abc)
'''


def aplica_falta_transformador(equiv_s: Equivalente, trans: Transformador, fal: Falta, equiv_r: Equivalente):
    """
    Aplica faltas no transformador, uma atrás e uma na frente do transformador

    :param equiv_s: equivalente S
    :param trans: transformador
    :param fal: elemento de falta
    :param equiv_r: equivalente R

    :return: valores de corrente e tensão antes e após o transformador (Não realizar faltas no interior
    do transformador)
    """
    vi_r_abc = []
    vi_s_abc = []
    vi_r_120 = []
    vi_s_120 = []

    # Calcula a Z total entre as duas fontes
    z_total_abc_d = equiv_s.z_abc * fal.z * trans.z_abc * equiv_r.z_abc
    vi_s_abc_temp, vi_r_abc_temp = calculo_tensao_corrente(equiv_r, equiv_s, z_total_abc_d)

    vi_s_abc = vi_s_abc_temp
    vi_r_abc = vi_r_abc_temp
    vi_s_120 = const.H6x6 * vi_s_abc_temp
    vi_r_120 = const.H6x6 * vi_r_abc_temp

    # Calcula a Z total entre as duas fontes
    z_total_abc_r = equiv_s.z_abc * trans.z_abc * fal.z * equiv_r.z_abc
    vi_s_abc_temp, vi_r_abc_temp = calculo_tensao_corrente(equiv_r, equiv_s, z_total_abc_r)

    vi_s_abc = np.hstack((vi_s_abc, vi_s_abc_temp))
    vi_r_abc = np.hstack((vi_r_abc, vi_r_abc_temp))
    vi_s_120 = np.hstack((vi_s_120, const.H6x6 * vi_s_abc_temp))
    vi_r_120 = np.hstack((vi_r_120, const.H6x6 * vi_r_abc_temp))

    return vi_s_abc, vi_r_abc, vi_s_120, vi_r_120


def calculo_tensao_corrente(equiv_r, equiv_s, z_total_abc):
    """
    Realiza o calculos da corrente e tensão do circuito

    :param equiv_r: equivalente R
    :param equiv_s: equivalente S
    :param z_total_abc: Impedancia total do circuito
    :return: Matrizes 6x1 com as tesões e correntes nos dois relés com valores em fase e sequencia
    """
    # Calcula a corrente de falta da fonte R
    i_r_abc = Ir(z_total_abc, equiv_s.v_abc, equiv_r.v_abc)
    # Monta o vetor VI com componentes abc da fonte R
    vi_r_abc = np.vstack((equiv_r.v_abc, i_r_abc))
    vi_s_abc = z_total_abc * vi_r_abc
    vi_s_rele = equiv_s.z_abc.inv() * vi_s_abc
    vi_r_rele = equiv_r.z_abc.inv() * vi_r_abc

    if True:
        for ponto in vi_s_rele:
            print(abs(ponto), ',  ang ', math.degrees(np.angle(ponto)))
        print('-------------')
        for ponto in vi_r_rele:
            print(abs(ponto), ',  ang ', math.degrees(np.angle(ponto)))
        print('-------------')

        for ponto in i_r_abc:
            print(abs(ponto), ',  ang ', math.degrees(np.angle(ponto)))
        print('-------------')

    return vi_s_rele, vi_r_rele


def calculo_falta(vs_abc, zr_abc, vr_abc, z_l_abc, z_total_abc, falta: bool, pre_falta: bool):
    """Realiza o calculo da falta no rele """

    # Calcula a corrente de falta da fonte R
    i_r_abc = Ir(z_total_abc, vs_abc, vr_abc)
    # Monta o vetor VI com componentes abc da fonte R
    vi_r_abc = np.vstack((vr_abc, i_r_abc))
    # Calcula VI com componentes abc para o rele R - I com tombo de 180 graus
    vi_reler_abc = const.I_ang_correcao * (zr_abc * vi_r_abc)
    # Calcula VI com componentes abc para o rele S
    vi_reles_abc = (z_l_abc * zr_abc) * vi_r_abc

    # verifica a posição dos relés para inverter a corrente
    # se for antes do relé S inverte a corrente vista pelo relé S
    # if pre_falta and not falta:
    #    vi_reles_abc = const.I_ang_correcao * vi_reles_abc
    # caso seja após o relé R inverte a corrente vista pelo relé R
    # elif not falta:
    #    vi_reler_abc = const.I_ang_correcao * vi_reler_abc

    # Calcula VI com componentes 120 para os reles R e S
    vi_reler_120 = const.H6x6 * vi_reler_abc
    vi_reles_120 = const.H6x6 * vi_reles_abc

    return vi_reles_abc, vi_reler_abc, vi_reles_120, vi_reler_120


def percorre_linha_com_falta(linha_falta: Elemento, param_s: Parametros, equiv_s: Equivalente, equiv_r: Equivalente,
                             lado_dir, lado_esq, elemento_falta: Falta, pre_falta: bool,
                             dist_ini: float):
    vi_abc_rele_s = []
    vi_120_rele_s = []
    vi_abc_rele_r = []
    vi_120_rele_r = []
    dist_falta = []

    # Faltas na linha, verifica se é o primeiro elemento sobre análise, caso seja considera posição na barra, caso
    # contrario faz o calculo imediatamente depois pois a barra já foi testado no elemento anterior
    for i in range(0 if dist_ini == 0 else 1, int(100 / (100 * param_s.intervalo_tempo)) + 1, 1):
        m = i / 100
        zlp1, zlp2 = linha_falta.parametros_linha_frac(m)

        zlp1 = lado_esq * flt.z_120abc(zlp1, '120')

        zlp2 = flt.z_120abc(zlp2, '120') * lado_dir

        s_abc, r_abc, s_120, r_120 = flt.aplica_falta(equiv_s.v_abc, equiv_s.z_abc, zlp1, zlp2, m, elemento_falta.z,
                                                      equiv_r.z_abc, equiv_r.v_abc, linha_falta.sofreu_falta, pre_falta)

        vi_abc_rele_s.append(s_abc)
        vi_120_rele_s.append(s_120)
        vi_abc_rele_r.append(r_abc)
        vi_120_rele_r.append(r_120)
        dist_falta.append((m * linha_falta.compr) + dist_ini)

    return vi_abc_rele_s, vi_120_rele_s, vi_abc_rele_r, vi_120_rele_r, dist_falta

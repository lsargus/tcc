# coding=utf8
"""
Programa principal do aplicativo modificado por Fabiano Magrin
Foi modificado da versao 2 dos alunos Paulo e Elvio
Versao 1.2 - data 13 de maio de 2019

Alteracoes:
Foi separado o arquivo de aplicacao de faltas do arquivo de calculos das
funcoes 67
Alterados os graficos para ficarem junto do arquivo de funcoes 67

Apesar de ser possivel entrar com as correntes dos equivalentes S e R,
elas nao foram utilizas, portanto, nao e levado em consideracao o fluxo de
potencia
"""

import numpy as np

from src.tcc.calculos import funcoes67 as f67, faltas as flt
from src.tcc.enums.tpFalta import TpFalta
from src.tcc.enums.tpRele import TpRele
from src.tcc.enums.tpTransformador import TpTransformador
from src.tcc.modelos.equivalente import Equivalente
from src.tcc.modelos.falta import Falta
from src.tcc.modelos.linha import Linha
from src.tcc.modelos.transformador import Transformador
from src.tcc.util.exceptions import ValidacaoException
from src.tcc.util.matriz import Matriz
from src.tcc.util.parametros import Parametros as Param

"""
- Os valores de tensão e corrente podem ser em valores primários ou secundários
- Os valores podem ser na unidade desejada, V, kV, pu, A, kA
- O usuário deve analisar a resposta baseado no dado de entrada
- Sempre utilize tensões de linha, independentemente de estarem em valores
primários ou secundários
- Os ângulos sao em graus
- As impedancias devem ser inseridas na forma retangular R + jX
"""
DEC = 12
# Entrada de dados do sistema equivalente S
equiv_s = Equivalente(230000.0, 0.0, 00.1058 + 10.58j,
                      0.1587 + 15.87j, "Equivalente S")

# Entrada de dados do sistema equivalente R
equiv_r = Equivalente(230000.0, 0.0, 0.7935 + 105.8j, 0.2645 + 79.35j, "Equivalente R")

# Entrada de dados da Linha considerando o modelo pi
# Comprimento da linha em km
# Z da linha como R+jX em ohm/km
# Y da linha como 0+jB em   S/km
linha1 = Linha(33.333*3, (0.2645 + 0.458114j)*3, (0.7935 + 1.374342j)*3, 0 + 0.0000000001j, 0.00 + 0.0000001j, "Linha 1")
linha1.sofreu_falta = True
linha1.analisa_falta = True

linha2 = Linha(33.333, 0.2645 + 0.458114j, 0.7935 + 1.374342j, 0 + 0.0000000001j, 0.00 + 0.0000001j,  "Linha 2")
linha2.analisa_falta = True

linha3 = Linha(33.333, 0.2645 + 0.458114j, 0.7935 + 1.374342j, 0 + 0.0000000001j, 0.00 + 0.0000001j,  "Linha 3")
linha3.analisa_falta = True

linha4 = Linha(33.333, 0.2645 + 0.458114j, 0.7935 + 1.374342j, 0 + 0.0000000001j, 0.00 + 0.0000001j,  "Linha 4")
linha4.analisa_falta = True

# teste linhas
lt = np.around(linha2.z_abc*linha3.z_abc*linha4.z_abc,decimals=8)
l1 = np.around(linha1.z_abc,decimals=8)

lt_r = lt[:3,3:]
l1_r = l1[:3,3:]
# cria o transformador
z_g1 = 0 * np.ones((3, 3))
z_g2 = 0 * np.ones((3, 3))
a_mono = equiv_s.v_mag / equiv_r.v_mag
transformador1 = Transformador(TpTransformador.Yy0, 0.00625 + 0.625j, 0.00625 + 0.625j, a_mono, z_g1, z_g2)
transformador1.analisa_falta = True

transformador2 = Transformador(TpTransformador.Dy1, 1 + 0j, 2 + 0j, 10, z_g1)

# Entrada de dados da falta
# tipo de falta (1-mono(default), 2-bi, 3-biterra, 4-tri, 5-triterra)
# rele = 1-'SEL-311', 2-'GE-D90Plus', 3-'Siemens-7SJ62'
# Porcentagem que cada ponto de falta e aplicado 0.01 = 1%

param_sis = Param(TpFalta.MONO, TpRele.GE_D90PLUS, 0.001, 0.01)

# Montagem da matriz da resistencia de falta

elemento_falta = Falta(param_sis.tipo_falta, param_sis.resistencia_falta)

# Fim da entrada de dados

# Inicio do programa

lista_elementos = [equiv_s, linha1, linha2, linha3, equiv_r]

# Aplicacao da falta e leitura pelos reles
VI_abc_rele_s = []
VI_120_rele_s = []
VI_abc_rele_r = []
VI_120_rele_r = []
dist_falta = []

# verifica se os extremos da lista são equivalentes
if isinstance(lista_elementos[0], Equivalente):
    lista_elementos.pop(0)
else:
    raise ValidacaoException("Primeiro elemento da lista deve ser um equivalente!")

if isinstance(lista_elementos[len(lista_elementos) - 1], Equivalente):
    lista_elementos.pop()
else:
    raise ValidacaoException("Ultimo elemento da lista deve ser um equivalente!")

linha_falta = None
z_120_total = Matriz(np.identity(6))
count = 0

# variaveis para serem usado para aplicar a falta atras caso apenas um elemento tenha sido analisado
lado_dir = Matriz(np.identity(6))
lado_esq = Matriz(np.identity(6))

pre_falta = True
pos_falta = False

# percorre a lista de elementos buscando aqueles a serem analisados
for n in range(0, len(lista_elementos)):
    elemento = lista_elementos[n]

    # Verifica se deve analizar a falta no elemento
    if elemento.analisa_falta:

        lado_dir = np.identity(6)

        # laco para somar a impedancias do lado direito
        for i in range(n + 1, len(lista_elementos)):
            elemento2 = lista_elementos[i]
            lado_dir = np.around(lado_dir * elemento2.z_abc, decimals=DEC)

        comprimento_acumulado = 0
        if len(dist_falta) != 0:
            comprimento_acumulado = dist_falta[len(dist_falta) - 1]

        # verifica se o elemento sofreu falta
        if elemento.sofreu_falta:
            pre_falta = False
            pos_falta = True

        # Caso o elemento seja uma linha, percorre aplicando as faltas
        if isinstance(elemento, Linha):
            linha_falta = elemento
            # chama função que irá percorrer o elemento aplicado as faltas
            s_abc, r_abc, s_120, r_120, dist = flt.percorre_linha_com_falta(linha_falta, param_sis, equiv_s, equiv_r,
                                                                            lado_dir, lado_esq, elemento_falta,
                                                                            pre_falta, comprimento_acumulado)

            # concatena resultado nos vetores
            VI_abc_rele_s += s_abc
            VI_abc_rele_r += r_abc
            VI_120_rele_r += r_120
            VI_120_rele_s += s_120
            dist_falta += dist

        elif isinstance(elemento, Transformador):
            # aplica apenas uma falta antes e uma após o transformador, não faz sentido para este trabalho analizar
            # faltas no interior do transformador

            # Falta reversa ao rele S
            s_abc, r_abc, s_120, r_120 = flt.aplica_falta_transformador(equiv_s, elemento, elemento_falta, equiv_r)

            # concatena elementos
            VI_abc_rele_s += s_abc
            VI_abc_rele_r += r_abc
            VI_120_rele_r += r_120
            VI_120_rele_s += s_120
            dist_falta.append(1)

    # soma impedancia dos elementos ao lado direito,
    # para o caso de vários elementos evitar refazer a soma
    lado_esq = np.around(lado_esq * elemento.z_abc,decimals=DEC)

    # Caso não seja um equivalente somo para calcular o Z total
    # if not isinstance(elemento, Equivalente):

# Atualiza a posição 100% da linha e barra reversa no vetor distancia da falta
# dist_falta.append((dist_falta[len(dist_falta) - 1] + paramS.intervalo_tempo * linha1.compr))

if param_sis.tipo_rele == TpRele.GE_D90PLUS:
    f67.GE_D90Plus(VI_120_rele_s, VI_abc_rele_s, VI_120_rele_r, VI_abc_rele_r, dist_falta)
elif param_sis.tipo_rele == TpRele.SIEMENS_7SJ62:  # Rele Siemens-7SJ62
    f67.Siemens_7SJ62(VI_120_rele_s, VI_abc_rele_s, VI_120_rele_r, VI_abc_rele_r, dist_falta)
else:  # Relé SEL-311L
    f67.rele_SEL_67(VI_120_rele_s, VI_120_rele_r, linha1.z_1, linha1.z_0, dist_falta)

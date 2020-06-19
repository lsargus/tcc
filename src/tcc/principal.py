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

from src.tcc.calculos import funcoes67 as f67, faltas as flt
from src.tcc.modelos.equivalente import Equivalente
from src.tcc.modelos.linha import Linha
from src.tcc.modelos.falta import Falta
from src.tcc.util.matriz import Matriz
from src.tcc.util.parametros import Parametros as Param
from src.tcc.enums.tpFalta import TpFalta
from src.tcc.enums.tpRele import TpRele

"""
- Os valores de tensao e corrente podem ser em valores primarios ou secundarios
- Os valores podem ser na unidade desejada, V, kV, pu, A, kA
- O usuario deve analisar a resposta baseado no dado de entrada
- Sempre utilize tensoes de linha, independentemente de estarem em valores
primarios ou secundarios
- Os angulos sao em graus
- As impedancias devem ser inseridas na forma retangular R + jX
"""

# Entrada de dados do sistema equivalente S
equiv_S = Equivalente(10000.0, 1 + 2j, 2 + 4j)

# Entrada de dados do sistema equivalente R
equiv_R = Equivalente(10000.0, 0.2 + 0.4j, 0.4 + 0.8j)

# Entrada de dados da Linha considerando o modelo pi
# Comprimento da linha em km
# Z da linha como R+jX em ohm/km
# Y da linha como 0+jB em   S/km
linha1 = Linha(400.0, 0.01 + 0.02j, 0.02 + 0.04j, 0.00 + 0.0000002j, 0.00 + 0.0000001j)
linha1.sofreu_falta = True

linha2 = Linha(400.0, 0.01 + 0.02j, 0.02 + 0.04j, 0.00 + 0.0000002j, 0.00 + 0.0000001j)

linha3 = Linha(400.0, 0.01 + 0.02j, 0.02 + 0.04j, 0.00 + 0.0000002j, 0.00 + 0.0000001j)

# Entrada de dados da falta
# tipo de falta (1-mono(default), 2-bi, 3-biterra, 4-tri, 5-triterra)
# rele = 1-'SEL-311', 2-'GE-D90Plus', 3-'Siemens-7SJ62'
# Porcentagem que cada ponto de falta e aplicado 0.01 = 1%

paramS = Param(TpFalta.MONO, TpRele.SEL_311, 0.001, 0.01)

# Montagem da matriz da resistencia de falta

elemento_falta = Falta(paramS.tipo_falta, paramS.resistencia_falta)

# Fim da entrada de dados

# Ini­cio do programa

lista_elementos = [equiv_S, linha1, linha2, linha3, equiv_R]

# Aplicacao da falta e leitura pelos reles
VI_abc_rele_s = []
VI_120_rele_s = []
VI_abc_rele_r = []
VI_120_rele_r = []
dist_falta = [(- paramS.intervalo_tempo * linha1.leng)]

# verifica se os extremos da lista são equivalentes
if isinstance(lista_elementos[0], Equivalente):
    lista_elementos.pop(0)
else:
    raise Exception("Primeiro elemento da lista deve ser um equivalente!")

if isinstance(lista_elementos[len(lista_elementos) - 1], Equivalente):
    lista_elementos.pop()
else:
    raise Exception("Ultimo elemento da lista deve ser um equivalente!")

falta = False
quadr_esq = flt.H6x6
quadr_dir = flt.H6x6
linha_falta = None
z_120_total = flt.H6x6
for elemento in lista_elementos:
    if not elemento.get_falta():
        if not falta:
            quadr_esq = quadr_esq * elemento.z_120
        else:
            quadr_dir = quadr_dir * elemento.z_120
    else:
        if isinstance(elemento, Linha):
            falta = True
            linha_falta = elemento
            z_120_total = quadr_esq * elemento.z_120
        else:
            raise Exception("Apenas pode tem falta em uma linha!")

# Z total
z_120_total = z_120_total * quadr_dir

# Falta reversa ao rele S
S_abc, R_abc, S_120, R_120 = flt.aplica_falta_atras(equiv_S.v_abc, equiv_S.z_abc, z_120_total, elemento_falta.z,
                                                    equiv_R.z_abc, equiv_R.v_abc)
VI_abc_rele_s.append(S_abc)
VI_120_rele_s.append(S_120)
VI_abc_rele_r.append(R_abc)
VI_120_rele_r.append(R_120)

# Faltas na linha
for i in range(0, int(100 / (100 * paramS.intervalo_tempo)) + 1, 1):
    m = i / 100
    zlp1, zlp2 = linha_falta.parametros_linha_frac(m)
    zlp1 = quadr_esq * zlp1
    zlp2 = zlp2 * quadr_dir
    S_abc, R_abc, S_120, R_120 = flt.aplica_falta(equiv_S.v_abc, equiv_S.z_abc, zlp1, zlp2, m, elemento_falta.z,
                                                  equiv_R.z_abc, equiv_R.v_abc)
    VI_abc_rele_s.append(S_abc)
    VI_120_rele_s.append(S_120)
    VI_abc_rele_r.append(R_abc)
    VI_120_rele_r.append(R_120)
    dist_falta.append(m * linha_falta.leng)

# Atualiza a posição 100% da linha e barra reversa no vetor distancia da falta
dist_falta.append((1 + paramS.intervalo_tempo) * linha1.leng)

# Falta reversa ao rele R
R_abc, S_abc, R_120, S_120 = flt.aplica_falta_atras(equiv_R.v_abc, equiv_R.z_abc, z_120_total, elemento_falta.z,
                                                    equiv_S.z_abc, equiv_S.v_abc)
VI_abc_rele_s.append(S_abc)
VI_120_rele_s.append(S_120)
VI_abc_rele_r.append(R_abc)
VI_120_rele_r.append(R_120)

if paramS.tipo_rele == TpRele.GE_D90PLUS:
    f67.GE_D90Plus(VI_120_rele_s, VI_abc_rele_s, VI_120_rele_r, VI_abc_rele_r, dist_falta)
elif paramS.tipo_rele == TpRele.SIEMENS_7SJ62:  # Rele Siemens-7SJ62
    f67.Siemens_7SJ62(VI_120_rele_s, VI_abc_rele_s, VI_120_rele_r, VI_abc_rele_r, dist_falta)
else:  # Relé SEL-311L
    f67.rele_SEL_67(VI_120_rele_s, VI_120_rele_r, linha1.z_1, linha1.z_0, dist_falta)

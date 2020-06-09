# coding=utf8
'''
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
'''

from src.tcc.calculos import funcoes67 as f67, faltas as flt

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
Vs_mag = 130.0
Vs_ang = 10.0
Is_mag = 0.0
Is_ang = 0.0
Zs_1   = 1 + 2j
Zs_0   = 2 + 4j

# Entrada de dados do sistema equivalente R
Vr_mag = 115.0
Vr_ang = 0.0
Ir_mag = 0.0
Ir_ang = 0.0
Zr_1   = 0.2 + 0.4j
Zr_0   = 0.4 + 0.8j

# Entrada de dados da Linha considerando o modelo pi
# Comprimento da linha em km
# Z da linha como R+jX em ohm/km
# Y da linha como 0+jB em   S/km
leng = 200.0
Zl_1 = 0.01+0.02j
Zl_0 = 0.02+0.04j
Yl_1 = 0.00+0.00001j
Yl_0 = 0.00+0.00001j

# Entrada de dados da falta
# tipo de falta (1-mono(default), 2-bi, 3-biterra, 4-tri, 5-triterra)
# rele = 1-'SEL-311', 2-'GE-D90Plus', 3-'Siemens-7SJ62'
Rf   = 0.01
tf   = 1
rele = 1

# Fim da entrada de dados


# Ini�cio do programa

# Porcentagem que cada ponto de falta e aplicado 0.01 = 1%
delta_m = 0.01


# Evita e entrada de Rf = 0
if (Rf == 0.0):
    Rf = 0.01


# Montagem das matrizes do sistema equivalente S
Vs_abc = flt.valor_abc(Vs_mag/3**(1/2), Vs_ang)
Is_abc = flt.valor_abc(Is_mag, Is_ang)
Zs_120 = flt.Z_120_6x6(Zs_1, Zs_0)
Zs_abc = flt.Z_120abc(Zs_120, '120')


# Montagem das matrizes do sistema equivalente R
Vr_abc = flt.valor_abc(Vr_mag/3**(1/2), Vr_ang)
Ir_abc = flt.valor_abc(Ir_mag, Ir_ang)
Zr_120 = flt.Z_120_6x6(Zr_1, Zr_0)
Zr_abc = flt.Z_120abc(Zr_120, '120')


# Montagem da matriz da resistencia de falta monofasica
Zf = flt.falta(tf, Rf)


# Aplicacao da falta e leitura pelos reles
VI_abc_rele_s = []
VI_120_rele_s = []
VI_abc_rele_r = []
VI_120_rele_r = []
dist_falta    = [(-delta_m*leng)]

# Falta reversa ao rele S
S_abc, R_abc, S_120, R_120 = flt.aplica_falta_atras(Vs_abc, Zs_abc, Zl_1, Zl_0, Yl_1, Yl_0, leng, Zf, Zr_abc, Vr_abc)
VI_abc_rele_s.append(S_abc)
VI_120_rele_s.append(S_120)
VI_abc_rele_r.append(R_abc)
VI_120_rele_r.append(R_120)

# Faltas na linha
for i in range(0, int(100/(100*delta_m))+1, 1):
    m = i/100
    S_abc, R_abc, S_120, R_120 = flt.aplica_falta(Vs_abc, Zs_abc, Zl_1, Zl_0, Yl_1, Yl_0, leng, m, Zf, Zr_abc, Vr_abc)
    VI_abc_rele_s.append(S_abc)
    VI_120_rele_s.append(S_120)
    VI_abc_rele_r.append(R_abc)
    VI_120_rele_r.append(R_120)
    dist_falta.append(m*leng)

# Atualiza a posi��o 100% da linha e barra reversa no vetor distancia da falta
dist_falta.append((1+delta_m)*leng)

# Falta reversa ao rele R
R_abc, S_abc, R_120, S_120 = flt.aplica_falta_atras(Vr_abc, Zr_abc, Zl_1, Zl_0, Yl_1, Yl_0, leng, Zf, Zs_abc, Vs_abc)
VI_abc_rele_s.append(S_abc)
VI_120_rele_s.append(S_120)
VI_abc_rele_r.append(R_abc)
VI_120_rele_r.append(R_120)


if rele == 2: # Rele GE-D90Plus
    f67.GE_D90Plus(VI_120_rele_s, VI_abc_rele_s, VI_120_rele_r, VI_abc_rele_r, dist_falta)
elif rele == 3: # Rele Siemens-7SJ62
    f67.Siemens_7SJ62(VI_120_rele_s, VI_abc_rele_s, VI_120_rele_r, VI_abc_rele_r, dist_falta)
else: # Rel� SEL-311L
    f67.rele_SEL_67(VI_120_rele_s, VI_120_rele_r, Zl_1, Zl_0, dist_falta)



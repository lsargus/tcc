"""
Este arquivo contem:
    Matrizes de V e I de ambos os extremos da linha
    Matrizes de impedancias das fontes e linha (curta e longa)
Versao 1.2 - data 13 de maio de 2019

Alteracoes:
Foi separado o arquivo de aplicacao de faltas do de calculos das funcoes 67
"""

# Importacao de modulos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

COMPRIMENTO = "Comprimento (km)"
ANGULO_S = 'angulo s'
ANGULO_R = 'angulo r'


def plota_graficos(x_axes, y_axes_s, y_axes_r, nome_s, nome_r, titulo, tit_y, tit_x):
    porc = [100 * i / x_axes[-2] for i in x_axes]

    fig = plt.figure()
    # Plota grafico em km
    ax1 = fig.add_axes([0.07, 0.15, 0.92, 0.80])
    ax1.plot(x_axes, y_axes_s, 'bx', label=nome_s, lw=3)
    ax1.plot(x_axes, y_axes_r, 'r+', label=nome_r, lw=3)
    ax1.set_title(titulo, fontsize=14)
    ax1.grid(True)
    ax1.set_ylabel(tit_y, fontsize=14)
    ax1.tick_params(labelsize=14)
    ax1.legend(loc='best')

    # Faz um segundo eixo X em %
    ax2 = ax1.twiny()
    ax2.plot(porc, y_axes_s, 'bx')
    ax2.plot(porc, y_axes_r, 'r+')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.spines['bottom'].set_position(('outward', 20))
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax2.set_xlabel('Comprimento em (km) e em (%)', fontsize=14)
    ax2.tick_params(labelsize=14)


def plota_graficos1(x_axes, y_axes_s, y_axes_r, nome_s, nome_r, titulo, tit_y, tit_x):
    plt.figure(figsize=(16, 9))
    plt.axes([0.07, 0.09, 0.92, 0.85])
    plt.plot(x_axes, y_axes_s, 'bx', label=nome_s, lw=3)
    plt.plot(x_axes, y_axes_r, 'r+', label=nome_r, lw=3)
    plt.title(titulo, fontsize=14)
    plt.grid(True)
    plt.ylabel(tit_y, fontsize=14)
    plt.xlabel(tit_x, fontsize=14)
    plt.tick_params(labelsize=14)
    plt.legend(loc='best')


def angulo(retangular):
    real_ret = retangular.real
    imag_ret = retangular.imag
    ang = np.arctan(imag_ret / real_ret)
    ang *= 180 / np.pi
    if (ang > 0 and real_ret < 0) or (ang < 0 and imag_ret > 0):
        ang += 180
    if ang < 0:
        ang += 360
    return ang


def aquisita_modulos(lista, posicao):
    lista_mod = []
    for _ in lista:
        mod = round(abs(lista[posicao, 0]), 2)
        lista_mod.append(mod)
    return lista_mod


def rele_SEL_67(vi_s_120, vi_r_120, z_1, z_0, dist_falta):
    i_2s = []
    a_2s = []
    k_2s = []
    z_2s = []
    i_0s = []
    a_0s = []
    z_0s = []
    i_2r = []
    a_2r = []
    k_2r = []
    z_2r = []
    i_0r = []
    a_0r = []
    z_0r = []
    for i in vi_s_120:
        mod_i1 = abs(i[3, 0])
        mod_i2 = abs(i[4, 0])
        mod_i0 = abs(i[5, 0])
        i_2s.append(round(3 * mod_i2, 4))
        a_2s.append(round(mod_i2 / mod_i1, 4))
        k_2s.append(round(mod_i2 / mod_i0, 4))
        z2 = (i[1, 0] * np.conjugate(i[4, 0] * (z_1 / abs(z_1)))).real / (mod_i2 ** 2)
        z_2s.append(z2)
        i_0s.append(round(3 * mod_i0, 4))
        a_0s.append(round(mod_i0 / mod_i1, 4))
        z0 = ((3 * i[2, 0]) * np.conjugate((3 * i[5, 0]) * (z_0 / abs(z_0)))).real / ((3 * mod_i0) ** 2)
        z_0s.append(z0)
    for i in vi_r_120:
        mod_i1 = abs(i[3, 0])
        mod_i2 = abs(i[4, 0])
        mod_i0 = abs(i[5, 0])
        i_2r.append(round(3 * mod_i2, 4))
        a_2r.append(round(mod_i2 / mod_i1, 4))
        k_2r.append(round(mod_i2 / mod_i0, 4))
        z2 = (i[1, 0] * np.conjugate(i[4, 0] * (z_1 / abs(z_1)))).real / (mod_i2 ** 2)
        z_2r.append(z2)
        i_0r.append(round(3 * mod_i0, 4))
        a_0r.append(round(mod_i0 / mod_i1, 4))
        z0 = ((3 * i[2, 0]) * np.conjugate((3 * i[5, 0]) * (z_0 / abs(z_0)))).real / ((3 * mod_i0) ** 2)
        z_0r.append(z0)

    # Graficos
    plota_graficos(dist_falta, i_2s, i_2r, '3I2s', '3I2r', "3I2 x comp", "3I2 (A)", "Comprimento (km)")
    plota_graficos(dist_falta, a_2s, a_2r, 'a2s', 'a2r', "a2 x comp", "a2", "Comprimento (km)")
    plota_graficos(dist_falta, k_2s, k_2r, 'k2s', 'k2r', "k2 x comp", "k2", "Comprimento (km)")
    plota_graficos(dist_falta, z_2s, z_2r, 'Z2s', 'Z2r', "Z2 x comp", "Z2 (Ohm)", "Comprimento (km)")
    plota_graficos(dist_falta, i_0s, i_0r, '3I0s', '3I0r', "3I0 x comp", "3I0 (A)", "Comprimento (km)")
    plota_graficos(dist_falta, a_0s, a_0r, 'a0s', 'a0r', "a0 x comp", "a0", "Comprimento (km)")
    plota_graficos(dist_falta, z_0s, z_0r, 'Z0s', 'Z0r', "Z0 x comp", "Z0 (Ohm)", "Comprimento (km)")


def GE_D90Plus(vi_s_120, vi_s_abc, vi_r_120, vi_r_abc, dist_falta):
    i_as = []
    i_bs = []
    i_cs = []
    v_bcs = []
    v_cas = []
    v_abs = []
    ang_ia_vbcs = []
    ang_ib_vcas = []
    ang_ic_vabs = []
    ang_3i0_v0s = []
    ang_i2_v2s = []
    for i in vi_s_abc:
        i_a = i[3, 0]
        i_b = i[4, 0]
        i_c = i[5, 0]
        v_a = i[0, 0]
        v_b = i[1, 0]
        v_c = i[2, 0]
        v_ab = v_a - v_b
        v_bc = v_b - v_c
        v_ca = v_c - v_a
        i_as.append(round(abs(i_a), 2))
        i_bs.append(round(abs(i_b), 2))
        i_cs.append(round(abs(i_c), 2))
        v_bcs.append(round(abs(v_bc), 2))
        v_cas.append(round(abs(v_ca), 2))
        v_abs.append(round(abs(v_ab), 2))
        ang_ia_vbc = angulo(i_a) - angulo(v_bc)
        ang_ib_vca = angulo(i_b) - angulo(v_ca)
        ang_ic_vab = angulo(i_c) - angulo(v_ab)
        ang_ia_vbcs.append(round(abs(ang_ia_vbc), 2))
        ang_ib_vcas.append(round(abs(ang_ib_vca), 2))
        ang_ic_vabs.append(round(abs(ang_ic_vab), 2))
    for i in vi_s_120:
        v2 = i[1, 0]
        v0 = i[2, 0]
        i2 = i[4, 0]
        i0 = i[5, 0]
        ang_3i0_v0 = angulo(i0) - angulo(-v0)
        ang_i2_v2 = angulo(i2) - angulo(-v2)
        ang_3i0_v0s.append(round(abs(ang_3i0_v0), 2))
        ang_i2_v2s.append(round(abs(ang_i2_v2), 2))

    i_ar = []
    i_br = []
    i_cr = []
    v_bcr = []
    v_car = []
    v_abr = []
    ang_ia_vbcr = []
    ang_ib_vcar = []
    ang_ic_vabr = []
    ang_3i0_v0r = []
    ang_i2_v2r = []
    for i in vi_r_abc:
        i_a = i[3, 0]
        i_b = i[4, 0]
        i_c = i[5, 0]
        v_a = i[0, 0]
        v_b = i[1, 0]
        v_c = i[2, 0]
        v_ab = v_a - v_b
        v_bc = v_b - v_c
        v_ca = v_c - v_a
        i_ar.append(round(abs(i_a), 2))
        i_br.append(round(abs(i_b), 2))
        i_cr.append(round(abs(i_c), 2))
        v_bcr.append(round(abs(v_bc), 2))
        v_car.append(round(abs(v_ca), 2))
        v_abr.append(round(abs(v_ab), 2))
        ang_ia_vbc = angulo(i_a) - angulo(v_bc)
        ang_ib_vca = angulo(i_b) - angulo(v_ca)
        ang_ic_vab = angulo(i_c) - angulo(v_ab)
        ang_ia_vbcr.append(round(abs(ang_ia_vbc), 2))
        ang_ib_vcar.append(round(abs(ang_ib_vca), 2))
        ang_ic_vabr.append(round(abs(ang_ic_vab), 2))
    for i in vi_r_120:
        v2 = i[1, 0]
        v0 = i[2, 0]
        i2 = i[4, 0]
        i0 = i[5, 0]
        ang_3i0_v0 = angulo(i0) - angulo(-v0)
        ang_i2_v2 = angulo(i2) - angulo(-v2)
        ang_3i0_v0r.append(round(abs(ang_3i0_v0), 2))
        ang_i2_v2r.append(round(abs(ang_i2_v2), 2))

    # Graficos
    plota_graficos(dist_falta, i_as, i_ar, 'Ias', 'Iar', "Ia x comp", "Ia (A)", "Comprimento (km)")
    plota_graficos(dist_falta, v_bcs, v_bcr, 'Vbcs', 'Vbcr', "Vbc x comp", "Vbc (V)", "Comprimento (km)")
    plota_graficos(dist_falta, ang_ia_vbcs, ang_ia_vbcr, ANGULO_S, ANGULO_R, "Angulo IaxVbc x comp",
                   "Angulo IaxVbc (graus)", "Comprimento (km)")
    plota_graficos(dist_falta, ang_3i0_v0s, ang_3i0_v0r, ANGULO_S, ANGULO_R, "Angulo 3I0xV0 x comp",
                   "Angulo 3I0xV0 (graus)", "Comprimento (km)")
    plota_graficos(dist_falta, ang_i2_v2s, ang_i2_v2r, ANGULO_S, ANGULO_R, "Angulo I2xV2 x comp",
                   "Angulo I2xV2 (graus)", "Comprimento (km)")


def Siemens_7SJ62(vi_s_120, vi_s_abc, vi_r_120, vi_r_abc, dist_falta):
    i_as = []
    i_bs = []
    i_cs = []
    v_bcs = []
    v_cas = []
    v_abs = []
    ang_ia_vbcs = []
    ang_ib_vcas = []
    ang_ic_vabs = []
    ang_3i0_3v0s = []
    ang_3i2_3v2s = []
    for i in vi_s_abc:
        i_a = i[3, 0]
        i_b = i[4, 0]
        i_c = i[5, 0]
        v_a = i[0, 0]
        v_b = i[1, 0]
        v_c = i[2, 0]
        v_ab = v_a - v_b
        v_bc = v_b - v_c
        v_ca = v_c - v_a
        i_as.append(round(abs(i_a), 2))
        i_bs.append(round(abs(i_b), 2))
        i_cs.append(round(abs(i_c), 2))
        v_bcs.append(round(abs(v_bc), 2))
        v_cas.append(round(abs(v_ca), 2))
        v_abs.append(round(abs(v_ab), 2))
        ang_ia_vbc = angulo(i_a) - angulo(v_bc)
        ang_ib_vca = angulo(i_b) - angulo(v_ca)
        ang_ic_vab = angulo(i_c) - angulo(v_ab)
        ang_ia_vbcs.append(round(abs(ang_ia_vbc), 2))
        ang_ib_vcas.append(round(abs(ang_ib_vca), 2))
        ang_ic_vabs.append(round(abs(ang_ic_vab), 2))
    for i in vi_s_120:
        v_2 = i[1, 0]
        v_0 = i[2, 0]
        i_2 = i[4, 0]
        i_0 = i[5, 0]
        ang_3i0_3v0 = angulo(-i_0) - angulo(v_0)
        ang_3i2_3v2 = angulo(-i_2) - angulo(v_2)
        ang_3i0_3v0s.append(round(abs(ang_3i0_3v0), 2))
        ang_3i2_3v2s.append(round(abs(ang_3i2_3v2), 2))

    i_ar = []
    i_br = []
    i_cr = []
    v_bcr = []
    v_car = []
    v_abr = []
    ang_ia_vbcr = []
    ang_ib_vcar = []
    ang_ic_vabr = []
    ang_3i0_3v0r = []
    ang_3i2_3v2r = []
    for i in vi_r_abc:
        i_a = i[3, 0]
        i_b = i[4, 0]
        i_c = i[5, 0]
        v_a = i[0, 0]
        v_b = i[1, 0]
        v_c = i[2, 0]
        v_ab = v_a - v_b
        v_bc = v_b - v_c
        v_ca = v_c - v_a
        i_ar.append(round(abs(i_a), 2))
        i_br.append(round(abs(i_b), 2))
        i_cr.append(round(abs(i_c), 2))
        v_bcr.append(round(abs(v_bc), 2))
        v_car.append(round(abs(v_ca), 2))
        v_abr.append(round(abs(v_ab), 2))
        ang_ia_vbc = angulo(i_a) - angulo(v_bc)
        ang_ib_vca = angulo(i_b) - angulo(v_ca)
        ang_ic_vab = angulo(i_c) - angulo(v_ab)
        ang_ia_vbcr.append(round(abs(ang_ia_vbc), 2))
        ang_ib_vcar.append(round(abs(ang_ib_vca), 2))
        ang_ic_vabr.append(round(abs(ang_ic_vab), 2))
    for i in vi_r_120:
        v_2 = i[1, 0]
        v_0 = i[2, 0]
        i_2 = i[4, 0]
        i_0 = i[5, 0]
        ang_3i0_3v0 = angulo(-i_0) - angulo(v_0)
        ang_3i2_3v2 = angulo(-i_2) - angulo(v_2)
        ang_3i0_3v0r.append(round(abs(ang_3i0_3v0), 2))
        ang_3i2_3v2r.append(round(abs(ang_3i2_3v2), 2))

    # Graficos
    plota_graficos(dist_falta, i_as, i_ar, 'i_as', 'Iar', "Ia x comp", "Ia (A)", COMPRIMENTO)
    plota_graficos(dist_falta, v_bcs, v_bcr, 'Vbcs', 'Vbcr', "Vbc x comp", "Vbc (V)", COMPRIMENTO)
    plota_graficos(dist_falta, ang_ia_vbcs, ang_ia_vbcr, ANGULO_S, ANGULO_R, "Angulo IaxVbc x comp",
                   "Angulo IaxVbc (graus)", COMPRIMENTO)
    plota_graficos(dist_falta, ang_3i0_3v0s, ang_3i0_3v0r, ANGULO_S, ANGULO_R, "Angulo 3I0x3V0 x comp",
                   "Angulo 3I0x3V0 (graus)", COMPRIMENTO)
    plota_graficos(dist_falta, ang_3i2_3v2s, ang_3i2_3v2r, ANGULO_S, ANGULO_R, "Angulo 3I2x3V2 x comp",
                   "Angulo 3I2x3V2 (graus)", COMPRIMENTO)

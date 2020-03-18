'''
Este arquivo contem:
    Matrizes de V e I de ambos os extremos da linha
    Matrizes de impedancias das fontes e linha (curta e longa)
Versao 1.2 - data 13 de maio de 2019

Alteracoes:
Foi separado o arquivo de aplicacao de faltas do de calculos das funcoes 67
'''

# Importacao de modulos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plota_graficos(x_axes, y_axes_s, y_axes_r, nome_s, nome_r, titulo, tit_y, tit_x):
    porc = [ 100 * i / x_axes[-2] for i in x_axes ]
    
    fig = plt.figure()
    # Plota grafico em km
    ax1 = fig.add_axes([0.07,0.15,0.92,0.80])
    ax1.plot( x_axes, y_axes_s, 'bx', label=nome_s, lw=3)
    ax1.plot( x_axes, y_axes_r, 'r+', label=nome_r, lw=3)
    ax1.set_title(titulo, fontsize=14)
    ax1.grid(True)
    ax1.set_ylabel(tit_y, fontsize=14)
    ax1.tick_params(labelsize=14)
    ax1.legend(loc='best')
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    
    # Faz um segundo eixo X em %
    ax2 = ax1.twiny()
    ax2.plot( porc, y_axes_s, 'bx')
    ax2.plot( porc, y_axes_r, 'r+')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.spines['bottom'].set_position(('outward', 20))
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax2.set_xlabel('Comprimento em (km) e em (%)', fontsize=14)
    ax2.tick_params(labelsize=14)
    

def plota_graficos1(x_axes, y_axes_s, y_axes_r, nome_s, nome_r, titulo, tit_y, tit_x):
    plt.figure(figsize=(16,9))
    plt.axes([0.07,0.09,0.92,0.85])
    plt.plot( x_axes, y_axes_s, 'bx', label=nome_s, lw=3)
    plt.plot( x_axes, y_axes_r, 'r+', label=nome_r, lw=3)
    plt.title(titulo, fontsize=14)
    plt.grid(True)
    plt.ylabel(tit_y, fontsize=14)
    plt.xlabel(tit_x, fontsize=14)
    plt.tick_params(labelsize=14)
    plt.legend(loc='best')
    mng = plt.get_current_fig_manager()
    mng.window.showMaximized()
    #plt.xlim(min(lista_dist_falta), max(lista_dist_falta))
    
def angulo(retangular):
    real_ret = retangular.real
    imag_ret = retangular.imag
    ang      = np.arctan(imag_ret / real_ret)
    ang     *= 180/np.pi
    if (ang > 0 and real_ret < 0) or (ang < 0 and imag_ret > 0):
        ang += 180
    if ang < 0:
        ang += 360
    return ang
    
def aquisita_modulos(lista, posicao):
    lista_mod = []
    for i in lista:
        mod = round(abs(lista[posicao,0]),2)
        lista_mod.append(mod)
    return lista_mod

def rele_SEL_67(VI_S_120, VI_R_120, Z_1, Z_0, dist_falta):
    I2s = []
    a2s = []
    k2s = []
    Z2s = []
    I0s = []
    a0s = []
    Z0s = []
    I2r = []
    a2r = []
    k2r = []
    Z2r = []
    I0r = []
    a0r = []
    Z0r = []
    for i in VI_S_120:
        modI1 = abs(i[3,0])
        modI2 = abs(i[4,0])
        modI0 = abs(i[5,0])
        I2s.append(round(3*modI2,4))
        a2s.append(round(modI2/modI1,4))
        k2s.append(round(modI2/modI0,4))
        Z2 = ((i[1,0]*np.conjugate(i[4,0]*(Z_1/abs(Z_1)))).real)/(modI2**2)
        Z2s.append(Z2)
        I0s.append(round(3*modI0,4))
        a0s.append(round(modI0/modI1,4))
        Z0 = (((3*i[2,0])*np.conjugate((3*i[5,0])*(Z_0/abs(Z_0)))).real)/((3*modI0)**2)
        Z0s.append(Z0)
    for i in VI_R_120:
        modI1 = abs(i[3,0])
        modI2 = abs(i[4,0])
        modI0 = abs(i[5,0])
        I2r.append(round(3*modI2,4))
        a2r.append(round(modI2/modI1,4))
        k2r.append(round(modI2/modI0,4))
        Z2 = ((i[1,0]*np.conjugate(i[4,0]*(Z_1/abs(Z_1)))).real)/(modI2**2)
        Z2r.append(Z2)
        I0r.append(round(3*modI0,4))
        a0r.append(round(modI0/modI1,4))
        Z0 = (((3*i[2,0])*np.conjugate((3*i[5,0])*(Z_0/abs(Z_0)))).real)/((3*modI0)**2)
        Z0r.append(Z0)

    # Graficos
    plota_graficos(dist_falta, I2s, I2r, '3I2s', '3I2r', "3I2 x comp",  "3I2 (A)", "Comprimento (km)")
    plota_graficos(dist_falta, a2s, a2r,  'a2s',  'a2r',  "a2 x comp",       "a2", "Comprimento (km)")
    plota_graficos(dist_falta, k2s, k2r,  'k2s',  'k2r',  "k2 x comp",       "k2", "Comprimento (km)")
    plota_graficos(dist_falta, Z2s, Z2r,  'Z2s',  'Z2r',  "Z2 x comp", "Z2 (Ohm)", "Comprimento (km)")
    plota_graficos(dist_falta, I0s, I0r, '3I0s', '3I0r', "3I0 x comp",  "3I0 (A)", "Comprimento (km)")
    plota_graficos(dist_falta, a0s, a0r,  'a0s',  'a0r',  "a0 x comp",       "a0", "Comprimento (km)")
    plota_graficos(dist_falta, Z0s, Z0r,  'Z0s',  'Z0r',  "Z0 x comp", "Z0 (Ohm)", "Comprimento (km)")

def GE_D90Plus(VI_S_120, VI_S_abc, VI_R_120, VI_R_abc, dist_falta):
    Ias  = []
    Ibs  = []
    Ics  = []
    Vbcs = []
    Vcas = []
    Vabs = []
    ang_Ia_Vbcs = []
    ang_Ib_Vcas = []
    ang_Ic_Vabs = []
    ang_3I0_V0s = []
    ang_I2_V2s  = []
    for i in VI_S_abc:
        Ia = i[3,0]
        Ib = i[4,0]
        Ic = i[5,0]
        Va = i[0,0]
        Vb = i[1,0]
        Vc = i[2,0]
        Vab = Va-Vb
        Vbc = Vb-Vc
        Vca = Vc-Va
        Ias.append(round(abs(Ia),2))
        Ibs.append(round(abs(Ib),2))
        Ics.append(round(abs(Ic),2))
        Vbcs.append(round(abs(Vbc),2))
        Vcas.append(round(abs(Vca),2))
        Vabs.append(round(abs(Vab),2))
        ang_Ia_Vbc = angulo(Ia)-angulo(Vbc)
        ang_Ib_Vca = angulo(Ib)-angulo(Vca)
        ang_Ic_Vab = angulo(Ic)-angulo(Vab)
        ang_Ia_Vbcs.append(round(abs(ang_Ia_Vbc),2))
        ang_Ib_Vcas.append(round(abs(ang_Ib_Vca),2))
        ang_Ic_Vabs.append(round(abs(ang_Ic_Vab),2))
    for i in VI_S_120:
        V2 = i[1,0]
        V0 = i[2,0]
        I2 = i[4,0]
        I0 = i[5,0]
        ang_3I0_V0 = angulo(I0)-angulo(-V0)
        ang_I2_V2  = angulo(I2)-angulo(-V2)
        ang_3I0_V0s.append(round(abs(ang_3I0_V0),2))
        ang_I2_V2s.append(round(abs(ang_I2_V2),2))
    
    Iar  = []
    Ibr  = []
    Icr  = []
    Vbcr = []
    Vcar = []
    Vabr = []
    ang_Ia_Vbcr = []
    ang_Ib_Vcar = []
    ang_Ic_Vabr = []
    ang_3I0_V0r = []
    ang_I2_V2r  = []
    for i in VI_R_abc:
        Ia = i[3,0]
        Ib = i[4,0]
        Ic = i[5,0]
        Va = i[0,0]
        Vb = i[1,0]
        Vc = i[2,0]
        Vab = Va-Vb
        Vbc = Vb-Vc
        Vca = Vc-Va
        Iar.append(round(abs(Ia),2))
        Ibr.append(round(abs(Ib),2))
        Icr.append(round(abs(Ic),2))
        Vbcr.append(round(abs(Vbc),2))
        Vcar.append(round(abs(Vca),2))
        Vabr.append(round(abs(Vab),2))
        ang_Ia_Vbc = angulo(Ia)-angulo(Vbc)
        ang_Ib_Vca = angulo(Ib)-angulo(Vca)
        ang_Ic_Vab = angulo(Ic)-angulo(Vab)
        ang_Ia_Vbcr.append(round(abs(ang_Ia_Vbc),2))
        ang_Ib_Vcar.append(round(abs(ang_Ib_Vca),2))
        ang_Ic_Vabr.append(round(abs(ang_Ic_Vab),2))
    for i in VI_R_120:
        V2 = i[1,0]
        V0 = i[2,0]
        I2 = i[4,0]
        I0 = i[5,0]
        ang_3I0_V0 = angulo(I0)-angulo(-V0)
        ang_I2_V2  = angulo(I2)-angulo(-V2)
        ang_3I0_V0r.append(round(abs(ang_3I0_V0),2))
        ang_I2_V2r.append(round(abs(ang_I2_V2),2))
    
    # Graficos
    plota_graficos(dist_falta,         Ias,         Iar,      'Ias',      'Iar',            "Ia x comp",                "Ia (A)", "Comprimento (km)")
    plota_graficos(dist_falta,        Vbcs,        Vbcr,     'Vbcs',     'Vbcr',           "Vbc x comp",               "Vbc (V)", "Comprimento (km)")
    plota_graficos(dist_falta, ang_Ia_Vbcs, ang_Ia_Vbcr, 'angulo s', 'angulo r', "Angulo IaxVbc x comp", "Angulo IaxVbc (graus)", "Comprimento (km)")
    plota_graficos(dist_falta, ang_3I0_V0s, ang_3I0_V0r, 'angulo s', 'angulo r', "Angulo 3I0xV0 x comp", "Angulo 3I0xV0 (graus)", "Comprimento (km)")
    plota_graficos(dist_falta,  ang_I2_V2s,  ang_I2_V2r, 'angulo s', 'angulo r',  "Angulo I2xV2 x comp",  "Angulo I2xV2 (graus)", "Comprimento (km)")

def Siemens_7SJ62(VI_S_120, VI_S_abc, VI_R_120, VI_R_abc, dist_falta):
    Ias  = []
    Ibs  = []
    Ics  = []
    Vbcs = []
    Vcas = []
    Vabs = []
    ang_Ia_Vbcs  = []
    ang_Ib_Vcas  = []
    ang_Ic_Vabs  = []
    ang_3I0_3V0s = []
    ang_3I2_3V2s = []
    for i in VI_S_abc:
        Ia = i[3,0]
        Ib = i[4,0]
        Ic = i[5,0]
        Va = i[0,0]
        Vb = i[1,0]
        Vc = i[2,0]
        Vab = Va-Vb
        Vbc = Vb-Vc
        Vca = Vc-Va
        Ias.append(round(abs(Ia),2))
        Ibs.append(round(abs(Ib),2))
        Ics.append(round(abs(Ic),2))
        Vbcs.append(round(abs(Vbc),2))
        Vcas.append(round(abs(Vca),2))
        Vabs.append(round(abs(Vab),2))
        ang_Ia_Vbc = angulo(Ia)-angulo(Vbc)
        ang_Ib_Vca = angulo(Ib)-angulo(Vca)
        ang_Ic_Vab = angulo(Ic)-angulo(Vab)
        ang_Ia_Vbcs.append(round(abs(ang_Ia_Vbc),2))
        ang_Ib_Vcas.append(round(abs(ang_Ib_Vca),2))
        ang_Ic_Vabs.append(round(abs(ang_Ic_Vab),2))
    for i in VI_S_120:
        V2 = i[1,0]
        V0 = i[2,0]
        I2 = i[4,0]
        I0 = i[5,0]
        ang_3I0_3V0 = angulo(-I0)-angulo(V0)
        ang_3I2_3V2 = angulo(-I2)-angulo(V2)
        ang_3I0_3V0s.append(round(abs(ang_3I0_3V0),2))
        ang_3I2_3V2s.append(round(abs(ang_3I2_3V2),2))
    
    Iar  = []
    Ibr  = []
    Icr  = []
    Vbcr = []
    Vcar = []
    Vabr = []
    ang_Ia_Vbcr  = []
    ang_Ib_Vcar  = []
    ang_Ic_Vabr  = []
    ang_3I0_3V0r = []
    ang_3I2_3V2r = []
    for i in VI_R_abc:
        Ia = i[3,0]
        Ib = i[4,0]
        Ic = i[5,0]
        Va = i[0,0]
        Vb = i[1,0]
        Vc = i[2,0]
        Vab = Va-Vb
        Vbc = Vb-Vc
        Vca = Vc-Va
        Iar.append(round(abs(Ia),2))
        Ibr.append(round(abs(Ib),2))
        Icr.append(round(abs(Ic),2))
        Vbcr.append(round(abs(Vbc),2))
        Vcar.append(round(abs(Vca),2))
        Vabr.append(round(abs(Vab),2))
        ang_Ia_Vbc = angulo(Ia)-angulo(Vbc)
        ang_Ib_Vca = angulo(Ib)-angulo(Vca)
        ang_Ic_Vab = angulo(Ic)-angulo(Vab)
        ang_Ia_Vbcr.append(round(abs(ang_Ia_Vbc),2))
        ang_Ib_Vcar.append(round(abs(ang_Ib_Vca),2))
        ang_Ic_Vabr.append(round(abs(ang_Ic_Vab),2))
    for i in VI_R_120:
        V2 = i[1,0]
        V0 = i[2,0]
        I2 = i[4,0]
        I0 = i[5,0]
        ang_3I0_3V0 = angulo(-I0)-angulo(V0)
        ang_3I2_3V2 = angulo(-I2)-angulo(V2)
        ang_3I0_3V0r.append(round(abs(ang_3I0_3V0),2))
        ang_3I2_3V2r.append(round(abs(ang_3I2_3V2),2))
    
    # Graficos
    plota_graficos(dist_falta,          Ias,          Iar,      'Ias',      'Iar',             "Ia x comp",                 "Ia (A)", "Comprimento (km)")
    plota_graficos(dist_falta,         Vbcs,         Vbcr,     'Vbcs',     'Vbcr',            "Vbc x comp",                "Vbc (V)", "Comprimento (km)")
    plota_graficos(dist_falta,  ang_Ia_Vbcs,  ang_Ia_Vbcr, 'angulo s', 'angulo r',  "Angulo IaxVbc x comp",  "Angulo IaxVbc (graus)", "Comprimento (km)")
    plota_graficos(dist_falta, ang_3I0_3V0s, ang_3I0_3V0r, 'angulo s', 'angulo r', "Angulo 3I0x3V0 x comp", "Angulo 3I0x3V0 (graus)", "Comprimento (km)")
    plota_graficos(dist_falta, ang_3I2_3V2s, ang_3I2_3V2r, 'angulo s', 'angulo r', "Angulo 3I2x3V2 x comp", "Angulo 3I2x3V2 (graus)", "Comprimento (km)")



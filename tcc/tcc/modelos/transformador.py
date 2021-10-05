import numpy as np

from src.tcc.calculos import faltas as flt
from src.tcc.enums.tpTransformador import TpTransformador
from src.tcc.modelos.elemento import Elemento
from src.tcc.util.exceptions import ValidacaoException
from src.tcc.util.matriz import Matriz

"""
Classe que deve representar os transformadores
"""


def valida_transformadores(z_1: complex, z_0: complex, a):
    """
    Realiza a validação dos dados do transformador
    :param z_1: impedancia positiva
    :param z_0: impedancia zero
    :param a: relação de transformação
    :return:
    """
    if z_0 is None or z_1 is None:
        raise ValidacaoException("Os valores de impedancia positiva e zero devem ser informados!")
    if a is None:
        raise ValidacaoException("Relação de transformação do transformador deve ser fornecido!")


class Transformador(Elemento):
    def __init__(self, tipo: TpTransformador, z_1: complex, z_0: complex, a, z_g1=None, z_g2=None):
        self.__tipo = tipo
        self.__z_1 = z_1
        self.__z_0 = z_0
        self.__a = a
        self.__z_g1 = z_g1
        self.__z_g2 = z_g2

        valida_transformadores(z_1, z_0, a)

        self.z_120 = flt.z_120_6x6(z_1, z_0)
        z_abc = flt.z_120abc(self.z_120, '120')

        self.M_imp = z_abc

        if tipo == TpTransformador.Yy0:
            if z_g1 is None or z_g2 is None:
                raise ValidacaoException("Para o transformador Yy0 as duas impedancias de aterramento devem ser "
                                         "fornecidas!")

            a_t = Matriz(a * np.identity(3))
            b_t = Matriz((a * z_g2 + z_g1 / a) * np.ones((3, 3)))
            c_t = Matriz(np.zeros((3, 3)))
            d_t = Matriz((1 / a) * np.identity(3))

            self.M_trans = Matriz.concatena_vertical(Matriz.concatena_horizontal(a_t, b_t),
                                                     Matriz.concatena_horizontal(c_t, d_t))

        # verifica para os outros 4 transformadores a impedancia de aterramento
        elif (z_g1 is None and z_g2 is None) or (z_g1 is not None and z_g2 is not None):
            raise ValidacaoException("Para o transformador Dy1 apenas uma impedancias de aterramento devem ser "
                                     "fornecidas!")

        # Verifica qual das impedancias foi fornecida
        z_g = z_g1 if z_g2 is None else z_g2

        if tipo == TpTransformador.Dy1:
            a_t = Matriz((-(a / 3) * np.ones((3, 3))) * [[0, 2, 1], [1, 0, 2], [2, 1, 0]])
            b_t = Matriz(-(a * z_g) * np.ones((3, 3)))
            c_t = Matriz(np.zeros((3, 3)))
            d_t = Matriz(((1 / a) * np.ones((3, 3))) * [[1, -1, 0], [0, 1, -1], [-1, 0, 1]])

            self.M_trans = Matriz.concatena_vertical(Matriz.concatena_horizontal(a_t, b_t),
                                                     Matriz.concatena_horizontal(c_t, d_t))

        elif tipo == TpTransformador.Dy11:
            a_t = Matriz(((a / 3) * np.ones((3, 3))) * [[2, 1, 0], [0, 2, 1], [1, 0, 2]])
            b_t = Matriz((a * z_g) * np.ones((3, 3)))
            c_t = Matriz(np.zeros((3, 3)))
            d_t = Matriz(((1 / a) * np.ones((3, 3))) * [[1, 0, -1], [-1, 1, 0], [0, -1, 1]])

            self.M_trans = Matriz.concatena_vertical(Matriz.concatena_horizontal(a_t, b_t),
                                                     Matriz.concatena_horizontal(c_t, d_t))

        elif tipo == TpTransformador.Yd11:
            a_t = Matriz(((a / 3) * np.ones((3, 3))) * [[2, -1, -1], [-4, 2, -1], [-1, -4, 2]])
            b_t = Matriz(-(a * z_g) * np.ones((3, 3)))
            c_t = Matriz(np.zeros((3, 3)))
            d_t = Matriz(((1 / (3 * a)) * np.ones((3, 3))) * [[4, -2, 1], [1, 4, -2], [-2, 1, 4]])

            self.M_trans = Matriz.concatena_vertical(Matriz.concatena_horizontal(a_t, b_t),
                                                     Matriz.concatena_horizontal(c_t, d_t))

        elif tipo == TpTransformador.Yd1:
            a_t = Matriz(((a / 3) * np.ones((3, 3))) * [[4, -2, 1], [1, 4, -2], [-2, 1, 4]])
            b_t = Matriz((a * z_g) * np.ones((3, 3)))
            c_t = Matriz(np.zeros((3, 3)))
            d_t = Matriz(((1 / (3 * a)) * np.ones((3, 3))) * [[2, -1, -4], [-4, 2, -1], [-1, -4, 2]])

            self.M_trans = Matriz.concatena_vertical(Matriz.concatena_horizontal(a_t, b_t),
                                                     Matriz.concatena_horizontal(c_t, d_t))

        self.z_abc = self.M_imp * self.M_trans
        self.z_120 = flt.z_120abc(self.z_abc, 'abc')

    def inverter_transf(self):
        return Transformador(self.__tipo, self.__a * self.__a * self.__z_1,
                             self.__a * self.__a * self.__z_2,
                             1 / self.__a, self.__z_g2, self.__z_g1)

    @property
    def tipo(self):
        return self.__tipo

    @property
    def z_1(self):
        return self.__z_1

    @property
    def z_0(self):
        return self.__z_0

    @property
    def a(self):
        return self.__a

    @property
    def z_g1(self):
        return self.__z_g1

    @property
    def z_g2(self):
        return self.__z_g2

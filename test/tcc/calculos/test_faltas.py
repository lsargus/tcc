from unittest import TestCase

import numpy as np

from src.tcc.calculos import funcoes67 as f67, faltas as flt
from src.tcc.enums.tpFalta import TpFalta
from src.tcc.enums.tpRele import TpRele
from src.tcc.enums.tpTransformador import TpTransformador
from src.tcc.modelos.equivalente import Equivalente
from src.tcc.modelos.falta import Falta
from src.tcc.modelos.transformador import Transformador
from src.tcc.util.parametros import Parametros as Param


class Test(TestCase):

    def setUp(self):
        # Parametros
        self.param = Param(TpFalta.MONO, TpRele.GE_D90PLUS, 0.0001, 0.01)
        # dados falta
        self.elemento_falta = Falta(self.param.tipo_falta, self.param.resistencia_falta)

        # Entrada de dados do sistema equivalente S
        self.equiv_s = Equivalente(25000.0, 0.0, 1 + 2j, 2 + 4j, "Equivalente S")

        # Entrada de dados do sistema equivalente R
        self.equiv_r = Equivalente(230000.0, 0.0, 0.2 + 0.4j, 0.4 + 0.8j, "Equivalente R")

        # cria o transformador
        z_g1 = 5.0 + 3.0j * np.ones((3, 3))
        z_g2 = 10.0 + 6.0j * np.ones((3, 3))
        a_mono = self.equiv_s.v_mag / self.equiv_r.v_mag
        self.transformador = Transformador(TpTransformador.Yy0, (0.1 + 10.0j) / 2, (0.1 + 10.0j) / 2,
                                           a_mono, z_g1, z_g2)
        self.transformador.analisa_falta = True

    def test_aplica_falta_transformador_monofásico(self):
        """
        Realiza o teste em um transformador aplicando uma falta monofásica na fase A
        """
        s_abc, r_abc, s_120, r_120 = flt.aplica_falta_transformador(self.equiv_s, self.transformador,
                                                                    self.elemento_falta, self.equiv_r)

        self.assertAlmostEqual(s_abc[0][0], 26.77283896 - 57.1719845j, delta=1)
        self.assertAlmostEqual(s_abc[0][1], 11062.72650944 + 275.3459379j, delta=1)
        self.assertAlmostEqual(s_abc[1][0], -11713.0044098 - 11432.78490095j, delta=1)
        self.assertAlmostEqual(s_abc[1][1], -7345.7598496 - 13226.44768304j, delta=1)
        self.assertAlmostEqual(s_abc[2][0], -11713.0044098 + 13567.21509905j, delta=1)
        self.assertAlmostEqual(s_abc[2][1], -7345.75984952 + 11773.55231689j, delta=1)
        self.assertAlmostEqual(s_abc[3][0], 2262.77492017 - 4122.16815358j, delta=1)
        self.assertAlmostEqual(s_abc[3][1], 364.60460106 - 1200.81337907j, delta=1)
        self.assertAlmostEqual(s_abc[4][0], -169.15148242 - 382.70243195j, delta=1)
        self.assertAlmostEqual(s_abc[4][1], 116.89230165 + 296.40484068j, delta=1)
        self.assertAlmostEqual(s_abc[5][0], -169.15148242 - 382.70243195j, delta=1)
        self.assertAlmostEqual(s_abc[5][1], 116.89230165 + 296.40484067j, delta=1)

        self.assertAlmostEqual(r_abc[0][0], 1.32886401e+05 - 1.17539028e+01j, delta=1)
        self.assertAlmostEqual(r_abc[0][1], 2.64562926e+05 + 1.96300705e+03j, delta=1)
        self.assertAlmostEqual(r_abc[1][0], -6.63907643e+04 - 1.14979427e+05j, delta=1)
        self.assertAlmostEqual(r_abc[1][1], -3.34366709e+04 - 1.14526537e+05j, delta=1)
        self.assertAlmostEqual(r_abc[2][0], -6.63907643e+04 + 1.15020573e+05j, delta=1)
        self.assertAlmostEqual(r_abc[2][1], -3.34366709e+04 + 1.15473463e+05j, delta=1)
        self.assertAlmostEqual(r_abc[3][0], -4.50553235e+01 + 1.73372858e+02j, delta=1)
        self.assertAlmostEqual(r_abc[3][1], -1.01780137e+05 + 1.96170182e+05j, delta=1)
        self.assertAlmostEqual(r_abc[4][0], -1.83860307e+01 - 4.15980904e+01j, delta=1)
        self.assertAlmostEqual(r_abc[4][1], 1.27056850e+01 + 3.22179175e+01j, delta=1)
        self.assertAlmostEqual(r_abc[5][0], -1.83860307e+01 - 4.15980904e+01j, delta=1)
        self.assertAlmostEqual(r_abc[5][1], 1.27056850e+01 + 3.22179175e+01j, delta=1)

        self.assertAlmostEqual(s_120[0][0], 11130.13744779 - 374.79569452j, delta=1)
        self.assertAlmostEqual(s_120[0][1], 13353.04048452 + 333.93120697j, delta=1)
        self.assertAlmostEqual(s_120[1][0], -3303.61928195 - 374.79569452j, delta=1)
        self.assertAlmostEqual(s_120[1][1], -1080.71624518 + 333.93120702j, delta=1)
        self.assertAlmostEqual(s_120[2][0], -7799.74532688 + 692.41940453j, delta=1)
        self.assertAlmostEqual(s_120[2][1], -1209.59772989 - 392.51647608j, delta=1)
        self.assertAlmostEqual(s_120[3][0], 810.6421342 - 1246.48857388j, delta=1)
        self.assertAlmostEqual(s_120[3][1], 82.57076647 - 499.07273991j, delta=1)
        self.assertAlmostEqual(s_120[4][0], 810.6421342 - 1246.48857388j, delta=1)
        self.assertAlmostEqual(s_120[4][1], 82.57076648 - 499.07273992j, delta=1)
        self.assertAlmostEqual(s_120[5][0], 641.49065178 - 1629.19100583j, delta=1)
        self.assertAlmostEqual(s_120[5][1], 199.46306812 - 202.66789924j, delta=1)

        self.assertAlmostEqual(r_120[0][0], 1.32821003e+05 - 1.07754909e+01j, delta=1)
        self.assertAlmostEqual(r_120[0][1], 1.65728480e+05 + 4.96514692e+02j, delta=1)
        self.assertAlmostEqual(r_120[1][0], 3.04407460e+01 - 1.07754909e+01j, delta=1)
        self.assertAlmostEqual(r_120[1][1], 3.29379180e+04 + 4.96514692e+02j, delta=1)
        self.assertAlmostEqual(r_120[2][0], 3.49574320e+01 + 9.79707897e+00j, delta=1)
        self.assertAlmostEqual(r_120[2][1], 6.58965281e+04 + 9.69977669e+02j, delta=1)
        self.assertAlmostEqual(r_120[3][0], -8.88976425e+00 + 7.16569829e+01j, delta=1)
        self.assertAlmostEqual(r_120[3][1], -3.39309474e+04 + 6.53793214e+04j, delta=1)
        self.assertAlmostEqual(r_120[4][0], -8.88976425e+00 + 7.16569829e+01j, delta=1)
        self.assertAlmostEqual(r_120[4][1], -3.39309474e+04 + 6.53793214e+04j, delta=1)
        self.assertAlmostEqual(r_120[5][0], -2.72757950e+01 + 3.00588925e+01j, delta=1)
        self.assertAlmostEqual(r_120[5][1], -3.39182417e+04 + 6.54115393e+04j, delta=1)

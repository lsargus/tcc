import unittest

from tcc.enums.tpFalta import TpFalta
from tcc.enums.tpRele import TpRele
from tcc.enums.tpTransformador import TpTransformador
from tcc.simulador.modelos.equivalente import Equivalente
from tcc.simulador.modelos.falta import Falta
from tcc.simulador.modelos.linha import Linha
from tcc.simulador.modelos.transformador import Transformador
from tcc.simulador.simulador import Simulador
from tcc.simulador.util.parametros import Parametros


class SimuladorTest(unittest.TestCase):
    def setUp(self):
        """
        O método setUp é chamado toda vez antes de um teste
        """
        # Entrada de dados do sistema equivalente S
        self.equiv_s = Equivalente(25000.0, 0.0, 0.0125 + 1.251875j,
                                   0.001875 + 0.1875j, "Equivalente S")

        # Entrada de dados do sistema equivalente R
        self.equiv_r = Equivalente(230000.0, 0.0, 0.3703 + 132.25j, 0.785036 + 68.5j, "Equivalente R")

        # Entrada de dados da Linha considerando o modelo pi
        self.linha1 = Linha(100, 0.003125 + 0.0054125j, 0.009375 + 0.0162375j, 0 + 0.0000000001j, 0.00 + 0.0000001j,
                            "Linha 1")
        self.linha1.sofreu_falta = True
        self.linha1.analisa_falta = True

        self.linha2 = Linha(100, 0.003125 + 0.0054125j, 0.009375 + 0.0162375j, 0 + 0.0000000001j, 0.00 + 0.0000001j,
                            "Linha 2")
        self.linha2.analisa_falta = True

        self.linha3 = Linha(100, 0.2645 + 0.458114j, 0.7935 + 1.374342j, 0 + 0.0000000001j, 0.00 + 0.0000001j,
                            "Linha 3")
        self.linha3.analisa_falta = True

        self.linha4 = Linha(100, 0.2645 + 0.458114j, 0.7935 + 1.374342j, 0 + 0.0000000001j, 0.00 + 0.0000001j,
                            "Linha 4")
        self.linha4.analisa_falta = True

        self.linha5 = Linha(100, 0.2645 + 0.458114j, 0.7935 + 1.374342j, 0 + 0.0000000001j, 0.00 + 0.0000001j,
                            "Linha 5")
        self.linha5.analisa_falta = True

        self.transformador1 = Transformador(TpTransformador.Yy0, 0.003125 + 0.3125j, 0.003125 + 0.3125j, (25000/230000), 0, 0)
        self.transformador1.analisa_falta = True

        self.param_sis = Parametros(TpFalta.MONO, TpRele.GE_D90PLUS, 0.001, 0.01)

        self.elemento_falta = Falta(self.param_sis.tipo_falta, self.param_sis.resistencia_falta)

    def test_circuito(self):
        simulacao = Simulador(self.elemento_falta, self.param_sis)
        simulacao.add_elemento(self.equiv_s) \
            .add_elemento(self.linha1) \
            .add_elemento(self.linha2) \
            .add_elemento(self.transformador1) \
            .add_elemento(self.linha3) \
            .add_elemento(self.linha4) \
            .add_elemento(self.linha5) \
            .add_elemento(self.equiv_r) \
            .add_conexao(self.equiv_s, self.linha1) \
            .add_conexao(self.linha1, self.linha2) \
            .add_conexao(self.linha2, self.transformador1) \
            .add_conexao(self.transformador1, self.linha3) \
            .add_conexao(self.linha3, self.linha4) \
            .add_conexao(self.linha4, self.linha5) \
            .add_conexao(self.linha5, self.equiv_r)\
            .start()

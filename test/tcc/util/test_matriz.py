# coding:utf-8
import unittest

import numpy

from src.tcc.util.matriz import Matriz


class VerificarMatrizTests(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    # método __new__
    # ------------------------------------------------------------------------------------------------------------------

    def test_new_cria_matriz_2d_3x3(self):
        """
        Testa a criação de uma matriz com o mesmo nr de colunas e linhas
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[0][1], 2)
        self.assertEqual(m[0][2], 3)
        self.assertEqual(m[1][0], 4)
        self.assertEqual(m[1][1], 5)
        self.assertEqual(m[1][2], 6)
        self.assertEqual(m[2][0], 7)
        self.assertEqual(m[2][1], 8)
        self.assertEqual(m[2][2], 9)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(m, Matriz)

    def test_new_cria_matriz_2d_3x3_complexa(self):
        """
        Testa a criação de uma matriz com o mesmo nr de colunas e linhas
        """
        m = Matriz([[1 + 2j, 2 + 3j, 3 + 4j], [4 + 5j, 5 + 6j, 6 + 7j], [7 + 8j, 8 + 9j, 9 + 1j]])

        self.assertEqual(m[0][0], 1 + 2j)
        self.assertEqual(m[0][1], 2 + 3j)
        self.assertEqual(m[0][2], 3 + 4j)
        self.assertEqual(m[1][0], 4 + 5j)
        self.assertEqual(m[1][1], 5 + 6j)
        self.assertEqual(m[1][2], 6 + 7j)
        self.assertEqual(m[2][0], 7 + 8j)
        self.assertEqual(m[2][1], 8 + 9j)
        self.assertEqual(m[2][2], 9 + 1j)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(m, Matriz)

    def test_new_cria_matriz_2d_2x3(self):
        """
        Testa a criação de uma matriz com mais colunas que linhas
        """
        m = Matriz([[1, 2, 3], [4, 5, 6]])

        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[0][1], 2)
        self.assertEqual(m[0][2], 3)
        self.assertEqual(m[1][0], 4)
        self.assertEqual(m[1][1], 5)
        self.assertEqual(m[1][2], 6)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(m, Matriz)

    def test_new_cria_matriz_2d_3x2(self):
        """
        Testa a criação de uma matriz com mais linhas que colunas
        """
        m = Matriz([[1, 2], [4, 5], [7, 8]])

        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[0][1], 2)
        self.assertEqual(m[1][0], 4)
        self.assertEqual(m[1][1], 5)
        self.assertEqual(m[2][0], 7)
        self.assertEqual(m[2][1], 8)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(m, Matriz)

    def test_new_cria_matriz_1d_linha(self):
        """
        Testa a criação de uma matriz linha.
        """
        m = Matriz([[1, 2, 3, 4]])

        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[0][1], 2)
        self.assertEqual(m[0][2], 3)
        self.assertEqual(m[0][3], 4)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(m, Matriz)

    def test_new_cria_matriz_1d_coluna(self):
        """
        Testa a criação de uma matriz coluna.
        """
        m = Matriz([[1], [2], [3], [4]])

        self.assertEqual(m[0][0], 1)
        self.assertEqual(m[1][0], 2)
        self.assertEqual(m[2][0], 3)
        self.assertEqual(m[3][0], 4)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(m, Matriz)

    def test_new_cria_matriz_3d(self):
        """
        Testa a criação de uma matriz com 3 dimensões.
        Teste deve falhar
        """
        with self.assertRaises(ValueError):
            Matriz([[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]])

    # ------------------------------------------------------------------------------------------------------------------
    # método nr_linhas
    # ------------------------------------------------------------------------------------------------------------------

    def test_nr_linhas_retorna_nr_de_linhas(self):
        m1 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = Matriz([[1, 2, 3], [4, 5, 6]])
        m3 = Matriz([[1, 2], [4, 5], [7, 8], [10, 11]])

        self.assertEqual(m1.nr_linhas(), 3)
        self.assertEqual(m2.nr_linhas(), 2)
        self.assertEqual(m3.nr_linhas(), 4)

    # ------------------------------------------------------------------------------------------------------------------
    # método nr_colunas
    # ------------------------------------------------------------------------------------------------------------------

    def test_nr_colunas_retorna_nr_de_colunas(self):
        m1 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = Matriz([[1, 2, 3], [4, 5, 6]])
        m3 = Matriz([[1, 2], [4, 5], [7, 8], [10, 11]])

        self.assertEqual(m1.nr_colunas(), 3)
        self.assertEqual(m2.nr_colunas(), 3)
        self.assertEqual(m3.nr_colunas(), 2)

    # ------------------------------------------------------------------------------------------------------------------
    # método __mul__
    # ------------------------------------------------------------------------------------------------------------------

    def test_mul_multiplica_matriz_por_constante_int(self):
        """
        Testa a multiplicação de uma matriz por um inteiro
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m * 2

        self.assertEqual(r[0][0], 2)
        self.assertEqual(r[0][1], 4)
        self.assertEqual(r[0][2], 6)
        self.assertEqual(r[1][0], 8)
        self.assertEqual(r[1][1], 10)
        self.assertEqual(r[1][2], 12)
        self.assertEqual(r[2][0], 14)
        self.assertEqual(r[2][1], 16)
        self.assertEqual(r[2][2], 18)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_constante_int_por_matriz(self):
        """
        Testa a multiplicação de um inteiro por uma matriz
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = 2 * m

        self.assertEqual(r[0][0], 2)
        self.assertEqual(r[0][1], 4)
        self.assertEqual(r[0][2], 6)
        self.assertEqual(r[1][0], 8)
        self.assertEqual(r[1][1], 10)
        self.assertEqual(r[1][2], 12)
        self.assertEqual(r[2][0], 14)
        self.assertEqual(r[2][1], 16)
        self.assertEqual(r[2][2], 18)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_matriz_por_constante_float(self):
        """
        Testa a multiplicação de uma matriz por um float.
         Utiliza doze casas decimais e aceita uma diferença de 0.000000000001
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m * 2.2

        self.assertAlmostEqual(r[0][0], 2.2, 12, 0.000000000001)
        self.assertAlmostEqual(r[0][1], 4.4, 12, 0.000000000001)
        self.assertAlmostEqual(r[0][2], 6.6, 12, 0.000000000001)
        self.assertAlmostEqual(r[1][0], 8.8, 12, 0.000000000001)
        self.assertAlmostEqual(r[1][1], 11.0, 12, 0.000000000001)
        self.assertAlmostEqual(r[1][2], 13.2, 12, 0.000000000001)
        self.assertAlmostEqual(r[2][0], 15.4, 12, 0.000000000001)
        self.assertAlmostEqual(r[2][1], 17.6, 12, 0.000000000001)
        self.assertAlmostEqual(r[2][2], 19.8, 12, 0.000000000001)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_constante_float_por_matriz(self):
        """
        Testa a multiplicação de um float por uma matriz.
         Utiliza oito casas decimais e aceita uma diferença de 0.00000001
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = 2.2 * m

        self.assertAlmostEqual(r[0][0], 2.2, delta=1e-8)
        self.assertAlmostEqual(r[0][1], 4.4, delta=1e-8)
        self.assertAlmostEqual(r[0][2], 6.6, delta=1e-8)
        self.assertAlmostEqual(r[1][0], 8.8, delta=1e-8)
        self.assertAlmostEqual(r[1][1], 11.0, delta=1e-8)
        self.assertAlmostEqual(r[1][2], 13.2, delta=1e-8)
        self.assertAlmostEqual(r[2][0], 15.4, delta=1e-8)
        self.assertAlmostEqual(r[2][1], 17.6, delta=1e-8)
        self.assertAlmostEqual(r[2][2], 19.8, delta=1e-8)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_matriz_por_complex(self):
        """
        Testa a multiplicação de uma matriz por um complexo
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m * (2 + 1j)

        self.assertEqual(r[0][0], 1 * (2 + 1j))
        self.assertEqual(r[0][1], 2 * (2 + 1j))
        self.assertEqual(r[0][2], 3 * (2 + 1j))
        self.assertEqual(r[1][0], 4 * (2 + 1j))
        self.assertEqual(r[1][1], 5 * (2 + 1j))
        self.assertEqual(r[1][2], 6 * (2 + 1j))
        self.assertEqual(r[2][0], 7 * (2 + 1j))
        self.assertEqual(r[2][1], 8 * (2 + 1j))
        self.assertEqual(r[2][2], 9 * (2 + 1j))
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_complex_por_matriz(self):
        """
        Testa a multiplicação de um complexo por uma matriz
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = (2 + 1j) * m

        self.assertEqual(r[0][0], 1 * (2 + 1j))
        self.assertEqual(r[0][1], 2 * (2 + 1j))
        self.assertEqual(r[0][2], 3 * (2 + 1j))
        self.assertEqual(r[1][0], 4 * (2 + 1j))
        self.assertEqual(r[1][1], 5 * (2 + 1j))
        self.assertEqual(r[1][2], 6 * (2 + 1j))
        self.assertEqual(r[2][0], 7 * (2 + 1j))
        self.assertEqual(r[2][1], 8 * (2 + 1j))
        self.assertEqual(r[2][2], 9 * (2 + 1j))
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_matriz_3x3_por_matriz_3x3(self):
        """
        Testa a multiplicação de uma matriz quadrada por outra matriz quadrada
        """
        m1 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m2 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m1 * m2

        self.assertEqual(r[0][0], 30)
        self.assertEqual(r[0][1], 36)
        self.assertEqual(r[0][2], 42)
        self.assertEqual(r[1][0], 66)
        self.assertEqual(r[1][1], 81)
        self.assertEqual(r[1][2], 96)
        self.assertEqual(r[2][0], 102)
        self.assertEqual(r[2][1], 126)
        self.assertEqual(r[2][2], 150)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_matriz_3x3_complex_por_matriz_3x3_complex(self):
        """
        Testa a multiplicação de uma matriz quadrada por outra matriz quadrada
        """
        m1 = Matriz([[1 + 2j, 2 + 3j, 3 + 4j], [4 + 5j, 5 + 6j, 6 + 7j], [7 + 8j, 8 + 9j, 9 + 1j]])
        m2 = Matriz([[1 + 2j, 2 + 3j, 3 + 4j], [4 + 5j, 5 + 6j, 6 + 7j], [7 + 8j, 8 + 9j, 9 + 1j]])

        r = m1 * m2

        self.assertEqual(r[0][0], - 21. + 78.j)
        self.assertEqual(r[0][1], - 24. + 93.j)
        self.assertEqual(r[0][2], + 9. + 81.j)
        self.assertEqual(r[1][0], - 30. + 159.j)
        self.assertEqual(r[1][1], - 33. + 192.j)
        self.assertEqual(r[1][2], + 27. + 171.j)
        self.assertEqual(r[2][0], + 33. + 177.j)
        self.assertEqual(r[2][1], + 39. + 219.j)
        self.assertEqual(r[2][2], + 54. + 180.j)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_matriz_3x3_complex_por_matriz_3x3(self):
        """
        Testa a multiplicação de uma matriz quadrada por outra matriz quadrada
        """
        m1 = Matriz([[1 + 2j, 2 + 3j, 3 + 4j], [4 + 5j, 5 + 6j, 6 + 7j], [7 + 8j, 8 + 9j, 9 + 1j]])
        m2 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m1 * m2

        self.assertEqual(r[0][0], 30. + 42.j)
        self.assertEqual(r[0][1], 36. + 51.j)
        self.assertEqual(r[0][2], 42. + 60.j)
        self.assertEqual(r[1][0], 66. + 78.j)
        self.assertEqual(r[1][1], 81. + 96.j)
        self.assertEqual(r[1][2], 96. + 114.j)
        self.assertEqual(r[2][0], 102. + 51.j)
        self.assertEqual(r[2][1], 126. + 69.j)
        self.assertEqual(r[2][2], 150. + 87.j)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_matriz_3x2_por_matriz_2x3_(self):
        """
        Testa a multiplicação de uma matriz 3x2 por outra matriz 2x3
        """
        m1 = Matriz([[1, 2], [4, 5], [7, 8]])
        m2 = Matriz([[1, 2, 3], [4, 5, 6]])

        r = m1 * m2

        self.assertEqual(r[0][0], 9)
        self.assertEqual(r[0][1], 12)
        self.assertEqual(r[0][2], 15)
        self.assertEqual(r[1][0], 24)
        self.assertEqual(r[1][1], 33)
        self.assertEqual(r[1][2], 42)
        self.assertEqual(r[2][0], 39)
        self.assertEqual(r[2][1], 54)
        self.assertEqual(r[2][2], 69)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_mul_multiplica_matriz_2x3_por_matriz_2x3_(self):
        """
        Testa a multiplicação de uma matriz 2x3 por outra matriz 2x3.
        Deve falhar.
        """
        m1 = Matriz([[1, 2], [4, 5], [7, 8]])
        m2 = Matriz([[1, 2], [4, 5], [7, 8]])

        with self.assertRaises(AssertionError):
            m1 * m2

    # ------------------------------------------------------------------------------------------------------------------
    # método __div__
    # ------------------------------------------------------------------------------------------------------------------

    def test_div_divide_matriz_por_inteiro(self):
        """
        Testa a divisão de um matriz por uma inteiro.
         Utiliza oito casas decimais e aceita uma diferença de 0.00000001
        """
        m1 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m1 / 3

        self.assertAlmostEqual(r[0][0], 0.333333333, delta=1e-8)
        self.assertAlmostEqual(r[0][1], 0.666666666, delta=1e-8)
        self.assertAlmostEqual(r[0][2], 1.0, delta=1e-8)
        self.assertAlmostEqual(r[1][0], 1.333333333, delta=1e-8)
        self.assertAlmostEqual(r[1][1], 1.666666666, delta=1e-8)
        self.assertAlmostEqual(r[1][2], 2.0, delta=1e-8)
        self.assertAlmostEqual(r[2][0], 2.333333333, delta=1e-8)
        self.assertAlmostEqual(r[2][1], 2.666666666, delta=1e-8)
        self.assertAlmostEqual(r[2][2], 3.0, delta=1e-8)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_div_divide_matriz_por_float(self):
        """
        Testa a divisão de um matriz por uma inteiro.
         Utiliza oito casas decimais e aceita uma diferença de 0.00000001
        """
        m1 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m1 / 3.3

        self.assertAlmostEqual(r[0][0], 0.30303030, delta=1e-8)
        self.assertAlmostEqual(r[0][1], 0.60606060, delta=1e-8)
        self.assertAlmostEqual(r[0][2], 0.90909090, delta=1e-8)
        self.assertAlmostEqual(r[1][0], 1.21212121, delta=1e-8)
        self.assertAlmostEqual(r[1][1], 1.51515151, delta=1e-8)
        self.assertAlmostEqual(r[1][2], 1.81818181, delta=1e-8)
        self.assertAlmostEqual(r[2][0], 2.12121212, delta=1e-8)
        self.assertAlmostEqual(r[2][1], 2.42424242, delta=1e-8)
        self.assertAlmostEqual(r[2][2], 2.72727272, delta=1e-8)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_div_divide_matriz_por_complex(self):
        """
        Testa a divisão de um matriz por um complexo.
         Utiliza oito casas decimais e aceita uma diferença de 0.00000001
        """
        m1 = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        r = m1 / (1 + 2j)

        self.assertAlmostEqual(r[0][0], 1 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[0][1], 2 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[0][2], 3 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[1][0], 4 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[1][1], 5 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[1][2], 6 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[2][0], 7 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[2][1], 8 / (1 + 2j), delta=1e-8)
        self.assertAlmostEqual(r[2][2], 9 / (1 + 2j), delta=1e-8)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    # ------------------------------------------------------------------------------------------------------------------
    # método concatena_horizontal
    # ------------------------------------------------------------------------------------------------------------------

    def test_inv_determina_matriz_inversa(self):
        """
        Calcula a matriz inversa, ao mutiplicar com a própria matriz deve resultar em uma identidade.
        """
        m = Matriz([[2, 2, 3], [4, 5, 6], [7, 8, 9]])
        inv = m.inv()

        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(inv, Matriz)

        r = m * inv

        self.assertAlmostEqual(r[0][0], 1, delta=1e-8)
        self.assertAlmostEqual(r[0][1], 0, delta=1e-8)
        self.assertAlmostEqual(r[0][2], 0, delta=1e-8)
        self.assertAlmostEqual(r[1][0], 0, delta=1e-8)
        self.assertAlmostEqual(r[1][1], 1, delta=1e-8)
        self.assertAlmostEqual(r[1][2], 0, delta=1e-8)
        self.assertAlmostEqual(r[2][0], 0, delta=1e-8)
        self.assertAlmostEqual(r[2][1], 0, delta=1e-8)
        self.assertAlmostEqual(r[2][2], 1, delta=1e-8)

    def test_inv_calculo_matriz_nao_invertivel(self):
        """
        Calcula a matriz inversa, ao mutiplicar com a própria matriz deve resultar em uma identidade.
        """
        m = Matriz([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        with self.assertRaises(numpy.linalg.LinAlgError):
            m.inv()
        
    # ------------------------------------------------------------------------------------------------------------------
    # método concatena_vertical
    # ------------------------------------------------------------------------------------------------------------------

    def test_concatena_vertical_concatena_matriz_verticalmente_um_elementos(self):
        """
        Testa método concatena passando um elemento
        """
        m1 = Matriz([[1, 2], [3, 4]])

        r = Matriz.concatena_vertical(m1)

        self.assertEqual(r.nr_linhas(), 2)
        self.assertEqual(r.nr_colunas(), 2)
        self.assertEqual(r[0][0], 1)
        self.assertEqual(r[0][1], 2)
        self.assertEqual(r[1][0], 3)
        self.assertEqual(r[1][1], 4)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_concatena_vertical_concatena_matriz_verticalmente_tres_elementos(self):
        """
        Testa método concatena passando tres elemento, verifica ordem de concatenação
        """
        m1 = Matriz([[1, 2], [3, 4]])
        m2 = Matriz([[5, 6], [7, 8]])
        m3 = Matriz([[9, 10], [11, 12]])

        r = Matriz.concatena_vertical(m1, m2, m3)

        self.assertEqual(r.nr_linhas(), 6)
        self.assertEqual(r.nr_colunas(), 2)
        self.assertEqual(r[0][0], 1)
        self.assertEqual(r[0][1], 2)
        self.assertEqual(r[1][0], 3)
        self.assertEqual(r[1][1], 4)
        self.assertEqual(r[2][0], 5)
        self.assertEqual(r[2][1], 6)
        self.assertEqual(r[3][0], 7)
        self.assertEqual(r[3][1], 8)
        self.assertEqual(r[4][0], 9)
        self.assertEqual(r[4][1], 10)
        self.assertEqual(r[5][0], 11)
        self.assertEqual(r[5][1], 12)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    # ------------------------------------------------------------------------------------------------------------------
    # método concatena_horizontal
    # ------------------------------------------------------------------------------------------------------------------
    def test_concatena_horizontal_concatena_matriz_horizontalmente_um_elementos(self):
        """
        Testa método concatena passando um elemento
        """
        m1 = Matriz([[1, 2], [3, 4]])

        r = Matriz.concatena_horizontal(m1)

        self.assertEqual(r.nr_linhas(), 2)
        self.assertEqual(r.nr_colunas(), 2)
        self.assertEqual(r[0][0], 1)
        self.assertEqual(r[0][1], 2)
        self.assertEqual(r[1][0], 3)
        self.assertEqual(r[1][1], 4)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

    def test_concatena_horizontal_concatena_matriz_horizontalmente_tres_elementos(self):
        """
        Testa método concatena passando tres elemento, verifica ordem de concatenação
        """
        m1 = Matriz([[1, 2], [3, 4]])
        m2 = Matriz([[5, 6], [7, 8]])
        m3 = Matriz([[9, 10], [11, 12]])

        r = Matriz.concatena_horizontal(m1, m2, m3)

        self.assertEqual(r.nr_linhas(), 2)
        self.assertEqual(r.nr_colunas(), 6)
        self.assertEqual(r[0][0], 1)
        self.assertEqual(r[0][1], 2)
        self.assertEqual(r[0][2], 5)
        self.assertEqual(r[0][3], 6)
        self.assertEqual(r[0][4], 9)
        self.assertEqual(r[0][5], 10)
        self.assertEqual(r[1][0], 3)
        self.assertEqual(r[1][1], 4)
        self.assertEqual(r[1][2], 7)
        self.assertEqual(r[1][3], 8)
        self.assertEqual(r[1][4], 11)
        self.assertEqual(r[1][5], 12)
        # verifica se o retorno é uma instancia de Matriz
        self.assertIsInstance(r, Matriz)

import numpy as np
from numpy.linalg import inv


class Matriz(object):
    def __init__(self, data):
        if isinstance(data, Matriz):
            self._matriz = data.matriz
        elif isinstance(data, np.ndarray):
            self._matriz = data

        elif isinstance(data, type(np.array)):
            self._matriz = data

        elif isinstance(data, list):
            self._matriz = np.array(data)

        if self._matriz.ndim != 2:
            raise ValueError("Matriz deve ter duas dimensões!")

    def nr_linhas(self):
        """Retorna o nr de linhas da matriz"""
        return len(self._matriz)

    def nr_colunas(self):
        """Retorna o nr de colunas da matriz"""
        return len(self._matriz[0])

    def inv(self):
        return Matriz(inv(self._matriz))

    @staticmethod
    def hstack(tup):
        if isinstance(tup, tuple):
            lista = []
            for i in range(0, len(tup)):
                lista.append(tup[i].matriz)
        elif isinstance(tup, list):
            lista = []
            for matriz in tup:
                lista.append(matriz.matriz)
        else:
            ValueError("Método deve receber uma tupla ou lista!")

        return Matriz(np.hstack(lista))

    @staticmethod
    def vstack(tup):
        if isinstance(tup, tuple):
            lista = []
            for i in range(0, len(tup)):
                lista.append(tup[i].matriz)
        elif isinstance(tup, list):
            lista = ()
            for matriz in tup:
                lista.append(matriz.matriz)
        else:
            ValueError("Método deve receber uma tupla ou lista!")
            raise
        return Matriz(np.vstack(lista))

    @property
    def matriz(self):
        return self._matriz

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Matriz(self._matriz * other)
        matriz2 = Matriz(other)

        # compara colunas da segunda matriz com as linhas da primeira, caso seja diferente lança uma AssertionError
        assert (matriz2.nr_colunas() == self.nr_linhas()), 'Número de linhas e colunas divergentes!'

        return Matriz(self._matriz @ matriz2.matriz)

    def __rmul__(self, other):
        if type(other) == int or type(other) == float:
            return Matriz(self._matriz * other)
        matriz2 = Matriz(other)

        # compara colunas da segunda matriz com as linhas da primeira, caso seja diferente lança uma AssertionError
        assert (matriz2.nr_colunas() == self.nr_linhas()), 'Número de linhas e colunas divergentes!'

        return Matriz(matriz2.matriz @ self._matriz)

    def __imul__(self, other):
        if type(other) == int or type(other) == float:
            return Matriz(self._matriz * other)

        matriz2 = Matriz(other)

        # compara colunas da segunda matriz com as linhas da primeira, caso seja diferente lança uma AssertionError
        assert (matriz2.nr_colunas() == self.nr_linhas()), 'Número de linhas e colunas divergentes!'

        return Matriz(self._matriz @ matriz2.matriz)

    def __truediv__(self, other):
        return Matriz(self._matriz / other)

    def __str__(self):
        return str(self._matriz)

    def __repr__(self):
        return 'Matriz \n %s' % self._matriz

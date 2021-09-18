import ast
import numpy


def _convert_from_string(data):
    for char in '[]':
        data = data.replace(char, '')

    rows = data.split(';')
    new_data = []
    count = 0
    for row in rows:
        trow = row.split(',')
        new_row = []
        for col in trow:
            temp = col.split()
            new_row.extend(map(ast.literal_eval, temp))
        if count == 0:
            n_cols = len(new_row)
        elif len(new_row) != n_cols:
            raise ValueError("Colunas não são do mesmo tamanho.")
        count += 1
        new_data.append(new_row)
    return new_data


class Matriz(numpy.ndarray):
    def __new__(cls, data, dtype=None, copy=True):
        if isinstance(data, Matriz):
            dtype2 = data.dtype
            if dtype is None:
                dtype = dtype2
            if dtype2 == dtype and not copy:
                return data
            return data.astype(dtype)

        elif isinstance(data, numpy.ndarray):
            if dtype is None:
                intype = data.dtype
            else:
                intype = numpy.dtype(dtype)
            new = data.view(cls)
            if intype != data.dtype:
                return new.astype(intype)
            if copy:
                return new.copy()
            else:
                return new

        elif isinstance(data, str):
            data = _convert_from_string(data)

        elif isinstance(data, list):
            matriz = numpy.array(data, dtype=dtype, copy=copy)

        # now convert data to an array
        arr = numpy.array(data, dtype=dtype, copy=copy)
        n_dim = arr.ndim
        shape = arr.shape
        if n_dim > 2:
            raise ValueError("Matriz pode ter até duas dimensões")

        order = 'C'
        if arr.flags.fortran:
            order = 'F'

        if not (order or arr.flags.contiguous):
            arr = arr.copy()

        ret = numpy.ndarray.__new__(cls, shape, arr.dtype,
                                    buffer=arr,
                                    order=order)
        return ret

    def nr_linhas(self):
        """Retorna o nr de linhas da matriz"""
        return len(self)

    def nr_colunas(self):
        """Retorna o nr de colunas da matriz"""
        return len(self[0])

    def inv(self):
        try:
            return Matriz(numpy.linalg.inv(self))
        except numpy.linalg.LinAlgError:
            raise numpy.linalg.LinAlgError('Matriz não possui inversa')

    def to_array(self):
        return self.__array__()

    def __mul__(self, other):
        if type(other) == int or type(other) == float or type(other) == complex:
            return Matriz(numpy.array(self) * other)
        matriz2 = Matriz(other)

        # compara colunas da segunda matriz com as linhas da primeira, caso seja diferente lança uma AssertionError
        assert (self.nr_colunas() == matriz2.nr_linhas()), 'Número de linhas e colunas divergentes! operação :'

        return Matriz(self @ matriz2)

# ----------------------------------------------------------------------------------------------------------------------
# Métodos estáticos
# ----------------------------------------------------------------------------------------------------------------------

        nova_m = matriz
        for x in range(0, len(matriz[0])):
            for y in range(0, len(x)):
                if matriz[x][y] < 1E-9:
                    nova_m[x][y] = 0
        return nova_m

    @staticmethod
    def concatena_horizontal(*args):
        if isinstance(args[0], Matriz):
            array = []
            for matriz in args:
                array.append(matriz.__array__())

            return Matriz(numpy.hstack(array))
        return Matriz(numpy.hstack(args))

    @staticmethod
    def concatena_vertical(*args):
        if isinstance(args[0], Matriz):
            array = []
            for matriz in args:
                array.append(matriz.__array__())

            return Matriz(numpy.vstack(array))
        return Matriz(numpy.vstack(args))

from src.tcc.modelos.elemento import Elemento


class Transformador(Elemento):
    def __init__(self, z_1, z_0, y_1, y_0):
        self.z_1 = z_1
        self.z_0 = z_0
        self.y_1 = y_1
        self.y_0 = y_0

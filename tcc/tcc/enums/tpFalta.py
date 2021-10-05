from enum import Enum, unique


# tipo de falta (1-mono(default), 2-bi, 3-biterra, 4-tri, 5-triterra)
@unique
class TpFalta(Enum):
    MONO = 1
    BI = 2
    BI_TERRA = 3
    TRI = 4
    TRI_TERRA = 5

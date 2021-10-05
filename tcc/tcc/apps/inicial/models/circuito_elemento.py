from django.db import models

from tcc.apps.inicial.models.circuito import Circuito
from tcc.apps.inicial.models.elemento import Elemento


class Circuito_elemento(models.Model):
    id_circuito = models.ForeignKey(Circuito, on_delete=models.PROTECT)
    id_elemento = models.ForeignKey(Elemento, on_delete=models.PROTECT)

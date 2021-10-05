from _ast import mod

from django.db import models


class Elemento(models.Model):
    ELEM_TIPO = (
        ('T', 'Transformador'),
        ('L', 'Linha'),
        ('F', 'Fonte'),
        ('B', 'Barra'),
    )
    nome = models.CharField(max_length=30, blank=False, null=False)
    tensao_mag = models.IntegerField()
    tensao_ang = models.IntegerField()
    corrente_mag = models.IntegerField()
    corrente_ang = models.IntegerField()
    imp_0_real = models.IntegerField()
    imp_0_imag = models.IntegerField()
    imp_1_real = models.IntegerField()
    imp_1_imag = models.IntegerField()
    tp_elemento = models.CharField(max_length=1, choices=ELEM_TIPO)
    dt_cadastro = models.DateTimeField(blank=False, null=False)
    dt_atualizacao = models.DateTimeField(blank=False, null=False)

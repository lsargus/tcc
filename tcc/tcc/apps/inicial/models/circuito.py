from django.db import models
from django.contrib.auth.models import User


class Circuito(models.Model):
    id_usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    qnt_elementos = models.IntegerField()
    dt_cadastro = models.DateTimeField(blank=False, null=False)
    dt_atualizacao = models.DateTimeField(blank=False, null=False)
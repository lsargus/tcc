from django.db import models
from datetime import datetime

class Teste(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField(max_length=255)
    sequencia = models.IntegerField()
    data = models.DateTimeField(default=datetime.now, blank=True)

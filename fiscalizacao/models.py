from django.db import models
from django.forms import CharField

class Estado(models.Model):

    nome = models.CharField(unique=True, max_length=60)
    uf = models.CharField(unique=True, max_length=2)
    
    class Meta:
        ordering = ['nome']

    def __str__(self):
        return '%s' % (self.nome)

class Cidade(models.Model):
    
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    nome = models.CharField(max_length=60)
    
    class Meta:
        ordering = ['nome']
        unique_together = ('estado', 'nome')

    def __str__(self):
        return '%s - %s' % (self.estado, self.nome)

class Obra(models.Model):

    TIPO_CHOICES=[
        ('a', 'Tipo A'),
        ('b', 'Tipo B'),
    ]

    nome=models.CharField(max_length=300, verbose_name='Nome')
    cno=models.CharField(max_length=200)
    tipo=models.CharField(max_length=1, choices=TIPO_CHOICES)
    logradouro=models.CharField(max_length=200)
    n=models.CharField(max_length=200, verbose_name='Número')
    complemento=models.CharField(max_length=200)
    bairro=models.CharField(max_length=200)
    cep=models.CharField(max_length=200, verbose_name='CEP')
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, verbose_name='Município')
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')
    
    def __str__(self):
        return '%s - %s' % (self.id, self.cno)
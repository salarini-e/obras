from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User
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

# class Obra(models.Model):

#     TIPO_CHOICES=[
#         ('a', 'Tipo A'),
#         ('b', 'Tipo B'),
#     ]

#     nome=models.CharField(max_length=300, verbose_name='Nome')
#     cno=models.CharField(max_length=200)
#     tipo=models.CharField(max_length=1, choices=TIPO_CHOICES)
#     logradouro=models.CharField(max_length=200)
#     n=models.CharField(max_length=200, verbose_name='Número')
#     complemento=models.CharField(max_length=200)
#     bairro=models.CharField(max_length=200)
#     cep=models.CharField(max_length=200, verbose_name='CEP')
#     cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, verbose_name='Município')
#     dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão')
    
#     def __str__(self):
#         return '%s - %s' % (self.id, self.cno)

class Status(models.Model):
    nome=models.CharField(max_length=50)
    
    def __str__(self):
        return '%s' % (self.nome)

class Nota_Fiscal(models.Model):
    
    PERIODO_CHOICES=[
        ('a', 'Ano'),
        ('m', 'Mês'),
        ('s', 'Semana'),        
        ('d', 'Dia'),        
    ]
    
    n_nota=models.IntegerField(verbose_name='N. da nota')
    data=models.DateField(verbose_name='Data de expedição')
    valor=models.CharField(max_length=20,verbose_name='Valor da nota (R$)')
    tipo_periodo=models.CharField(max_length=1, choices=PERIODO_CHOICES, default='a', verbose_name='Tipo de Período')
    periodo=models.CharField( max_length=5,verbose_name='Período')
    url=models.CharField(max_length=300, default='#', verbose_name='Link da nota')
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 


    def __str__(self):
        return '%s' % (self.n_nota)

class Empresa(models.Model):
    nome=models.CharField(max_length=150, verbose_name='Nome da empresa')
    cnpj=models.CharField(max_length=14, verbose_name='CNPJ')
    cadastrado_por=models.ForeignKey(User, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 

    def __str__(self):
        return '%s' % (self.nome)

class Fiscal(models.Model):
    nome=models.CharField(max_length=150, verbose_name='Nome do Fiscal')
    crea=models.CharField(max_length=150, verbose_name='CREA')
    matricula=models.CharField(max_length=150, verbose_name='Matrícula')
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 

    def __str__(self):
        return '%s' % (self.nome)

class Obra(models.Model):        

    objeto_da_obra=models.CharField(max_length=150, verbose_name='Objeto da obra')
    populacao_atendida=models.CharField(max_length=150, verbose_name='População atendida')
    valor_previsto=models.CharField(max_length=20, verbose_name='Valor previsto (R$)')
    status=models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Situação')    
    fiscal=models.ManyToManyField(Fiscal, through='Obra_Fiscal')
    justificativa=models.TextField(verbose_name='Justificativa')
    cadastrado_por=models.ForeignKey(User, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 
    #latitude e longitude
    
    def __str__(self):
        return '%s %s' % (self.id, self.objeto_da_obra)

class Contrato(models.Model): 
    obra=models.ForeignKey(Obra, on_delete=models.CASCADE)   
    empresa=models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa contratada')
    nota_fiscal=models.ForeignKey(Nota_Fiscal, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 

    def __str__(self):
        return '%s - %s' % (self.id, self.nota_fiscal)

class Aditivos(models.Model):
    contrato=models.ForeignKey(Contrato, on_delete=models.CASCADE)
    nota_fiscal=models.ForeignKey(Nota_Fiscal, on_delete=models.PROTECT)    
    
class Obra_Fiscal(models.Model):
    STATUS_CHOICES=[
        ('r', 'Responsável'),
        ('s', 'Suplente'),
        ('f', 'Férias'),
    ]
    obra=models.ForeignKey(Obra, on_delete=models.CASCADE)
    fiscal=models.ForeignKey(Fiscal, on_delete=models.CASCADE)
    status=models.CharField(max_length=1, choices=STATUS_CHOICES)

class Fotos(models.Model):   
    obra=models.ForeignKey(Obra, on_delete=models.CASCADE) 
    url=models.CharField(max_length=300)

    def __str__(self):
        return '%s' % (self.url)

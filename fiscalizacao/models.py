from pyexpat import model
from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    nome=models.CharField(max_length=50)
    
    def __str__(self):
        return '%s' % (self.nome)

class Nota_Empenho(models.Model):
    
    # PERIODO_CHOICES=[
    #     ('a', 'Ano'),
    #     ('m', 'Mês'),
    #     ('s', 'Semana'),        
    #     ('d', 'Dia'),        
    # ]
    TIPO_CHOICES=[
        ('in', 'Inicial'),
        ('sd', 'Substituido'),
        ('st', 'Substituto'),        
        ('co', 'Complementar'),        
    ]

    tipo_empenho=models.CharField(max_length=2, choices=TIPO_CHOICES, default='in', verbose_name='Tipo de empenho')    
    substituto=models.IntegerField(verbose_name='Substituto', blank=True, default=0)
    substituindo=models.IntegerField(verbose_name='Substituindo', blank=True, default=0)
    n_nota=models.IntegerField(verbose_name='N. da nota de empenho', unique=True)
    data=models.DateField(verbose_name='Data de expedição do empenho')
    valor=models.CharField(max_length=20,verbose_name='Valor do empenho(R$)')
    # tipo_periodo=models.CharField(max_length=1, choices=PERIODO_CHOICES, default='a', verbose_name='Tipo de período do empenho')
    # periodo=models.CharField( max_length=5,verbose_name='Período do empenho')
    url=models.CharField(max_length=300, default='#', verbose_name='Link da nota do empenho')
    ativo=models.BooleanField(default=False)
    abatido=models.BooleanField(default=False)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 


    def __str__(self):
        return '%s' % (self.n_nota)

class Nota_Fiscal(models.Model):
    
    # PERIODO_CHOICES=[
    #     ('a', 'Ano'),
    #     ('m', 'Mês'),
    #     ('s', 'Semana'),        
    #     ('d', 'Dia'),        
    # ]
    
    empenho=models.ForeignKey(Nota_Empenho, on_delete=models.CASCADE)
    n_nota=models.CharField(max_length=100 ,verbose_name='N. da nota fiscal')
    data=models.DateField(verbose_name='Data de expedição fiscal')
    valor=models.CharField(max_length=20,verbose_name='Valor da nota (R$)')
    # tipo_periodo=models.CharField(max_length=1, choices=PERIODO_CHOICES, default='a', verbose_name='Tipo de Período')
    periodo_inicial=models.DateField(verbose_name='Período inicial da medição')
    periodo_final=models.DateField(verbose_name='Período final da medição')
    url=models.CharField(max_length=300, default='#', verbose_name='Link da nota')
    ativo=models.BooleanField(default=False, null=True)
    obs=models.TextField(verbose_name='Observações')
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 


    def __str__(self):
        return '%s - %s' % (self.id, self.n_nota)

class Nota_Fiscal_Arquivada(models.Model):    
    nota=models.ForeignKey(Nota_Fiscal, on_delete=models.CASCADE)
    dt_arquivado=models.DateTimeField(auto_now_add=True, verbose_name='Arquivado em') 
    
class Empresa(models.Model):
    nome=models.CharField(max_length=150, verbose_name='Nome da empresa')
    cnpj=models.CharField(max_length=14, verbose_name='CNPJ', unique=True)
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

    n_processo_adm=models.CharField(max_length=50, default='', blank=True, verbose_name='Número do Processo Administrativo') 
    objeto_da_obra=models.CharField(max_length=150, verbose_name='Objeto da obra')
    populacao_atendida=models.CharField(max_length=150, verbose_name='População atendida')
    valor_previsto=models.CharField(max_length=20, verbose_name='Valor previsto do contrato (R$)')
    n_processo_pagamento=models.CharField(max_length=50, default='', blank=True, verbose_name='Número do Processo de Pagamento') 
    status=models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Situação')    
    fiscal=models.ForeignKey(Fiscal,on_delete=models.PROTECT, verbose_name='Fiscal responsável')
    fiscal_substituto=models.ForeignKey(Fiscal,on_delete=models.PROTECT, verbose_name='Fiscal substituto', related_name='substituto')
    engenheiro=models.CharField(max_length=250, verbose_name='Nome do engenheiro responsável', default='')
    justificativa=models.TextField(verbose_name='Justificativa')
    data_conclusao=models.DateField(verbose_name='Data prevista de conclusão', blank=True, null=True)
    cadastrado_por=models.ForeignKey(User, on_delete=models.PROTECT)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 
    #latitude e longitude
    
    def __str__(self):
        return '%s %s' % (self.id, self.objeto_da_obra)

class Contrato(models.Model): 

    obra=models.ForeignKey(Obra, on_delete=models.CASCADE)   
    empresa=models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa contratada')
    nota_empenho=models.ManyToManyField(Nota_Empenho, blank=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 

    def __str__(self):
        return '%s - %s' % (self.id, self.nota_empenho)

# class Aditivos(models.Model):

#     contrato=models.ForeignKey(Contrato, on_delete=models.CASCADE)
#     nota_fiscal=models.ForeignKey(Nota_Fiscal, on_delete=models.PROTECT)    
    
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

class Aditivo(models.Model):
    prazo=models.BooleanField()
    valor=models.BooleanField()
    id_empenho=models.CharField(max_length=50)

class Log(models.Model):

    TABELAS=[                
        ('stu', 'Status de Obra'),
        ('nte', 'Nota de Empenho'),
        ('emp', 'Empresa'),
        ('ntf', 'Nota Fiscal'),
        ('fis', 'Fiscal'),        
        ('obr', 'Obra'),
        ('con', 'Contrato'),
        ('adi', 'Aditivos'),
    ]    
    TIPOS=[
        ('c', 'Criado'),        
        ('u', 'Atualizado'),
        ('a', 'Arquivado'),
        ('d', 'Deletado'),

    ]
    tabela=models.CharField(max_length=3, blank=False, choices=TABELAS)
    ref=models.IntegerField(blank=True, default=0)
    tipo=models.CharField(max_length=1, blank=False, choices=TIPOS)
    acao=models.CharField(max_length=300, blank=False)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Dt. Inclusão') 
    user=models.CharField(max_length=150)
    ipv4=models.CharField(max_length=15, verbose_name='IP')    
    # ipv6=CharField(max_length=16)    
    def __str__(self):
        return '%s - %s - %s' % (self.tabela, self.acao, self.user)
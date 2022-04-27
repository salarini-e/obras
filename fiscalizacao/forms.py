from .models import Contrato, Empresa, Estado, Nota_Fiscal, Obra

from django import forms
from django.forms import ModelForm, ValidationError


class Form_Obras(ModelForm): 
    class Meta:
        model = Obra
        widgets = {'cadastrado_por': forms.HiddenInput()}
        exclude = ['dt_inclusao']

class Form_Empresa(ModelForm): 
    class Meta:
        model = Empresa
        widgets = {'cadastrado_por': forms.HiddenInput()}
        exclude = ['dt_inclusao']

class Form_Nota(ModelForm): 
    class Meta:
        model = Nota_Fiscal
        exclude = ['dt_inclusao']

class Form_Nota(ModelForm): 
    class Meta:
        model = Nota_Fiscal
        exclude = ['dt_inclusao']

class Form_Contrato(ModelForm): 
    class Meta:
        model = Contrato
        exclude = ['dt_inclusao']
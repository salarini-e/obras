from .models import Contrato, Empresa, Estado, Fiscal, Nota_Fiscal, Obra
from .validations import validate_CNPJ

from django import forms
from django.forms import ModelForm, ValidationError

class Form_Obras(ModelForm): 
    class Meta:
        model = Obra
        widgets = {'cadastrado_por': forms.HiddenInput(),                   
                   'valor_previsto': forms.TextInput(attrs={'onkeydown':"maskValor(this)"})}
        exclude = ['dt_inclusao']

class Form_Fiscal(ModelForm): 
    
    class Meta:
        model = Fiscal
        widgets = {'cadastrado_por': forms.HiddenInput()}
        exclude = ['dt_inclusao']

class Form_Empresa(ModelForm): 
    cnpj=forms.CharField(label="CNPJ", max_length=18, required=True,  widget = forms.TextInput(attrs={'onkeydown':"mascara(this,icnpj)"}))
    class Meta:
        model = Empresa
        widgets = {'cadastrado_por': forms.HiddenInput()}
        exclude = ['dt_inclusao']

    def clean_cnpj(self):
        cnpj = validate_CNPJ(self.cleaned_data["cnpj"])
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace('-', '')
        return cnpj

class Form_Nota(ModelForm): 
    class Meta:
        model = Nota_Fiscal
        widgets = {'valor': forms.TextInput(attrs={'onkeydown':"maskValor(this)"})}
        exclude = ['dt_inclusao']


class Form_Contrato(ModelForm): 
    class Meta:
        model = Contrato        
        exclude = ['dt_inclusao']
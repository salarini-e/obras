from .models import Contrato, Empresa, Fiscal, Nota_Empenho, Nota_Fiscal, Obra
from .validations import validate_CNPJ

from django import forms
from django.forms import ModelForm, ValidationError

class Form_Obras(ModelForm): 

    class Meta:
        model = Obra
        widgets = {'cadastrado_por': forms.HiddenInput(),                   
                   'valor_previsto': forms.TextInput(attrs={'onkeydown':"maskValor(this)"}),
                   'status': forms.Select(attrs={'class':'form-select mb-3'}),
                   'fiscal': forms.Select(attrs={'class':'form-select mb-3'}),
                   'fiscal_substituto': forms.Select(attrs={'class':'form-select mb-3'}),}
        exclude = ['dt_inclusao']
    
    def clean_valor_previsto(self):                        
        valor=self.cleaned_data["valor_previsto"]
        valor = valor.replace('.', '')
        valor = valor.replace(',', '')        
        return valor

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


class Form_Empenho(ModelForm):     
    class Meta:
        model = Nota_Empenho
        widgets = {'valor': forms.TextInput(attrs={'onkeydown':"maskValor(this)"}),
                   'tipo_periodo': forms.Select(attrs={'class':'form-select mb-3'}),
                   'tipo_empenho': forms.HiddenInput(),
                   'substituindo': forms.HiddenInput()
                   }
        exclude = ['ativo', 'dt_inclusao', 'abatido', 'substituto']        

    def clean_valor(self):                        
        valor=self.cleaned_data["valor"]
        valor = valor.replace('.', '')
        valor = valor.replace(',', '')        
        return valor

class Form_Empenho_Desabilitado(ModelForm): 

    class Meta:
        model = Nota_Empenho
        widgets = {'n_nota': forms.TextInput(attrs={'disabled':'true'}),
                    'data': forms.DateInput(attrs={'disabled':'true'}),
                   'valor': forms.TextInput(attrs={'onkeydown':"maskValor(this)", 'disabled':'true'}),
                   'tipo_periodo': forms.Select(attrs={'class':'form-select mb-3', 'disabled':'true'}),
                   'periodo': forms.TextInput(attrs={'disabled':'true'}),
                   'url': forms.TextInput(attrs={'disabled':'true'}),}        
        exclude = ['ativo', 'dt_inclusao', 'tipo_empenho', 'abatido', 'substituto', 'substituindo']

    def clean_valor(self):                        
        valor=self.cleaned_data["valor"]
        valor = valor.replace('.', '')
        valor = valor.replace(',', '')        
        return valor

class Form_Nota(ModelForm): 

    class Meta:
        model = Nota_Fiscal
        widgets = {'valor': forms.TextInput(attrs={'onkeydown':"maskValor(this)"}),
                   'tipo_periodo': forms.Select(attrs={'class':'form-select mb-3'}),}        
        exclude = ['dt_inclusao', 'ativo']

    def clean_valor(self):                        
        valor=self.cleaned_data["valor"]
        valor = valor.replace('.', '')
        valor = valor.replace(',', '')        
        return valor


class Form_Contrato(ModelForm): 

    class Meta:
        model = Contrato        
        exclude = ['dt_inclusao']
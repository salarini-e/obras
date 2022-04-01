from .models import Estado, Obra

from django import forms
from django.forms import ModelForm, ValidationError


class FormObras(ModelForm): 
    class Meta:
        model = Obra
        exclude = ['dt_inclusao']
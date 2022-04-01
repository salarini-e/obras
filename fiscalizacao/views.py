from django.shortcuts import render

from .forms import FormObras
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def cadastrar_obra(request):
    
    if request.method=='POST':        
        form=FormObras(request.POST)
        if form.is_valid():
            form.save()
            context={
                'form': FormObras(),
                'success': [True, 'Vaga cadastrada com sucesso!']
            }
            return render(request, 'fiscalizacao/cadastrar_obra.html', context)

    else:
        form=FormObras()    

    context={
        'form': form,
    }
    return render(request, 'fiscalizacao/cadastrar_obra.html', context)

def fiscalizar_obra(request):
    obra=Obra.objects.get(id=1)
    form=FormObras(instance=obra)
    context={
        'form': form,
    }
    return render(request, 'fiscalizacao/fiscalizar_obra.html', context)

def gerar_qr_code(request):
    conteudo = 'ID: 156832 Url: https://github.com/smctinf/turismo/blob/dev/equipamentos/urls.py'

    context={
        'conteudo': conteudo,
    }

    return render(request, 'fiscalizacao/gerar_qr_code.html', context)    
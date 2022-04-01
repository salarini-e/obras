from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import FormObras
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
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

@login_required
def fiscalizar_obra(request, obra_id):
    try:
        form=Obra.objects.get(id=obra_id)        
        success=True
    except:
        success=False
        form=FormObras()
    context={
        'form': form,
        'success':success
    }
    return render(request, 'fiscalizacao/fiscalizar_obra.html', context)

@login_required
def gerar_qr_code(request, obra_id):
    conteudo = 'ID: '+obra_id

    context={
        'conteudo': conteudo,
    }

    return render(request, 'fiscalizacao/gerar_qr_code.html', context)    


def login_view(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                return redirect(request.GET['next'])    
            except:
                return redirect('obra:index')
        else:                
            context={
                'error': True,
            }
            return render(request, 'registration/login.html', context)        
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('obra:index')
    else:
        return redirect('/login')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import Form_Contrato, Form_Nota, Form_Obras, Form_Empresa
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def cadastrar_empresa(request): 
    if request.method=='POST':  
        form=Form_Empresa(request.POST)   
        print(form)           
        if form.is_valid():
            form.save()            
            context={
                'form': Form_Empresa(initial={'cadastrado_por':request.user}),
                'success': 'Empresa cadastrada com sucesso!'
            }
            return render(request, 'fiscalizacao/cadastrar_empresa.html', context) 
    else:
        form=Form_Empresa(initial={'cadastrado_por':request.user})
    print(form)           
    context={
            'form': form,
    }
    return render(request, 'fiscalizacao/cadastrar_empresa.html', context)

@login_required
def teste(request):
    form=Form_Contrato()      
    context={
        'form': form,
    }
    return render(request, 'fiscalizacao/teste.html', context)

def get_empresa(request):
    try:
        # empresas=Empresa.objects.filter(nome__startswith=request.GET.get('nome')).order_by('nome')
        empresas=Empresa.objects.filter(nome__icontains=request.GET.get('nome')).order_by('nome')
    except Exception as E:
        print(E)
        empresas=[]
    context={
        'empresas': empresas,
    }
    return render(request, 'fiscalizacao/get_empresa.html', context)


@login_required
def cadastrar_obra(request):    
    if request.method=='POST':          
        form_nota=Form_Nota(request.POST)
        form_obra=Form_Obras(request.POST)
        try:
            empresa=Empresa.objects.get(nome=request.POST['empresa'])    
            go=True
        except:
            print(request.POST['empresa'])
            go=False
        if go:
            if form_obra.is_valid() and form_nota.is_valid():            

                try:
                    obra=form_obra.save()
                    nota=form_nota.save()
                    contrato=Contrato(obra=obra, empresa=empresa, nota_fiscal=nota)
                    contrato.save()
                except Exception as E:
                    print(E)
                context={
                    'form_nota': Form_Nota(),
                    'form_obra': Form_Obras(),
                    'success': 'Obracadastrada com sucesso!'
                }
                return render(request, 'fiscalizacao/cadastrar_obra.html', context)

    else:
        form_nota=Form_Nota()
        form_obra=Form_Obras(initial={'cadastrado_por':request.user})    

    context={
        'form_nota': form_nota,
        'form_obra': form_obra,
    }
    return render(request, 'fiscalizacao/cadastrar_obra.html', context)

@login_required
def fiscalizar_obra(request, valor_busca='buscar'):
    if valor_busca=='buscar':
        buscar=True
        contrato=Form_Obras()
        success=False
        contratos=Contrato.objects.all()
    else:
        buscar=False
        contratos=[]
        try:
            try:
                contrato=Contrato.objects.get(id=valor_busca)        
                success=True
            except:
            
                contratos=Contrato.objects.filter(empresa=Empresa.objects.get(nome=valor_busca))        
                success=False
                buscar=True
                contrato=Form_Contrato()
                if len(contratos)==1:
                    success=True                        
                    buscar=False
                    contrato=Contrato.objects.get(empresa=Empresa.objects.get(nome=valor_busca))
                elif len(contratos)==0:
                    success=False
                    buscar=False
                    contrato=Form_Contrato()                                    
        except:
            success=False
            contrato=Form_Contrato()
    context={
        'form': contrato,
        'success':success,
        'buscar': buscar,
        'obra': contratos
    }
    return render(request, 'fiscalizacao/fiscalizar_obra.html', context)

@login_required
def gerar_qr_code(request, obra_id):
    contrato=Contrato.objects.get(id=obra_id)
    fiscais=''
    if len(contrato.obra.fiscal.all())==1:        
        for fiscal in contrato.obra.fiscal.all():
            fiscais=fiscal
    else:
        for fiscal in contrato.obra.fiscal.all():
            fiscais+=fiscal+', '

    conteudo = f'''Identificação da obra: {obra_id}
Objeto da obra: {contrato.obra.objeto_da_obra}
Justificativa: {contrato.obra.justificativa}
População atendida: {contrato.obra.populacao_atendida}
Valor previsto: {contrato.obra.valor_previsto}
Data da ordem de serviço: ????
Data da conclusão da obra: ????
Empresa(s): {contrato.empresa.nome} (?)
Aditivos: ????
Fotos: link
Cronograma da obra: link
Nome do agente público responsável pela fiscalização: {fiscal}
'''
    print(contrato.obra.fiscal.all)
    try:
        back_to=request.GET.get('back')
    except:
        back_to='/ver-obra/buscar'
    context={
        'conteudo': conteudo,
        'back_to': back_to
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
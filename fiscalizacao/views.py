from textwrap import indent
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import Form_Contrato, Form_Fiscal, Form_Nota, Form_Empenho, Form_Obras, Form_Empresa
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from settings.settings import BASE_DIR
import os

from .functions import get_client_ip
# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def cadastrar_empresa(request): 
    if request.method=='POST':  
        form=Form_Empresa(request.POST)   
        # print(form)           
        if form.is_valid():
            empresa=form.save()             
            acao={''}
            log=Log(
                    tabela='Empresa',
                    ref=empresa.id,
                    tipo='c', 
                    acao=acao,
                    user=request.user, 
                    ipv4=get_client_ip(request)
                )
            log.save()
            print(empresa.id)
            context={
                'form': Form_Empresa(initial={'cadastrado_por':request.user}),
                'success': 'Empresa cadastrada com sucesso!'
            }
            return render(request, 'fiscalizacao/cadastrar_empresa.html', context) 
    else:
        form=Form_Empresa(initial={'cadastrado_por':request.user})
    # print(form)           
    context={
            'form': form,
    }
    return render(request, 'fiscalizacao/cadastrar_empresa.html', context)

@login_required
def historico_empresa(request): 
    context={
        'logs': Log.objects.filter(tabela='emp')
    }
    return render(request, 'fiscalizacao/historico_empresa.html', context)

def historico_empresa_acoes(request, id): 
    log=Log.objects.get(id=id)
    import json
    json_=json.loads(str(log.acao.replace("'",'"')))
    #aqui
    context={
        'log': log,
        'acoes': json_.items()
    }
    return render(request, 'fiscalizacao/historico_empresa_acoes.html', context)

@login_required
def visualizar_empresa(request, id): 
    context={
        'empresa': Empresa.objects.get(id=id)
    }
    return render(request, 'fiscalizacao/listar_itens_empresa.html', context)

@login_required
def editar_empresa(request, id): 
    empresa=Empresa.objects.get(id=id)
    form=Form_Empresa(instance=empresa)
    if request.method=='POST':  
        form_=Form_Empresa(request.POST, instance=empresa)           
        if form_.is_valid():
            acoes={}
            for i in form_:      
                if i.name!='cadastrado_por':    
                    if form[i.name].value()!=form_.cleaned_data[i.name]:
                        # print(i.name)                    
                        acoes[i.name]={
                            'antes': form[i.name].value(),
                            'depois': form_.cleaned_data[i.name]
                        }
                else:
                    if form[i.name].value()!=form_.cleaned_data[i.name].id:
                        acoes[i.name]={
                            'antes': form[i.name].value(),
                            'depois': form_.cleaned_data[i.name].id
                        }
            # print(acoes)              
            empresa=form_.save()                         
            log=Log(
                    tabela='Empresa',
                    ref=empresa.id,
                    tipo='u', 
                    acao=acoes,
                    user=request.user, 
                    ipv4=get_client_ip(request)
                )
            log.save()            
            context={
                'form': form_,
                'success': 'Cadastrada da empresa atualizado com sucesso!'
            }
            return render(request, 'fiscalizacao/cadastrar_empresa.html', context) 
        else:
            form=form_      
    
    context={
            'form': form,
    }
    return render(request, 'fiscalizacao/cadastrar_empresa.html', context)

@login_required
def cadastrar_fiscal(request): 
    if request.method=='POST':  
        form=Form_Fiscal(request.POST)   
        print(form)           
        if form.is_valid():
            form.save()            
            context={
                'form': Form_Fiscal(initial={'cadastrado_por':request.user}),
                'success': 'Fiscal cadastrado com sucesso!'
            }
            return render(request, 'fiscalizacao/cadastrar_fiscais.html', context) 
    else:
        form=Form_Fiscal(initial={'cadastrado_por':request.user})
    print(form)           
    context={
            'form': form,
    }
    return render(request, 'fiscalizacao/cadastrar_fiscais.html', context)

@login_required
def listar_empresa(request):
    context={
        'empresas': Empresa.objects.all()
    }
    return render(request, 'fiscalizacao/listar_empresa.html', context)

@login_required
def listar_fiscais(request):
    context={
        'fiscais': Fiscal.objects.all()
    }
    return render(request, 'fiscalizacao/listar_fiscais.html', context)

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
        form_nota=Form_Empenho(request.POST)
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
                    os.mkdir(str(BASE_DIR)+'/settings/static/fotos/'+str(contrato.id))
                    error=False
                except Exception as E:
                    error=str(E)
                    print(E)
                context={      
                    'error': error,               
                    'form_nota': Form_Empenho(),
                    'form_obra': Form_Obras(),
                    'success': 'Obracadastrada com sucesso!'
                }
                return render(request, 'fiscalizacao/cadastrar_obra.html', context)
        else:
            error='ERROR'

    else:
        error=False
        form_nota=Form_Empenho()
        form_obra=Form_Obras(initial={'cadastrado_por':request.user})    

    context={
        'error': error,
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
            
                contratos=Contrato.objects.filter(empresa=Empresa.objects.get(nome__icontains=valor_busca))        
                success=False
                buscar=True
                contrato=Form_Contrato()                
                if len(contratos)==1:
                    success=True                        
                    buscar=False
                    contrato=Contrato.objects.get(empresa=Empresa.objects.get(nome__icontains=valor_busca))
                elif len(contratos)==0:
                    success=False
                    buscar=False
                    contrato=Form_Contrato()                                    
        except:
            try:
                fiscais=Fiscal.objects.filter(nome__icontains=valor_busca)                
                obras=[]   
                obra_fiscal=[]             
                for fiscal in fiscais:                    
                    obra_fiscal.append(Obra_Fiscal.objects.filter(fiscal=fiscal))        
                if len(obra_fiscal)==1:
                    try:
                        obras.append(obra_fiscal[0].obra)
                    except:
                        obras.append(obra_fiscal[0])
                else:
                    for i in obra_fiscal:
                        if len(i)>1:                            
                            for o in i:
                                print('a', o)
                                try:
                                    obras.append(o.obra)
                                except:
                                    obras.append(o)
                        else:
                            
                            try:
                                obras.append(i[0].obra)
                            except:
                                obras.append(i[0])
                contrato=Form_Contrato()                
                
                for obra in obras:                    
                    try:
                        contratos.append(Contrato.objects.filter(obra=obra.id))                
                    except:                        
                        for o in obra:
                            contratos.append(Contrato.objects.filter(obra=o.obra.id))   
                             
                if len(contratos)==1:
                    success=True                        
                    buscar=False                    
                elif len(contratos)==0:
                    success=False
                    buscar=False
                    contrato=Form_Contrato()
                success=False
                buscar=True
                contratos_=[]
                for contrato in contratos:
                    contratos_.append(contrato[0])
                contratos=contratos_
            except Exception as E:
                print('ops', E)
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
def get_obras(request):
    from django.db.models import Q

    valor=request.GET.get('nome')

    if valor!='':
        complexQuery = Q(empresa__nome__icontains=valor) | Q(id__icontains=valor) | Q(obra__objeto_da_obra__icontains=valor)
        obras=Contrato.objects.filter(complexQuery)
        context={           
            'obras': obras
        }
        if len(obras)==0:
            context={
                'alert': True,
                'obras': Contrato.objects.all()
            }
    else:            
        context={
            'alert': False,
            'obras': Contrato.objects.all()
        }
    return render(request, 'fiscalizacao/get_obras.html', context)

@login_required
def listar_obras(request, valor_busca):
    obras=Contrato.objects.all()
    context={
        'obras': obras
    }
    return render(request, 'fiscalizacao/listar_obras.html', context)

@login_required
def visualizar_obra(request, id):
    obra=Contrato.objects.get(id=id)
    context={
        'obra': obra
    }
    return render(request, 'fiscalizacao/listar_itens_obra.html', context)

@login_required
def visualizar_fotos_obra(request, id):
    obra=Contrato.objects.get(id=id)    
    if request.method=='POST':
        files=[]               
        for item in request.FILES:                        
            files.append(request.FILES[item])                   
        lista=os.listdir(os.path.join(BASE_DIR, 'settings/static')+'/fotos/'+str(id))
        try:
            lista.remove('arquivado')
        except:
            pass
        count=len(files)                
        if count>0:
            foto=Fotos(obra=Obra.objects.get(id=id), url="")
            foto.save()
            if foto.id<10:
                foto.url='0'+str(foto.id)+'.jpg'            
            else:
                foto.url=str(foto.id)+'.jpg'            
            foto.save()
            count=int(foto.id)
        for file in files:  
            if count<10:
                file_name='0'+str(count)
            else:
                file_name=str(count)
            path = default_storage.save(str(BASE_DIR)+'/settings/static/fotos/'+id+"/"+str(file_name)+".jpg", ContentFile(file.read()))                        
    context={
        'fotos': Fotos.objects.filter(obra=obra.obra.id),
        'obra': obra
    }
    return render(request, 'fiscalizacao/listar_fotos_obra.html', context)

@login_required
def visualizar_foto_obra(request, id, url):
    print(id, url)
    obra=Contrato.objects.get(id=id)     
    if request.method=='POST':
        try:
            file_name=url
            files=[]               
            for item in request.FILES:                        
                files.append(request.FILES[item])                                   
            for file in files:                  
                os.remove(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/'+str(file_name))
                path = default_storage.save(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+"/"+str(file_name), ContentFile(file.read()))                        
        except Exception as E:
            print(E)
    context={
        'foto_url': url,
        'obra': obra
    }
    return render(request, 'fiscalizacao/listar_foto_obra.html', context)

@login_required
def arquivar_foto_obra(request, id, url):    
    obra=Contrato.objects.get(id=id)     
    success='nops'
    if request.method=='POST':        
        try:            
            file_name=url              
            try:
                import shutil
                from datetime import date
                today = date.today()
                shutil.move(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/'+url, str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/arquivado/'+str(today.strftime("%m-%Y"))+'/'+url)                                
                success=True
            except:
                try:                
                    os.mkdir(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/arquivado/'+str(today.strftime("%m-%Y")))                 
                    shutil.move(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/'+url, str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/arquivado/'+str(today.strftime("%m-%Y"))+'/'+url)                
                    # os.remove(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/'+str(url))
                    success=True
                except:
                    try:
                        os.mkdir(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/arquivado')                 
                        os.mkdir(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/arquivado/'+str(today.strftime("%m-%Y")))
                        shutil.move(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/'+url, str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/arquivado/'+str(today.strftime("%m-%Y"))+'/'+url)                
                        # os.remove(str(BASE_DIR)+'/settings/static/fotos/'+str(id)+'/'+str(url))
                        success=True
                    except Exception as E:
                        print('ops')
                        success=False                         
        except Exception as E:
            print(E)
            success=False    
    if success==True:
        foto=Fotos.objects.get(obra=obra.obra, url=url)
        foto.delete()                          

    context={
        'foto_url': url,        
        'obra': obra,
        'success': success
    }
    return render(request, 'fiscalizacao/listar_foto_obra_apagar.html', context)

@login_required
def visualizar_notas(request, id):
    notas=Nota_Fiscal.objects.filter(id=id).order_by('dt_inclusao')
    form=Form_Nota()
    context={
        'obra': {'id': id},
        'notas':notas,
        'form': form
    }
    return render(request, 'fiscalizacao/listar_notas_obra.html', context)
@login_required
def gerar_qr_code(request, obra_id):
    conteudo = f'''localhost:8000/gerar-qr-code/{obra_id}'''
    context={
        'conteudo': conteudo,
        'obra_id': obra_id
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
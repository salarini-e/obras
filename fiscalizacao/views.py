from textwrap import indent
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import Form_Contrato, Form_Fiscal, Form_Nota, Form_Empenho_Desabilitado, Form_Empenho, Form_Obras, Form_Empresa
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages
from settings.settings import BASE_DIR
import os

from .functions import get_client_ip, progresso_obra, testarSeFoiAbatido

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def cadastrar_empresa(request): 
    if request.method=='POST':  
        form=Form_Empresa(request.POST)   
        # print(form)           
        if form.is_valid():
            empresa=form.save()             
            # acao={''}
            # log=Log(
            #         tabela='Empresa',
            #         ref=empresa.id,
            #         tipo='c', 
            #         acao=acao,
            #         user=request.user, 
            #         ipv4=get_client_ip(request)
            #     )
            # log.save()
            # print(empresa.id)
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
def editar_empenho(request, id, id_empenho): 
    empenho=Nota_Empenho.objects.get(id=id_empenho)
    form=Form_Empenho(instance=empenho)
    if request.method=='POST':  
        form=Form_Empenho(request.POST, instance=empenho)           
        if form.is_valid():
            empenho=form.save() 
            empenho.tipo_empenho='co'
            empenho.save()
            context={
                'form': form,
                'id': id,
                'success': 'Empenho atualizado com sucesso!'
            }
            return render(request, 'fiscalizacao/editar_empenho.html', context)                            
    context={
            'form': form,
            'id': id,
            'id_empenho': id_empenho
    }
    return render(request, 'fiscalizacao/editar_empenho.html', context)

@login_required
def substituir_empenho(request, id, id_empenho):     
    empenho=Nota_Empenho.objects.get(id=id_empenho)
    form_d=Form_Empenho_Desabilitado(instance=empenho)
    notas=Nota_Fiscal.objects.filter(empenho=empenho)
    soma=0
    for nota in notas:
        soma+=int(nota.valor)
    form=Form_Empenho(initial={'tipo_empenho': 'st','valor':int(empenho.valor)-soma, 'substituindo': id_empenho})
    if request.method=='POST':  
        form=Form_Empenho(request.POST)           
        if form.is_valid():            
            novo_empenho=form.save() 
            empenho.substituto=novo_empenho.id
            empenho.tipo_empenho='sd'
            empenho.save()
            contrato=Contrato.objects.get(id=id)
            contrato.nota_empenho.add(novo_empenho)
            contrato.save()
            novo_empenho.ativo=True            
            novo_empenho.save()
            empenho.ativo=False
            empenho.save()

            context={
                'form_d': form_d,
                'form': form,
                'id': id,
                'success': 'Empenho substituido com sucesso!'
            }
            return render(request, 'fiscalizacao/editar_empenho_substituir.html', context)                            
    context={
            'form_d': form_d,
            'form': form,
            'id': id,
            'id_empenho': id_empenho
    }
    return render(request, 'fiscalizacao/editar_empenho_substituir.html', context)

@login_required
def editar_nota(request, id, id_nota): 
    nota=Nota_Fiscal.objects.get(id=id_nota)
    form=Form_Nota(instance=nota)
    if request.method=='POST':  
        form=Form_Nota(request.POST, instance=nota)           
        if form.is_valid():
            form.save() 
            context={
                'form': form,
                'id': id,
                'success': 'Medição atualizada com sucesso!'
            }
            return render(request, 'fiscalizacao/editar_nota.html', context)                            
    context={
            'form': form,
            'id': id
    }
    return render(request, 'fiscalizacao/editar_nota.html', context)

@login_required
def editar_empresa(request, id): 
    empresa=Empresa.objects.get(id=id)
    form=Form_Empresa(instance=empresa)
    if request.method=='POST':  
        form_=Form_Empresa(request.POST, instance=empresa)           
        if form_.is_valid():
            # acoes={}
            # for i in form_:      
            #     if i.name!='cadastrado_por':    
            #         if form[i.name].value()!=form_.cleaned_data[i.name]:
            #             # print(i.name)                    
            #             acoes[i.name]={
            #                 'antes': form[i.name].value(),
            #                 'depois': form_.cleaned_data[i.name]
            #             }
            #     else:
            #         if form[i.name].value()!=form_.cleaned_data[i.name].id:
            #             acoes[i.name]={
            #                 'antes': form[i.name].value(),
            #                 'depois': form_.cleaned_data[i.name].id
            #             }
            # print(acoes)              
            empresa=form_.save()                         
            # log=Log(
            #         tabela='Empresa',
            #         ref=empresa.id,
            #         tipo='u', 
            #         acao=acoes,
            #         user=request.user, 
            #         ipv4=get_client_ip(request)
            #     )
            # log.save()            
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

def get_empenhos(request):    
    contrato=Contrato.objects.get(id=request.GET.get('id'))
    context={
        'empenhos': contrato.nota_empenho.filter(ativo=True, abatido=False),
    }
    return render(request, 'fiscalizacao/get_empenhos.html', context)

def get_notas(request):
    # print(request.GET.get('id'))
    try:        
        if request.GET.get('filter')=='all':
            contrato=Contrato.objects.get(id=request.GET.get('id'))
            notas=[]            
            for i in contrato.nota_empenho.filter(ativo=True):                
                nf=Nota_Fiscal.objects.filter(empenho=i).order_by('id')
                for n in nf:
                    notas.append(n)

            empenho_id=request.GET.get('id')
        else:
            empenho=Nota_Empenho.objects.get(id=request.GET.get('id'))
            notas=Nota_Fiscal.objects.filter(empenho=empenho).order_by('id') 
            empenho_id=empenho.n_nota   
    except Exception as E:
        print(E)
        notas=[]    
    soma_notas=0
    for nota in notas:
        try:
            soma_notas+=int(nota.valor)
        except:
            soma_notas+=0

    context={
        'filter': request.GET.get('filter'),
        'notas': notas,        
        'id': empenho_id,
        'soma_notas': soma_notas,   
        'obra_id': request.GET.get('obra_id')     
    }
    return render(request, 'fiscalizacao/get_notas_fiscais.html', context)

def get_notas_arquivadas(request):
    # print(request.GET.get('id'))
    try:        
        if request.GET.get('filter')=='all':
            contrato=Contrato.objects.get(id=request.GET.get('id'))
            notas=[]            
            for i in contrato.nota_empenho.filter(ativo=False):                
                nf=Nota_Fiscal.objects.filter(empenho=i).order_by('id')
                for n in nf:
                    notas.append(n)

            empenho_id=request.GET.get('id')
        else:
            empenho=Nota_Empenho.objects.get(id=request.GET.get('id'))
            notas=Nota_Fiscal.objects.filter(empenho=empenho).order_by('id') 
            empenho_id=empenho.n_nota   
    except Exception as E:
        print(E)
        notas=[]    
    soma_notas=0
    for nota in notas:
        try:
            soma_notas+=int(nota.valor)
        except:
            soma_notas+=0

    context={
        'filter': request.GET.get('filter'),
        'notas': notas,        
        'id': empenho_id,
        'soma_notas': soma_notas,   
        'obra_id': request.GET.get('obra_id')     
    }
    return render(request, 'fiscalizacao/get_notas_fiscais_arquivadas.html', context)

@login_required
def cadastrar_obra(request):    
    if request.method=='POST': 

        id_empenhos=request.POST['empenhos']
        id_empenhos=id_empenhos.split(';')
        id_empenhos.pop()
        list_empenhos=[]

        for id in id_empenhos:
            list_empenhos.append(Nota_Empenho.objects.get(n_nota=id))

        
        form_obra=Form_Obras(request.POST)

        try:
            empresa=Empresa.objects.get(nome=request.POST['empresa'])    
            go=True
        except:
            print(request.POST['empresa'])
            go=False
        
        if go:
            if form_obra.is_valid() and len(list_empenhos)>0:            
                try:
                    obra=form_obra.save()
                    contrato=Contrato(obra=obra, empresa=empresa)
                    contrato.save()
                    try:
                        for i in list_empenhos:
                            i.ativo=True
                            i.save()
                            contrato.nota_empenho.add(i)
                        contrato.save()
                    except Exception as E:
                        print(E)

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
            print(form_obra.errors)
            print(len(list_empenhos))
            error='ERROR'

    else:
        error=False        
        form_obra=Form_Obras(initial={'cadastrado_por':request.user})    

    context={
        'error': error,
        'form_nota': Form_Empenho(),
        'form_obra': form_obra,
    }
    return render(request, 'fiscalizacao/cadastrar_obra.html', context)

@login_required
def arquivar_empenho(request, id, id_empenho):    
    try:
        empenho=Nota_Empenho.objects.get(id=id_empenho)
        notas=Nota_Fiscal.objects.filter(empenho=empenho)        
        soma_notas=0
        for nota in notas:
            soma_notas+=int(nota.valor)

        if int(empenho.valor)==soma_notas:            
            empenho.ativo=False
            empenho.save()
            messages.success(request, 'Empenho de id: '+str(id_empenho)+' foi arquivado.')
        elif int(empenho.valor)>soma_notas:
            messages.error(request, 'Empenho de id: '+str(id_empenho)+' ainda não foi abatido. Tente substituir em vez de arquivar.')
        elif int(empenho.valor)<soma_notas:
            messages.error(request, 'Empenho de id: '+str(id_empenho)+' está com notas com valores acima do empenho.')
    except Exception as E:
        messages.error(request, str(E))
    return redirect('obra:visualizar_notas', id=id)

@login_required
def cadastrar_empenho(request, contrato_id):
    form=Form_Empenho()
    success=''
    if request.method=='POST':
        form=Form_Empenho(request.POST)
        if form.is_valid():
            obj=form.save()                        
            cont=Contrato.objects.get(id=contrato_id)
            cont.nota_empenho.add(obj)
            cont.save()
            obj.ativo=True
            obj.tipo_empenho='co'
            obj.save()
            success='Novo empenho cadastrado com sucesso!'                    
            form=Form_Empenho()
    context={
        'id': contrato_id,
        'form': form,
        'success': success
    }
    return render(request, 'fiscalizacao/cadastrar_empenho.html', context)

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
            foto=Fotos(obra=obra.obra, url="")
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
    if request.method=='POST':  
        form=Form_Nota(request.POST)                
        if form.is_valid():
            nota=form.save()    
            if testarSeFoiAbatido(nota):
                nota.empenho.abatido=True
                nota.empenho.save()
        else: 
            print(form.errors)                    
    else:
        # form=Form_Nota(initial={'cadastrado_por':request.user})
        form=Form_Nota()
    
    contratos=Contrato.objects.get(id=id)
    soma_notas, percent, soma_empenhos, previsto=progresso_obra(contratos)
    if percent!=0:
        progresso=int(soma_notas/percent)
        if progresso >= 100:
            progresso=100            
    else:
        progresso=0
    empenhos_exercicio=contratos.nota_empenho.filter(ativo=True)
    v_total=0
    for nota in empenhos_exercicio:
        v_total+=int(nota.valor)

    context={
        'obra': {'id': id},
        'notas':empenhos_exercicio,
        'form': form,
        'progresso': progresso,
        'soma_empenhos': v_total,
        'soma_notas': soma_notas,
        'previsto': previsto
    }
    return render(request, 'fiscalizacao/listar_notas_obra.html', context)

@login_required
def visualizar_notas_arquivadas(request, id):
    if request.method=='POST':  
        form=Form_Nota(request.POST)                
        if form.is_valid():
            form.save()    
        else: 
            print(form.errors)                    
    else:
        # form=Form_Nota(initial={'cadastrado_por':request.user})
        form=Form_Nota()
    
    contratos=Contrato.objects.get(id=id)
    soma_notas, percent, soma_empenhos, previsto=progresso_obra(contratos, False)
    if percent!=0:
        progresso=int(soma_notas/percent)
        if progresso >= 100:
            progresso=100            
    else:
        progresso=0
    
    empenhos_arquivados=contratos.nota_empenho.filter(ativo=False)
    v_total=0
    for nota in empenhos_arquivados:
        v_total+=int(nota.valor)
    
    context={
        'obra': {'id': id},
        'notas': empenhos_arquivados,
        'form': form,
        'progresso': progresso,
        'soma_empenhos': v_total,
        'soma_notas': soma_notas,
        'previsto': previsto
    }
    return render(request, 'fiscalizacao/listar_notas_obra_arquivadas.html', context)

@login_required
def editar_obra(request, id):
    print(id)
    contrato=Contrato.objects.get(id=id)
    form_obra=Form_Obras(instance=contrato.obra)
    if request.method=='POST':
        form_obra_POST=Form_Obras(request.POST, instance=contrato.obra)
        if form_obra_POST.is_valid():
            # acoes={}
            # for i in form_obra_POST:      
                # if i.name!='cadastrado_por':    
                #     if form_obra[i.name].value()!=form_obra_POST.cleaned_data[i.name]:
                                          
                #         acoes[i.name]={
                #             'antes': form_obra[i.name].value(),
                #             'depois': form_obra_POST.cleaned_data[i.name]
                #         }
                # else:
                #     if form_obra[i.name].value()!=form_obra_POST.cleaned_data[i.name].id:
                #         acoes[i.name]={
                #             'antes': form_obra[i.name].value(),
                #             'depois': form_obra_POST.cleaned_data[i.name].id
                #         }                        
            obra=form_obra_POST.save()
            form_obra=Form_Obras(instance=obra)
            # log=Log(
            #         tabela='Obra',
            #         ref=contrato.obra.id,
            #         tipo='u', 
            #         acao=acoes,
            #         user=request.user, 
            #         ipv4=get_client_ip(request)
            #     )
            # log.save()          
    

    context={
        'obra': {'id':id},        
        'empresa': contrato.empresa.nome,
        'form_obra': form_obra
    }
    return render(request, 'fiscalizacao/listar_itens_obra_editar.html', context)

@login_required
def gerar_qr_code(request, obra_id):
    conteudo = f'''obras.pmnf.rj.gov.br/dados-obras/v/{obra_id}'''
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
from .models import Nota_Fiscal, Nota_Empenho

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def progresso_obra(contratos, ativo=True):
    soma_empenhos=0
    soma_notas=0  
    previsto=int(contratos.obra.valor_previsto)  
    ids=[]
    for i in contratos.nota_empenho.all():
        soma_empenhos+=int(i.valor)
        notas_fiscais=Nota_Fiscal.objects.filter(empenho=i)
        for n in notas_fiscais:
            soma_notas+=int(n.valor)
        
    percent=previsto/100.00
    return soma_notas, percent, soma_empenhos, previsto

def testarSeFoiAbatido(nota):
    notas=Nota_Fiscal.objects.filter(empenho=nota.empenho)
    soma_notas=0
    for n in notas:
        soma_notas+=int(n.valor)
    if int(nota.empenho.valor)<=soma_notas:
        return True
    return False

    
    
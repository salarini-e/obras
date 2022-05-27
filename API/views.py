from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from requests import request
from rest_framework.parsers import JSONParser
from fiscalizacao.models import Nota_Empenho
from .serializer import NotaEmpenhoSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import generics

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from fiscalizacao.forms import Form_Empenho

class Listar_Empenho(generics.ListAPIView):
    queryset=Nota_Empenho.objects.all()
    serializer_class=NotaEmpenhoSerializer
    permission_classes=[IsAuthenticated]

class add_empenho(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'fiscalizacao/cadastrar_obra_get_empenho.html'

    def get(self, request):
        return Response({'nota':'get'})
    def post(self, request):    
        form=Form_Empenho(request.data)
        if form.is_valid():
            fail=False
            nota=form.save()
        else:             
            fail=True
            nota=form.errors
        return Response({'nota': nota, 'fail': fail})

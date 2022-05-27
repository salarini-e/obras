from rest_framework import serializers
from fiscalizacao.models import Nota_Empenho

class NotaEmpenhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota_Empenho
        fields = ['id', 'valor'] 
        
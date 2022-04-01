from django import views
from django.contrib import admin
from django.urls import path
from . import views

app_name='obra'

urlpatterns = [
    path('', views.index, name='index' ),
    path('cadastrar-obra/', views.cadastrar_obra, name='cadastrar' ),
    path('fiscal/', views.fiscalizar_obra, name='visualizar' ),
    path('gerar-qr-code/', views.gerar_qr_code, name='gerar_qrcode' ),
]

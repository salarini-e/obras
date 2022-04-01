from django import views
from django.contrib import admin
from django.urls import path
from . import views

app_name='obra'

urlpatterns = [
    path('', views.index, name='index' ),
    path('login/', views.login_view, name='login' ),
    path('logout/', views.logout_view, name='logout' ),
    path('cadastrar-obra/', views.cadastrar_obra, name='cadastrar' ),
    path('ver-obra/<obra_id>', views.fiscalizar_obra, name='visualizar' ),
    path('gerar-qr-code/<obra_id>', views.gerar_qr_code, name='gerar_qrcode' ),
]

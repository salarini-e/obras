from django import views
from django.contrib import admin
from django.urls import path
from . import views

app_name='obra'

urlpatterns = [
    path('get_empresa/', views.get_empresa, name='get_empresa' ),    
    path('teste/', views.teste, name='teste' ),

    path('', views.index, name='index' ),

    path('login/', views.login_view, name='login' ),
    path('logout/', views.logout_view, name='logout' ),

    path('cadastrar-obra/', views.cadastrar_obra, name='cadastrar' ),
    path('get-obras/', views.get_obras, name='get_obras' ),
    path('dados-obras/<valor_busca>', views.listar_obras, name='visualizar' ),
    path('dados-obras/v/<id>', views.visualizar_obra, name='visualizar_obra' ),
    path('dados-obras/v/<id>/fotos', views.visualizar_fotos_obra, name='visualizar_fotos_obra' ),
    path('dados-obras/v/<id>/fotos/<url>', views.visualizar_foto_obra, name='visualizar_foto_obra' ),
    path('dados-obras/v/<id>/fotos/<url>/arquivar', views.arquivar_foto_obra, name='arquivar_foto_obra' ),
    path('dados-obras/v/<id>/notas', views.visualizar_notas, name='visualizar_notas' ),
    
    path('cadastrar-empresa/', views.cadastrar_empresa, name='cadastrar_empresa' ),
    path('editar-empresa/<id>', views.editar_empresa, name='editar_empresa' ),
    path('listar-empresa/', views.listar_empresa, name='listar_empresa' ),
    path('listar-empresa/v/<id>', views.visualizar_empresa, name='visualizar_empresa' ),    
    path('listar-empresa/h', views.historico_empresa, name='historico_empresa' ),
    path('listar-empresa/h/a/<id>', views.historico_empresa_acoes, name='historico_empresa_acoes' ),
    
    path('cadastrar-fiscal/', views.cadastrar_fiscal, name='cadastrar_fiscal' ),
    path('listar-fiscais/', views.listar_fiscais, name='listar_fiscais' ),

    path('ver-obra/', views.fiscalizar_obra, name='buscar' ),
    # path('ver-obra/<valor_busca>', views.fiscalizar_obra, name='visualizar' ),
    path('gerar-qr-code/<obra_id>', views.gerar_qr_code, name='gerar_qrcode' ),
]

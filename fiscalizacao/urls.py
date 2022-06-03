from django import views
from django.contrib import admin
from django.urls import path
from . import views

app_name='obra'

urlpatterns = [
    path('get_empresa/', views.get_empresa, name='get_empresa' ),    
    path('get_notas/', views.get_notas, name='get_notas' ),    
    path('get_notas_arquivadas/', views.get_notas_arquivadas, name='get_notas_arquivadas' ),    
    path('teste/', views.teste, name='teste' ),

    path('', views.index, name='index' ),

    path('login/', views.login_view, name='login' ),
    path('logout/', views.logout_view, name='logout' ),

    path('cadastrar-obra/', views.cadastrar_obra, name='cadastrar' ),
    path('get-obras/', views.get_obras, name='get_obras' ),
    path('get-empenho/', views.get_empenhos, name='get_empenhos' ),
    
    path('dados-obras/<valor_busca>', views.listar_obras, name='visualizar' ),
    path('dados-obras/v/<id>', views.visualizar_obra, name='visualizar_obra' ),
    
    path('dados-obras/v/<id>/editar', views.editar_obra, name='editar_obra' ),

    path('dados-obras/v/<id>/fotos', views.visualizar_fotos_obra, name='visualizar_fotos_obra' ),
    path('dados-obras/v/<id>/fotos/<url>', views.visualizar_foto_obra, name='visualizar_foto_obra' ),
    path('dados-obras/v/<id>/fotos/<url>/arquivar', views.arquivar_foto_obra, name='arquivar_foto_obra' ),
    
    path('dados-obras/v/<id>/notas', views.visualizar_notas, name='visualizar_notas' ),
    path('dados-obras/v/<id>/notas_arquivadas', views.visualizar_notas_arquivadas, name='visualizar_notas_arquivadas' ),
    path('dados-obras/v/<id>/notas/editar-empenho/<id_empenho>', views.editar_empenho, name='editar_empenho' ),
    path('dados-obras/v/<id>/notas/arquivar-empenho/<id_empenho>', views.arquivar_empenho, name='arquivar_empenho' ),
    path('dados-obras/v/<id>/notas/editar-nota/<id_nota>', views.editar_nota, name='editar_nota' ),
    path('dados-obras/v/<contrato_id>/notas/cad_empenho', views.cadastrar_empenho, name='cadastrar_empenho' ),

    path('cadastrar-empresa/', views.cadastrar_empresa, name='cadastrar_empresa' ),
    path('editar-empresa/<id>', views.editar_empresa, name='editar_empresa' ),
    path('listar-empresa/', views.listar_empresa, name='listar_empresa' ),
    path('listar-empresa/v/<id>', views.visualizar_empresa, name='visualizar_empresa' ),    
    path('listar-empresa/h', views.historico_empresa, name='historico_empresa' ),
    path('listar-empresa/h/a/<id>', views.historico_empresa_acoes, name='historico_empresa_acoes' ),

    path('cadastrar-fiscal/', views.cadastrar_fiscal, name='cadastrar_fiscal' ),
    path('listar-fiscais/', views.listar_fiscais, name='listar_fiscais' ),

    # path('ver-obra/', views.fiscalizar_obra, name='buscar' ),
    # path('ver-obra/<valor_busca>', views.fiscalizar_obra, name='visualizar' ),
    path('gerar-qr-code/<obra_id>', views.gerar_qr_code, name='gerar_qrcode' ),
]

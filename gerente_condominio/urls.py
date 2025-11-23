from django.urls import path
from . import views # Importa as views da sua aplicação

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('noticias/', views.gerenciar_noticias, {'acao': 'lista'}, name='gerenciar_noticias'), 
    path('noticias/adicionar/', views.gerenciar_noticias, {'acao': 'adicionar'}, name='adicionar_noticia'), 
    
    # 2. DETALHE, EDITAR e EXCLUIR (URL com PK)
    # URL: /noticias/123/detalhe/ | URL: /noticias/123/editar/ | URL: /noticias/123/excluir/
    path('noticias/<int:pk>/detalhe/', views.gerenciar_noticias, {'acao': 'detalhe'}, name='detalhe_noticia'),
    path('noticias/<int:pk>/editar/', views.gerenciar_noticias, {'acao': 'editar'}, name='editar_noticia'),
    path('noticias/<int:pk>/excluir/', views.gerenciar_noticias, {'acao': 'excluir'}, name='excluir_noticia'),

    path('ver-inquilinos/', views.ver_inquilinos, name='ver_inquilinos'),
    path('ver-casas/', views.ver_casas, name='ver_casas'),
    path('ver-contratos/', views.ver_contratos, name='ver_contratos'),
    path('ver-manutencoes/', views.ver_manutencoes, name='ver_manutencoes'),
    path('ver-empresas/', views.ver_empresas, name='ver_empresas'),

    # AJAX URLs for CRUD
    path('add-inquilino/', views.add_inquilino, name='add_inquilino'),
    path('edit-inquilino/<int:pk>/', views.edit_inquilino, name='edit_inquilino'),
    path('delete-inquilino/<int:pk>/', views.delete_inquilino, name='delete_inquilino'),

    path('add-casa/', views.add_casa, name='add_casa'),
    path('edit-casa/<int:pk>/', views.edit_casa, name='edit_casa'),
    path('delete-casa/<int:pk>/', views.delete_casa, name='delete_casa'),

    path('add-contrato/', views.add_contrato, name='add_contrato'),
    path('edit-contrato/<int:pk>/', views.edit_contrato, name='edit_contrato'),
    path('delete-contrato/<int:pk>/', views.delete_contrato, name='delete_contrato'),

    path('add-manutencao/', views.add_manutencao, name='add_manutencao'),
    path('manutencoes/get-detalhes/<str:tipo>/<int:id>/', views.get_detalhes_manutencao, name='get_detalhes_manutencao'),
    path('manutencoes/editar/<str:tipo>/<int:id>/', views.editar_manutencao, name='editar_manutencao'),
    path('manutencoes/excluir/<str:tipo>/<int:id>/', views.excluir_manutencao, name='excluir_manutencao'),

    path('add-empresa/', views.add_empresa, name='add_empresa'),
    path('edit-empresa/<int:pk>/', views.edit_empresa, name='edit_empresa'),
    path('delete-empresa/<int:pk>/', views.delete_empresa, name='delete_empresa'),

    # API endpoints
    path('api/get-empresas/', views.get_empresas, name='get_empresas'),
    path('api/get-condominios/', views.get_condominios, name='get_condominios'),
    path('api/get-casas/', views.get_casas, name='get_casas'),
    path('api/get-inquilinos/', views.get_inquilinos, name='get_inquilinos'),
    path('api/get-historico-empresa/<int:empresa_id>/', views.get_historico_empresa, name='get_historico_empresa'),

    # Welcome endpoint
    path('welcome/', views.welcome, name='welcome'),
]
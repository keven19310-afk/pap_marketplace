from django.urls import path
from . import views

urlpatterns = [
    # Catálogo e Pesquisa
    path('', views.lista_produtos, name='lista_produtos'),
    
    # Gestão de Produtos (CRUD)
    path('criar/', views.criar_produto, name='criar_produto'),
    path('produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('produto/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('produto/<int:id>/apagar/', views.apagar_produto, name='apagar_produto'),
    path('produto/<int:id>/vendido/', views.marcar_vendido, name='marcar_vendido'),
    
    # Carrinho e Reservas
    path('carrinho/adicionar/<int:id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    
    # Propostas de Troca
    path('produto/<int:id>/propor-troca/', views.propor_troca, name='propor_troca'),
    
    # Autenticação e Área Pessoal
    path('entrar/', views.entrar_view, name='entrar'),
    path('registar/', views.registar_view, name='registar'),
    path('sair/', views.sair_view, name='sair'),
    path('meus-anuncios/', views.meus_anuncios, name='meus_anuncios'),
    
    # Formulário de Contacto
    path('contacto/', views.enviar_contacto, name='enviar_contacto'),
]
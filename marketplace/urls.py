from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('criar/', views.criar_produto, name='criar_produto'),
    path('produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('produto/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('produto/<int:id>/apagar/', views.apagar_produto, name='apagar_produto'),
    path('carrinho/adicionar/<int:id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
]
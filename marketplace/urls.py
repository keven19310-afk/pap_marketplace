from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('criar/', views.criar_produto, name='criar_produto'),
    path('produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('produto/<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('produto/<int:id>/apagar/', views.apagar_produto, name='apagar_produto'),
]
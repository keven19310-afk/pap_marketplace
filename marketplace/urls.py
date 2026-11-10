from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('criar/', views.criar_produto, name='criar_produto'),
]
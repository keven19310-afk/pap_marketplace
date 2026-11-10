from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, PropostaTroca, PedidoProcura
from .forms import ProdutoForm, PropostaTrocaForm, PedidoProcuraForm
from django.contrib.auth import get_user_model

# 1. Página Inicial / Catálogo
def lista_produtos(request):
    produtos = Produto.objects.filter(status='disponivel').order_by('-data_criacao')
    return render(request, 'marketplace/home.html', {'produtos': produtos})

# 2. Criar Novo Anúncio (Sem exigir Login)
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            
            # Pega o primeiro utilizador que existir ou associa um temporário
            User = get_user_model()
            usuario_padrao = User.objects.first()
            if not usuario_padrao:
                usuario_padrao = User.objects.create_user(username='anónimo', password='123')
            
            produto.vendedor = usuario_padrao
            produto.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'marketplace/criar_produto.html', {'form': form})
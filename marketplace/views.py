from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto, PropostaTroca, PedidoProcura
from .forms import ProdutoForm, PropostaTrocaForm

# 1. Página Inicial / Catálogo
def lista_produtos(request):
    produtos = Produto.objects.filter(status='disponivel').order_by('-data_criacao')
    return render(request, 'marketplace/home.html', {'produtos': produtos})

# 2. Criar Novo Anúncio de Produto
@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.vendedor = request.user
            produto.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'marketplace/criar_produto.html', {'form': form})
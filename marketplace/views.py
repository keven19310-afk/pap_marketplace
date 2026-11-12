from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, PropostaTroca, PedidoProcura
from .forms import ProdutoForm, PropostaTrocaForm, PedidoProcuraForm
from django.contrib.auth import get_user_model

# 1. Página Inicial / Catálogo
def lista_produtos(request):
    produtos = Produto.objects.filter(status='disponivel').order_by('-data_criacao')
    return render(request, 'home.html', {'produtos': produtos})

# 2. Criar Novo Anúncio (Sem exigir Login + Upload de Imagens)
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            
            User = get_user_model()
            usuario_padrao = User.objects.first()
            if not usuario_padrao:
                usuario_padrao = User.objects.create_user(username='anónimo', password='123')
            
            produto.vendedor = usuario_padrao
            produto.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'criar_produto.html', {'form': form})

# 3. Ver Detalhes do Produto
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'detalhe_produto.html', {'produto': produto})

# 4. Editar Produto (Alterar foto, preço, título, etc.)
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('detalhe_produto', id=produto.id)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})

# 5. Apagar Produto
def apagar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    return redirect('detalhe_produto', id=produto.id)
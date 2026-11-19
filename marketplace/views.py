from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Produto, PropostaTroca, PedidoProcura
from .forms import ProdutoForm, PropostaTrocaForm, PedidoProcuraForm
from django.contrib.auth import get_user_model

# Função auxiliar para obter os produtos do carrinho (usando dicionário {id: qtd})
def obter_dados_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    # Compatibilidade caso ainda exista o formato antigo em lista na sessão
    if isinstance(carrinho, list):
        carrinho = {str(i): 1 for i in carrinho}
        request.session['carrinho'] = carrinho

    itens_carrinho = []
    total_carrinho = 0
    qtd_total_itens = 0

    for prod_id_str, qtd in carrinho.items():
        produto = Produto.objects.filter(id=int(prod_id_str)).first()
        if produto and qtd > 0:
            subtotal = produto.preco * qtd
            total_carrinho += subtotal
            qtd_total_itens += qtd
            itens_carrinho.append({
                'produto': produto,
                'quantidade': qtd,
                'subtotal': subtotal,
            })

    return itens_carrinho, total_carrinho, qtd_total_itens

# 1. Página Inicial / Catálogo
def lista_produtos(request):
    produtos = Produto.objects.filter(status='disponivel').order_by('-data_criacao')
    
    categoria_selecionada = request.GET.get('categoria')
    termo_pesquisa = request.GET.get('q')

    if categoria_selecionada:
        produtos = produtos.filter(categoria__iexact=categoria_selecionada)

    if termo_pesquisa:
        produtos = produtos.filter(
            Q(titulo__icontains=termo_pesquisa) |
            Q(descricao__icontains=termo_pesquisa) |
            Q(localizacao__icontains=termo_pesquisa)
        )

    itens_carrinho, total_carrinho, qtd_carrinho = obter_dados_carrinho(request)

    return render(request, 'home.html', {
        'produtos': produtos,
        'categoria_selecionada': categoria_selecionada,
        'termo_pesquisa': termo_pesquisa,
        'itens_carrinho': itens_carrinho,
        'total_carrinho': total_carrinho,
        'qtd_carrinho': qtd_carrinho,
    })

# 2. Criar Novo Anúncio
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
    return render(request, 'produto.html', {'form': form, 'modo': 'criar'})

# 3. Ver Detalhes do Produto
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    carrinho = request.session.get('carrinho', {})
    if isinstance(carrinho, list):
        carrinho = {str(i): 1 for i in carrinho}
        request.session['carrinho'] = carrinho

    qtd_no_carrinho = carrinho.get(str(produto.id), 0)
    return render(request, 'produto.html', {
        'produto': produto,
        'modo': 'detalhe',
        'qtd_no_carrinho': qtd_no_carrinho,
    })

# 4. Editar Produto
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('detalhe_produto', id=produto.id)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto.html', {'form': form, 'produto': produto, 'modo': 'editar'})

# 5. Apagar Produto
def apagar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    return redirect('detalhe_produto', id=produto.id)

# 6. Adicionar 1 unidade ao Carrinho (e descontar 1 do Stock)
def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)
    carrinho = request.session.get('carrinho', {})
    if isinstance(carrinho, list):
        carrinho = {str(i): 1 for i in carrinho}

    if produto.quantidade > 0:
        produto.quantidade -= 1
        produto.save()

        prod_id_str = str(produto.id)
        carrinho[prod_id_str] = carrinho.get(prod_id_str, 0) + 1
        request.session['carrinho'] = carrinho

    return redirect('detalhe_produto', id=produto.id)

# 7. Remover do Carrinho (e devolver as unidades ao Stock)
def remover_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)
    carrinho = request.session.get('carrinho', {})
    if isinstance(carrinho, list):
        carrinho = {str(i): 1 for i in carrinho}

    prod_id_str = str(produto.id)
    if prod_id_str in carrinho:
        qtd_devolver = carrinho.pop(prod_id_str)
        produto.quantidade += qtd_devolver
        produto.save()
        request.session['carrinho'] = carrinho

    return redirect('lista_produtos')

# 8. Finalizar Compra (Mantém o stock descontado e esvazia o carrinho)
def finalizar_compra(request):
    if request.method == 'POST':
        request.session['carrinho'] = {}
        messages.success(request, 'Pedido reservado com sucesso! O stock foi atualizado e o vendedor entrará em contacto.')
    return redirect('lista_produtos')
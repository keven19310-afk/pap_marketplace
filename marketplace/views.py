from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from .models import Produto, PropostaTroca, PedidoProcura
from .forms import ProdutoForm, PropostaTrocaForm, PedidoProcuraForm

User = get_user_model()

# Função auxiliar para calcular o carrinho guardado na sessão
def obter_dados_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    itens = []
    total = Decimal('0.00')
    qtd_total = 0
    for prod_id, qtd in carrinho.items():
        produto = Produto.objects.filter(id=prod_id).first()
        if produto:
            subtotal = produto.preco * qtd
            total += subtotal
            qtd_total += qtd
            itens.append({
                'produto': produto,
                'quantidade': qtd,
                'subtotal': subtotal
            })
    return itens, total, qtd_total

# 1. Página Inicial / Catálogo com Pesquisa, Categoria, Troca e Ordenação
def lista_produtos(request):
    produtos = Produto.objects.filter(status='disponivel')
    
    categoria = request.GET.get('categoria')
    termo = request.GET.get('q')
    so_troca = request.GET.get('troca')
    ordem = request.GET.get('ordem', '-data_criacao')

    if categoria:
        produtos = produtos.filter(categoria__iexact=categoria)
    if termo:
        produtos = produtos.filter(
            Q(titulo__icontains=termo) | 
            Q(descricao__icontains=termo) | 
            Q(localizacao__icontains=termo)
        )
    if so_troca == '1':
        produtos = produtos.filter(aceita_troca=True)

    if ordem in ['preco', '-preco', '-data_criacao']:
        produtos = produtos.order_by(ordem)
    else:
        produtos = produtos.order_by('-data_criacao')

    itens_carrinho, total_carrinho, qtd_carrinho = obter_dados_carrinho(request)

    return render(request, 'home.html', {
        'produtos': produtos,
        'categoria_selecionada': categoria,
        'termo_pesquisa': termo,
        'so_troca': so_troca,
        'ordem_selecionada': ordem,
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
            if request.user.is_authenticated:
                produto.vendedor = request.user
            else:
                usuario_padrao = User.objects.first()
                if not usuario_padrao:
                    usuario_padrao = User.objects.create_user(username='anonimo', password='123')
                produto.vendedor = usuario_padrao
            produto.save()
            messages.success(request, 'Anúncio publicado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produto.html', {'form': form, 'modo': 'criar'})

# 3. Ver Detalhes do Produto + Formulário de Proposta de Troca
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    form_troca = PropostaTrocaForm()
    propostas = PropostaTroca.objects.filter(produto_alvo=produto).order_by('-data_proposta')
    itens_carrinho, total_carrinho, qtd_carrinho = obter_dados_carrinho(request)
    
    pode_gerir = (
        request.user.is_superuser or 
        (request.user.is_authenticated and produto.vendedor == request.user) or
        (not request.user.is_authenticated and produto.vendedor.username in ['anonimo', 'anónimo'])
    )

    return render(request, 'produto.html', {
        'produto': produto,
        'modo': 'detalhe',
        'form_troca': form_troca,
        'propostas': propostas,
        'pode_gerir': pode_gerir,
        'itens_carrinho': itens_carrinho,
        'total_carrinho': total_carrinho,
        'qtd_carrinho': qtd_carrinho,
    })

# 4. Editar Produto
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alterações guardadas com sucesso!')
            return redirect('detalhe_produto', id=produto.id)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto.html', {'form': form, 'produto': produto, 'modo': 'editar'})

# 5. Apagar Produto
def apagar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Anúncio apagado permanentemente.')
        return redirect('lista_produtos')
    return redirect('detalhe_produto', id=produto.id)

# 6. Marcar Produto como Vendido
def marcar_vendido(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.status = 'vendido'
        produto.save()
        messages.success(request, f'O artigo "{produto.titulo}" foi marcado como Vendido!')
    return redirect('detalhe_produto', id=produto.id)

# 7. Carrinho: Adicionar, Remover e Finalizar Reserva
def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)
    carrinho = request.session.get('carrinho', {})
    prod_id = str(produto.id)
    
    qtd_atual = carrinho.get(prod_id, 0)
    if qtd_atual < produto.quantidade:
        carrinho[prod_id] = qtd_atual + 1
        request.session['carrinho'] = carrinho
        messages.success(request, f'"{produto.titulo}" foi adicionado ao teu carrinho!')
    else:
        messages.warning(request, 'Já atingiste a quantidade máxima disponível deste artigo.')
    
    pagina_anterior = request.META.get('HTTP_REFERER')
    if pagina_anterior:
        return redirect(pagina_anterior)
    return redirect('lista_produtos')

def remover_carrinho(request, id):
    carrinho = request.session.get('carrinho', {})
    prod_id = str(id)
    if prod_id in carrinho:
        del carrinho[prod_id]
        request.session['carrinho'] = carrinho
        messages.success(request, 'Artigo removido do carrinho.')
    return redirect('lista_produtos')

def finalizar_compra(request):
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})
        for prod_id, qtd in carrinho.items():
            produto = Produto.objects.filter(id=prod_id).first()
            if produto:
                produto.quantidade = max(0, produto.quantidade - qtd)
                if produto.quantidade == 0:
                    produto.status = 'vendido'
                produto.save()
        request.session['carrinho'] = {}
        messages.success(request, 'Reserva concluída com sucesso! O vendedor foi notificado.')
    return redirect('lista_produtos')

# 8. Propor Troca num Produto
def propor_troca(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = PropostaTrocaForm(request.POST, request.FILES)
        if form.is_valid():
            proposta = form.save(commit=False)
            proposta.produto_alvo = produto
            proposta.proprietario = produto.vendedor
            if request.user.is_authenticated:
                proposta.proponente = request.user
            else:
                usuario_padrao = User.objects.first()
                if not usuario_padrao:
                    usuario_padrao = User.objects.create_user(username='anonimo', password='123')
                proposta.proponente = usuario_padrao
            proposta.save()
            messages.success(request, 'A tua proposta de troca foi enviada ao vendedor!')
        else:
            messages.error(request, 'Verifica os dados da proposta de troca e tenta novamente.')
    return redirect('detalhe_produto', id=produto.id)

# 9. Autenticação (Entrar, Registar, Sair) e Os Meus Anúncios
def entrar_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.username}!')
            return redirect('lista_produtos')
        else:
            messages.error(request, 'Nome de utilizador ou palavra-passe incorretos.')
    return redirect('lista_produtos')

def registar_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Esse nome de utilizador já está em uso.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}.')
    return redirect('lista_produtos')

def sair_view(request):
    logout(request)
    messages.success(request, 'Terminaste a sessão.')
    return redirect('lista_produtos')

@login_required(login_url='/')
def meus_anuncios(request):
    produtos = Produto.objects.filter(vendedor=request.user).order_by('-data_criacao')
    itens_carrinho, total_carrinho, qtd_carrinho = obter_dados_carrinho(request)
    return render(request, 'home.html', {
        'produtos': produtos,
        'modo_meus_anuncios': True,
        'itens_carrinho': itens_carrinho,
        'total_carrinho': total_carrinho,
        'qtd_carrinho': qtd_carrinho,
    })

# 10. Contacto
def enviar_contacto(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        messages.success(request, f'Obrigado pelo teu contacto, {nome}! Responderemos em breve.')
    return redirect('lista_produtos')
from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Utilizador Híbrido (Comprador + Vendedor)
class Utilizador(AbstractUser):
    e_loja_verificada = models.BooleanField(default=False)
    nome_loja = models.CharField(max_length=100, blank=True, null=True)
    saldo_disponivel = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo_cativo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Cofre Digital (Escrow)

    def __str__(self):
        return self.username


# 2. Catálogo de Produtos
class Produto(models.Model):
    CATEGORIAS_CHOICES = [
        ('tecnologia', 'Tecnologia'),
        ('moda', 'Moda'),
        ('casa', 'Casa (Utensílios Domésticos)'),
        ('desporto', 'Desporto'),
        ('gaming', 'Gaming'),
        ('livros', 'Livros'),
    ]

    ESTADO_CHOICES = [
        ('novo', 'Novo'),
        ('semi_novo', 'Semi Novo'),
        ('muito_usado', 'Muito Usado'),
    ]

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
        ('vendido', 'Vendido'),
        ('trocado', 'Trocado'),
    ]

    vendedor = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='produtos')
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS_CHOICES, default='tecnologia')
    estado_conservacao = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='semi_novo')
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=1)
    localizacao = models.CharField(max_length=100, default='Portugal')
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    
    aceita_troca = models.BooleanField(default=False)
    preferencias_troca = models.CharField(max_length=255, blank=True, null=True, help_text="O que aceita em troca?")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# 3. Propostas de Troca Direta (Simulada / Escrow)
class PropostaTroca(models.Model):
    STATUS_PROPOSTA = [
        ('pendente', 'Pendente'),
        ('aceite', 'Aceite'),
        ('rejeitada', 'Rejeitada'),
        ('cancelada', 'Cancelada'),
    ]

    proponente = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='propostas_enviadas')
    proprietario = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='propostas_recebidas')
    produto_alvo = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='trocas_alvo')
    produto_oferecido = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='trocas_oferecidas')
    valor_ajuste = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) # Acerto em dinheiro se necessário
    status = models.CharField(max_length=20, choices=STATUS_PROPOSTA, default='pendente')
    data_proposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Troca: {self.produto_oferecido.titulo} por {self.produto_alvo.titulo}"


# 4. Mural "Procuro Produto" (Anúncios Invertidos)
class PedidoProcura(models.Model):
    cliente = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='pedidos_procura')
    titulo_procurado = models.CharField(max_length=150)
    descricao = models.TextField()
    orcamento_maximo = models.DecimalField(max_digits=8, decimal_places=2)
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo_procurado
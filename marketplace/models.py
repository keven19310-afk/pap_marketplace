from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilizador(AbstractUser):
    e_loja_verificada = models.BooleanField(default=False)
    nome_loja = models.CharField(max_length=100, blank=True, null=True)
    saldo_disponivel = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo_cativo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username

class Produto(models.Model):
    ESTADO_CHOICES = [
        ('novo', 'Novo'),
        ('como_novo', 'Como Novo'),
        ('usado', 'Usado'),
    ]
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
        ('vendido', 'Vendido'),
        ('trocado', 'Trocado'),
    ]

    vendedor = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name='produtos')
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estado_conservacao = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    aceita_troca = models.BooleanField(default=False)
    preferencias_troca = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
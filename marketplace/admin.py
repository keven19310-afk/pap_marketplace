from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilizador, Produto

# Regista o modelo de Utilizador
@admin.register(Utilizador)
class UtilizadorAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informação do Marketplace', {'fields': ('is_loja', 'nome_loja', 'saldo')}),
    )

# Regista o modelo de Produto
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass
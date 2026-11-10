from django import forms
from .models import Produto, PropostaTroca, PedidoProcura

# 1. Formulário para Publicar Produtos
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'titulo', 
            'categoria', 
            'estado_conservacao', 
            'preco', 
            'quantidade', 
            'localizacao', 
            'imagem', 
            'descricao', 
            'aceita_troca', 
            'preferencias_troca'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Consola PS5'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado_conservacao': forms.Select(attrs={'class': 'form-select'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Aveiro, Porto, Lisboa'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreve o produto em pormenor...'}),
            'aceita_troca': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_aceita_troca'}),
            'preferencias_troca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Obrigatório: especifica o que aceitas em troca (ex: telemóveis, jogos PS5)'}),
        }


# 2. Formulário para Enviar Proposta de Troca
class PropostaTrocaForm(forms.ModelForm):
    class Meta:
        model = PropostaTroca
        fields = ['produto_oferecido', 'valor_ajuste']
        widgets = {
            'produto_oferecido': forms.Select(attrs={'class': 'form-select'}),
            'valor_ajuste': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }


# 3. Formulário para Criar Pedido no Mural "Procuro..."
class PedidoProcuraForm(forms.ModelForm):
    class Meta:
        model = PedidoProcura
        fields = ['titulo_procurado', 'descricao', 'orcamento_maximo']
        widgets = {
            'titulo_procurado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Manual de Matemática 12º Ano'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalhes do artigo que estás a procurar...'}),
            'orcamento_maximo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
        }
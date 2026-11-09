from django import forms
from .models import Produto, PropostaTroca, PedidoProcura

# Formulário para Publicar Produtos
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['titulo', 'descricao', 'preco', 'estado_conservacao', 'aceita_troca', 'preferencias_troca']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'Ex: Bicicleta de Montanha'}),
            'descricao': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-xl', 'rows': 4, 'placeholder': 'Descreve o produto...'}),
            'preco': forms.NumberInput(attrs={'class': 'w-full p-3 border rounded-xl', 'step': '0.01'}),
            'estado_conservacao': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl'}),
            'preferencias_troca': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'Ex: Aceito trocas por material escolar ou jogos'}),
        }

# Formulário para Enviar Proposta de Troca
class PropostaTrocaForm(forms.ModelForm):
    class Meta:
        model = PropostaTroca
        fields = ['produto_oferecido', 'valor_ajuste']
        widgets = {
            'produto_oferecido': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl'}),
            'valor_ajuste': forms.NumberInput(attrs={'class': 'w-full p-3 border rounded-xl', 'step': '0.01'}),
        }
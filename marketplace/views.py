from django.shortcuts import render
from .models import Produto

def home(request):
    produtos = Produto.objects.all()
    return render(request, 'marketplace/home.html', {'produtos': produtos})
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CadastroForm
from .models import Produto, Assinatura, Pedido
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos.html', {'produtos': produtos})

def lista_assinaturas(request):
    assinaturas = Assinatura.objects.all()
    return render(request, 'assinaturas.html', {'assinaturas': assinaturas})

@login_required
def comprar_produto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    pedido = Pedido.objects.create(usuario=request.user, produto=produto, status='pago')
    return render(request, 'compra_sucesso.html', {'pedido': pedido})

@login_required
def assinar_plano(request, assinatura_id):
    assinatura = Assinatura.objects.get(id=assinatura_id)
    pedido = Pedido.objects.create(usuario=request.user, assinatura=assinatura, status='pago')
    return render(request, 'assinatura_sucesso.html', {'pedido': pedido})
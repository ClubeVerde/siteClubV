from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CadastroForm
from .models import Produto, Assinatura, Pedido 
from django.contrib.auth.decorators import login_required


def home(request):
    produtos = Produto.objects.all() 
    return render(request, 'home.html', {'produtos': produtos})

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

@login_required
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'meus_pedidos.html', {'pedidos': pedidos})

# View para assinar um plano
@login_required
def assinar_plano(request):
    planos = PlanoAssinatura.objects.all()
    if request.method == "POST":
        plano_id = request.POST.get("plano")
        plano = get_object_or_404(PlanoAssinatura, id=plano_id)
        assinatura, created = Assinatura.objects.get_or_create(usuario=request.user)
        assinatura.plano = plano
        assinatura.ativo = True
        assinatura.save()
        return redirect("meu_perfil")
    return render(request, "assinatura/assinar.html", {"planos": planos})

# View para alterar assinatura
@login_required
def alterar_assinatura(request):
    assinatura = get_object_or_404(Assinatura, usuario=request.user)
    planos = PlanoAssinatura.objects.all()
    if request.method == "POST":
        plano_id = request.POST.get("plano")
        assinatura.plano = get_object_or_404(PlanoAssinatura, id=plano_id)
        assinatura.save()
        return redirect("meu_perfil")
    return render(request, "assinatura/alterar.html", {"assinatura": assinatura, "planos": planos})

# View para cancelar assinatura
@login_required
def cancelar_assinatura(request):
    assinatura = get_object_or_404(Assinatura, usuario=request.user)
    if request.method == "POST":
        assinatura.cancelar()
        return redirect("meu_perfil")
    return render(request, "assinatura/cancelar.html", {"assinatura": assinatura})

# View para exibir produtos da loja
@login_required
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "loja/lista.html", {"produtos": produtos})

# View para adicionar produto ao carrinho
@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
    carrinho.adicionar_produto(produto)
    return redirect("listar_produtos")

# View para remover produto do carrinho
@login_required
def remover_do_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho = get_object_or_404(Carrinho, usuario=request.user)
    carrinho.remover_produto(produto)
    return redirect("ver_carrinho")

# View para exibir o carrinho
@login_required
def ver_carrinho(request):
    carrinho, created = Carrinho.objects.get_or_create(usuario=request.user)
    return render(request, "loja/carrinho.html", {"carrinho": carrinho})

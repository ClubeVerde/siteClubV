from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Produto, Assinatura, Pedido, Carrinho, Plano
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from core.models import Usuario
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError



def home(request):
    produtos = Produto.objects.all()[:4]

    return render(request, 'home.html', {'produtos': produtos})


def cadastro(request):
    if request.method == "POST":
        try:
            nome = request.POST.get("nome")
            sobrenome = request.POST.get("sobrenome")
            telefone = request.POST.get("telefone")
            cpf = request.POST.get("cpf")
            email = request.POST.get("email")
            senha1 = request.POST.get("password1")
            senha2 = request.POST.get("password2")
            rua = request.POST.get("rua")
            numero = request.POST.get("numero")
            cep = request.POST.get("cep")
            bairro = request.POST.get("bairro")
            cidade = request.POST.get("cidade")
            estado = request.POST.get("estado")
            referencia = request.POST.get("referencia")

           
            if senha1 != senha2:
                messages.error(request, "As senhas não coincidem.")
                return render(request, "cadastro.html")

           
            usuario = Usuario.objects.create_user(
                username=email, 
                first_name=nome,
                last_name=sobrenome,
                email=email,
                password=senha1,
                telefone=telefone,
                cpf=cpf,
                rua=rua,
                numero=numero,
                cep=cep,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                referencia=referencia,
            )



            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect("login")

        except IntegrityError:
            messages.error(request, "Este email ou CPF já estão cadastrado.")
        except ValidationError as e: 
            messages.error(request, f"Erro ao criar usuário: {e}")


    return render(request, "cadastro.html")


def minha_pagina(request):
    
    pedidos = Pedido.objects.filter(usuario=request.user)
    assinaturas = Assinatura.objects.filter(usuario=request.user)
    
    return render(request, 'minha_pagina.html', {
        'pedidos': pedidos,
        'assinaturas': assinaturas,
    })


def alterar_informacoes(request):
    return render(request, 'alterar_informacoes.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Página de login carregada com sucesso!")
            return redirect("home")  
        else:
            messages.error(request, "Email ou senha incorretos. Tente novamente.")

    return render(request, "login.html", {'messages': messages.get_messages(request)})

def custom_logout(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect('home')

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos.html', {'produtos': produtos})


def lista_assinaturas(request):
    assinaturas = Assinatura.objects.all()
    return render(request, 'assinaturas.html', {'assinaturas': assinaturas})


def sobre_nos(request):
    return render(request, 'sobre_nos.html')


def loja(request):
    produtos = Produto.objects.all()  
    return render(request, 'loja.html', {'produtos': produtos})


def contato(request):
    return render(request, 'contato.html')



def carrinho(request):
    
    cart = request.session.get('carrinho', {})
    
    
    produtos_carrinho = []
    planos_carrinho = []
    
    
    for item_id, quantidade in cart.items():
    
        try:
            produto = Produto.objects.get(id=int(item_id))
            produtos_carrinho.append({
                'item': produto,
                'quantidade': quantidade,
            })
        except Produto.DoesNotExist:
    
            try:
                plano = Plano.objects.get(id=int(item_id))
                planos_carrinho.append({
                    'item': plano,
                    'quantidade': quantidade,
                })
            except Plano.DoesNotExist:
    
                continue

    context = {
        'produtos_carrinho': produtos_carrinho,
        'planos_carrinho': planos_carrinho,
    }
    return render(request, 'carrinho.html', context)

@login_required
def adicionar_carrinho_produto(request, id_produto):
    produto = get_object_or_404(Produto, id=id_produto)
    carrinho = request.session.get('carrinho', {})
    if str(id_produto) in carrinho:
        carrinho[str(id_produto)] += 1
    else:
        carrinho[str(id_produto)] = 1
    request.session['carrinho'] = carrinho
    messages.success(request, f"'{produto.nome}' foi adicionado ao carrinho!")
    return redirect('carrinho')

@login_required
def adicionar_carrinho_plano(request, id_plano):
    plano = get_object_or_404(Plano, id=id_plano)
    carrinho = request.session.get('carrinho', {})
    if str(id_plano) in carrinho:
        carrinho[str(id_plano)] += 1
    else:
        carrinho[str(id_plano)] = 1
    request.session['carrinho'] = carrinho
    messages.success(request, f"Plano '{plano.nome}' foi adicionado ao carrinho!")
    return redirect('carrinho')


def visualizar_carrinho(request):
    """
    Exibe os itens do carrinho e o total.
    """

    carrinho = request.session.get('carrinho', {})
    produtos_carrinho = []
    total = 0


    for id_produto, quantidade in carrinho.items():
        produto = Produto.objects.get(id=id_produto)
        subtotal = produto.preco * quantidade
        total += subtotal
        produtos_carrinho.append({
            'produto': produto,
            'quantidade': quantidade,
            'subtotal': subtotal
        })

    context = {
        'produtos_carrinho': produtos_carrinho,
        'total': total,
    }
    return render(request, 'carrinho.html', context)
 

def planos(request):
    planos = Plano.objects.all()
    return render(request, 'planos.html', {'planos': planos})

@login_required
def escolher_plano(request, plano_id):
    try:
        plano = Plano.objects.get(id=plano_id)
    except Plano.DoesNotExist:

        return redirect('planos')

    if request.method == 'POST':
      
        assinatura, created = Assinatura.objects.update_or_create(
            usuario=request.user,
            defaults={'plano': plano}
        )
        
        return redirect('minha_pagina')

    return render(request, 'escolher_plano.html', {'plano': plano})

@login_required
def adicionar_carrinho(request, plano_id):
    plano = Produto.objects.get(id=plano_id)
   
    if request.method == 'POST':
        carrinho = Carrinho(usuario=request.user, produto=plano)
        carrinho.save()
        return redirect('carrinho') 
    return render(request, 'carrinho.html', {'plano': plano})

@login_required
def finalizar_compra(request):
    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        messages.error(request, "Seu carrinho está vazio!")
        return redirect('carrinho')

    for item_id, quantidade in carrinho.items():
        try:
            produto = Produto.objects.get(id=int(item_id))
            Pedido.objects.create(
                usuario=request.user,
                produto=produto,
                assinatura=None,
                quantidade=quantidade,
                status=f"{produto.nome} - R$ {produto.preco:.2f}" 
            )
        except Produto.DoesNotExist:
            try:
                plano = Plano.objects.get(id=int(item_id))
                Pedido.objects.create(
                    usuario=request.user,
                    produto=None,  
                    assinatura=plano,
                    quantidade=1,
                    status=f"{plano.nome} - R$ {plano.preco:.2f}"  
                )
            except Plano.DoesNotExist:
                continue

    request.session['carrinho'] = {}

    messages.success(request, "Compra finalizada com sucesso!")
    return redirect('minha_pagina')    

def minha_view(request):
    storage = get_messages(request) 

    return render(request, 'minha_pagina.html', {'messages': storage})

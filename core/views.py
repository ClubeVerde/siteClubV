from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Produto, Assinatura, Pedido, Carrinho, Plano, Avaliacao
from .forms import AvaliacaoForm, CadastroForm, EditarPerfilForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from core.models import Usuario
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta


def home(request):
    produtos = Produto.objects.all()[:4]
    avaliacoes = Avaliacao.objects.all().order_by('-data')[:5]
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
    usuario = request.user
    pedidos = Pedido.objects.filter(usuario=request.user)
    assinatura = Assinatura.objects.filter(usuario=request.user).first()

    dias_restantes = None
    if assinatura and assinatura.data_expiracao:
        dias_restantes = (assinatura.data_expiracao - timezone.now().date()).days
    
    return render(request, 'minha_pagina.html', {
        'usuario': usuario,
        'pedidos': pedidos,
        'assinatura': assinatura,
        'dias_restantes': dias_restantes

    })
def verificar_senha(request):
    if request.method == "POST":
        senha_atual = request.POST.get("senha_atual")
        
        user = authenticate(username=request.user.username, password=senha_atual)

        if user is not None:
            return redirect('editar_perfil')
        else:
            messages.error(request, "Senha incorreta. Tente novamente.")
            return render(request, 'verificar_senha.html')

    return render(request, 'verificar_senha.html')

@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas com sucesso!")
            return redirect('minha_pagina')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})

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
    carrinho = request.session.get('carrinho', {})

    produtos_carrinho = []
    planos_carrinho = []

    for item_id, quantidade in carrinho.items():
        if str(item_id).startswith("plano_"):
            try:
                plano_id = int(item_id.replace("plano_", ""))
                plano = Plano.objects.get(id=plano_id)
                planos_carrinho.append({'item': plano, 'quantidade': quantidade})
            except Plano.DoesNotExist:
                continue
        else:
            try:
                produto = Produto.objects.get(id=int(item_id))
                produtos_carrinho.append({'item': produto, 'quantidade': quantidade})
            except Produto.DoesNotExist:
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
    
    key = f"plano_{id_plano}"
    if key in carrinho:
        carrinho[key] += 1
    else:
        carrinho[key] = 1

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
def finalizar_compra(request):
    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        messages.error(request, "Seu carrinho está vazio!")
        return redirect('carrinho')

    for item_id, quantidade in carrinho.items():
        if str(item_id).startswith("plano_"):
            try:
                plano_id = int(item_id.replace("plano_", ""))
                plano = Plano.objects.get(id=plano_id)
                
                assinatura, created = Assinatura.objects.update_or_create(
                    usuario=request.user,
                    defaults={
                        'plano': plano,
                        'status': 'ativa',
                        'preco': plano.preco,
                        'data_expiracao': timezone.now() + timedelta(days=30)
                    }
                )
            except Plano.DoesNotExist:
                continue
        else:
            try:
                produto = Produto.objects.get(id=int(item_id))
                Pedido.objects.create(
                    usuario=request.user,
                    produto=produto,
                    assinatura=None,
                    quantidade=quantidade,
                    status="pago"
                )
            except Produto.DoesNotExist:
                continue

    request.session['carrinho'] = {}
    messages.success(request, "Compra finalizada com sucesso!")
    return redirect('minha_pagina')

def minha_view(request):
    storage = get_messages(request) 

    return render(request, 'minha_pagina.html', {'messages': storage})

@login_required
def avaliar_compra(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    produto = pedido.produto

    if request.method == "POST":
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.usuario = request.user
            avaliacao.produto = produto
            avaliacao.save()
            messages.success(request, "Avaliação enviada com sucesso!")
            return redirect('minha_pagina')
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliar_compra.html', {'form': form, 'produto': produto})

@login_required
def cancelar_plano(request, assinatura_id, confirmacao=None):
    assinatura = get_object_or_404(Assinatura, id=assinatura_id, usuario=request.user)

    if confirmacao == "sim":
        if assinatura.status != 'cancelada':
            assinatura.status = 'cancelada'
            assinatura.save()
            messages.success(request, "Sua assinatura foi cancelada com sucesso!")
        else:
            messages.info(request, "A assinatura já está cancelada.")
    elif confirmacao == "nao":
        messages.info(request, "O cancelamento foi cancelado.")

    return redirect('minha_pagina') 

@login_required
def retomar_plano(request, assinatura_id, confirmacao=None):
    assinatura = get_object_or_404(Assinatura, id=assinatura_id, usuario=request.user)

    if confirmacao == "sim":
        if assinatura.status == 'cancelada':
            assinatura.status = 'ativa'
            assinatura.save()
            messages.success(request, "Sua assinatura foi reativada com sucesso!")
        else:
            messages.info(request, "A assinatura já está ativa.")
    elif confirmacao == "nao":
        messages.info(request, "O retomar da assinatura foi cancelado.")

    return redirect('minha_pagina')

@login_required
def confirmar_exclusao_conta(request):
    return render(request, 'confirmar_exclusao.html')

@login_required
def excluir_conta(request):
    user = request.user
    user.delete()
    messages.success(request, "Sua conta foi excluída com sucesso.")
    logout(request)
    return redirect('home')

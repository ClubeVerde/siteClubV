from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CadastroForm
from .models import Produto, Assinatura, Pedido, Carrinho, Plano
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from core.models import Usuario


def home(request):
    produtos = Produto.objects.all() 
    return render(request, 'home.html', {'produtos': produtos})

def cadastro(request):
    if request.method == "POST":
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

        # Verificar se o email já está em uso
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Este email já está cadastrado.")
            return render(request, "cadastro.html")

        # Validar se as senhas são iguais
        if senha1 != senha2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "cadastro.html")

        # Criar usuário
        try:
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

            # Realizar login automático
            login(request, usuario)
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect("minha_pagina")  # Redireciona para a página do cliente

        except ValidationError as e:
            messages.error(request, f"Erro ao criar usuário: {e}")
            return render(request, "cadastro.html")

    return render(request, "cadastro.html")

def minha_pagina(request):
    # Obtém os pedidos e assinaturas do usuário logado
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
            return redirect("home")  # Redireciona para a página inicial
        else:
            messages.error(request, "Email ou senha incorretos. Tente novamente.")  # ✅ Adiciona mensagem de erro

    return render(request, "login.html", {'messages': messages.get_messages(request)})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos.html', {'produtos': produtos})

def lista_assinaturas(request):
    assinaturas = Assinatura.objects.all()
    return render(request, 'assinaturas.html', {'assinaturas': assinaturas})

def sobre_nos(request):
    return render(request, 'sobre_nos.html')

def loja(request):
    produtos = Produto.objects.all()  # Certifique-se de que Produto é o seu modelo de produtos
    return render(request, 'loja.html', {'produtos': produtos})

def contato(request):
    return render(request, 'contato.html')

def carrinho(request):
    # Recupera o dicionário do carrinho da sessão
    cart = request.session.get('carrinho', {})
    
    # Inicializa listas para produtos e planos
    produtos_carrinho = []
    planos_carrinho = []
    
    # Itera pelos itens do carrinho
    for item_id, quantidade in cart.items():
        # Tenta obter como Produto
        try:
            produto = Produto.objects.get(id=int(item_id))
            produtos_carrinho.append({
                'item': produto,
                'quantidade': quantidade,
            })
        except Produto.DoesNotExist:
            # Se não encontrar como Produto, tenta como Plano
            try:
                plano = Plano.objects.get(id=int(item_id))
                planos_carrinho.append({
                    'item': plano,
                    'quantidade': quantidade,
                })
            except Plano.DoesNotExist:
                # Se não encontrar de nenhum dos dois, ignora o item
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
    # Obtém o carrinho da sessão
    carrinho = request.session.get('carrinho', {})
    produtos_carrinho = []
    total = 0

    # Para cada item (id_produto e quantidade) no carrinho, busca o produto no BD e calcula o subtotal
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

def criar_pedido(request, assinatura_id):
    # Recuperando a assinatura do usuário
    assinatura = get_object_or_404(Assinatura, id=assinatura_id)
    
    if assinatura.status == 'ativa':
        # Criar o pedido relacionado à assinatura
        pedido = Pedido.objects.create(
            usuario=request.user,
            assinatura=assinatura,
            status='pendente'
        )
        
        # Se necessário, altere o status da assinatura ao criar o pedido
        # Exemplo: Suspende a assinatura enquanto o pedido está em andamento
        assinatura.status = 'suspensa'
        assinatura.save()

        # Redireciona o usuário para a página do carrinho ou página de confirmação
        return redirect('carrinho')
    else:
        # Exibe uma mensagem de erro caso a assinatura não esteja ativa
        messages.error(request, 'Sua assinatura não está ativa. Não é possível fazer o pedido.')
        return redirect('minha_pagina')
def planos(request):
    planos = Plano.objects.all()  # Recuperando todos os planos
    return render(request, 'planos.html', {'planos': planos})

@login_required
def escolher_plano(request, plano_id):
    try:
        plano = Plano.objects.get(id=plano_id)
    except Plano.DoesNotExist:
        # Se o plano não existir, redireciona para a página de planos
        return redirect('planos')

    if request.method == 'POST':
        # Aqui, associamos o plano ao usuário, criando ou atualizando a assinatura
        assinatura, created = Assinatura.objects.update_or_create(
            usuario=request.user,
            defaults={'plano': plano}
        )
        # Redireciona para a página do usuário ou para onde você desejar após a escolha
        return redirect('minha_pagina')

    return render(request, 'escolher_plano.html', {'plano': plano})

@login_required
def adicionar_carrinho(request, plano_id):
    plano = Produto.objects.get(id=plano_id)  # Ou qualquer modelo relacionado a planos
    # Lógica para adicionar ao carrinho
    if request.method == 'POST':
        carrinho = Carrinho(usuario=request.user, produto=plano)
        carrinho.save()
        return redirect('carrinho')  # Redireciona para o carrinho ou outra página
    return render(request, 'carrinho.html', {'plano': plano})
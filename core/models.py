from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuario_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuario_permissions",
        blank=True
    )

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.TextField()
    telefone = models.CharField(max_length=15)
    cnpj = models.CharField(max_length=14, null=False, default='00000000000000')
    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    tamanho = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, null=True, blank=True)
    estoque = models.PositiveIntegerField(default=0)
    data_adicao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome

class Assinatura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    data_inicio = models.DateField(auto_now_add=True)
    data_expiracao = models.DateField()
    status = models.CharField(max_length=20, choices=[('ativa', 'Ativa'), ('suspensa', 'Suspensa'), ('cancelada', 'Cancelada')])

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', null=True, blank=True, on_delete=models.SET_NULL)
    assinatura = models.ForeignKey('Assinatura', null=True, blank=True, on_delete=models.SET_NULL)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado')
    ], default='pendente')

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username}'

class Avaliacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    comentario = models.TextField()
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_avaliacao = models.DateTimeField(auto_now_add=True)

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

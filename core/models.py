from django.db import models
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
    email = models.EmailField(unique=True)

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    tamanho = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    estoque = models.PositiveIntegerField(default=0)
    data_adicao = models.DateTimeField(auto_now_add=True)

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

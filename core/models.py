from django.db import models
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone


class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    rua = models.CharField(max_length=255, default="Desconhecido")
    numero = models.CharField(max_length=10, default="0")
    cep = models.CharField(max_length=10, default="00000-000")
    bairro = models.CharField(max_length=255, default="Desconhecido")
    cidade = models.CharField(max_length=100, default="Desconhecido")
    estado = models.CharField(max_length=50, default="Desconhecido")
    referencia = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        
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
    imagem = models.ImageField(upload_to='plantas/', null=True, blank=True) 
    def __str__(self):
        return self.nome

class Plano(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    descricao = models.TextField()

    def __str__(self):
        return self.nome
class Assinatura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    data_inicio = models.DateField(auto_now_add=True)
    data_expiracao = models.DateField()
    status = models.CharField(max_length=20, choices=[('ativa', 'Ativa'), ('suspensa', 'Suspensa'), ('cancelada', 'Cancelada')])

class Carrinho(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f'Carrinho de {self.usuario.username}'

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)
    assinatura = models.ForeignKey(Plano, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.PositiveIntegerField(default=1)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_expiracao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=[
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado')
    ], default='pendente')
    
    def salvar_pedido(self):
        if self.assinatura:
            self.data_expiracao = timezone.now() + timedelta(days=30)
        self.save()

    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username}'
    
class Avaliacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True, blank=True)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario} - Nota {self.nota}"
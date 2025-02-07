from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('', views.home, name='home'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('assinaturas/', views.lista_assinaturas, name='lista_assinaturas'),
    path('comprar/<int:produto_id>/', views.comprar_produto, name='comprar_produto'),
    path('assinar/<int:assinatura_id>/', views.assinar_plano, name='assinar_plano'),
    path('pedidos/', views.meus_pedidos, name='meus_pedidos'),
        # Rotas para Assinaturas
    path('assinatura/', views.assinar_plano, name='assinar_plano'),
    path('assinatura/alterar/', views.alterar_assinatura, name='alterar_assinatura'),
    path('assinatura/cancelar/', views.cancelar_assinatura, name='cancelar_assinatura'),
    
    # Rotas para Loja
    path('loja/', views.listar_produtos, name='listar_produtos'),
    path('loja/adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('loja/remover/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('loja/carrinho/', views.ver_carrinho, name='ver_carrinho'),
]

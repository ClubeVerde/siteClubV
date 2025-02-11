from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import adicionar_carrinho, visualizar_carrinho, escolher_plano

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('cadastro/', views.cadastro, name='cadastro'),
    path('', views.home, name='home'),
    path('sobre_nos/', views.sobre_nos, name='sobre_nos'),
    path('loja/', views.loja, name='loja'),
    path('contato/', views.contato, name='contato'),
    path('planos/', views.planos, name='planos'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('assinaturas/', views.lista_assinaturas, name='lista_assinaturas'),

    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar-carrinho/<int:id_produto>/', views.adicionar_carrinho_produto, name='adicionar_carrinho_produto'),
    path('adicionar-carrinho/plano/<int:id_plano>/', views.adicionar_carrinho_plano, name='adicionar_carrinho_plano'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),


    path('minha_pagina/', views.minha_pagina, name='minha_pagina'),
    path('alterar_informacoes/', views.alterar_informacoes, name='alterar_informacoes'),  # Adicione essa linha
    path("escolher-plano/<str:tipo>/", escolher_plano, name="escolher_plano"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

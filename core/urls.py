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
]

from django.contrib import admin
from .models import Plano, Usuario, Produto, Fornecedor

admin.site.register(Plano)
admin.site.register(Usuario)
admin.site.register(Produto)
admin.site.register(Fornecedor)
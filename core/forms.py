from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CadastroForm(UserCreationForm):
    cpf = forms.CharField(max_length=14)
    telefone = forms.CharField(max_length=15)
    endereco = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cpf', 'telefone', 'endereco', 'password1', 'password2']

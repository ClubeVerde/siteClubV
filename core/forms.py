from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Avaliacao

class CadastroForm(UserCreationForm):
    cpf = forms.CharField(max_length=14)
    telefone = forms.CharField(max_length=15)
    endereco = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cpf', 'telefone', 'endereco', 'password1', 'password2']

class EditarPerfilForm(forms.ModelForm):
    senha_atual = forms.CharField(widget=forms.PasswordInput(), label="Senha Atual")

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefone', 'cpf', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'referencia']

    def clean_senha_atual(self):
        senha_atual = self.cleaned_data.get('senha_atual')
        if not self.instance.check_password(senha_atual):
            raise forms.ValidationError("Senha atual incorreta.")
        return senha_atual

class AvaliacaoForm(forms.Form):
    comentario = forms.CharField(max_length=1000)
    
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
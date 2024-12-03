from views.application.models import Endereco, Cidade
from views.userAuth.models import DeactivateReason

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

Usuario = get_user_model()

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}),
    )
    password2 = forms.CharField(
        label="Confirme a Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}),
    )

    class Meta:
        model = Usuario
        fields = ['usuario', 'nome', 'email', 'telefone', 'is_motorista']
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu telefone'}),
            'is_motorista': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("nome")
        return name.title()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone and len(telefone) != 11:
            raise forms.ValidationError("O telefone deve conter exatamente 11 dígitos.")
        return telefone

    def clean_usuario(self):
        usuario_field = self.cleaned_data.get('usuario')
        if Usuario.objects.filter(usuario=usuario_field).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return usuario_field

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])  # Hash da senha
        if commit:
            user.save()
        return user

class EditUsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['usuario', 'nome', 'email', 'telefone', 'imagem']
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu telefone'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_name(self):
        name = self.cleaned_data.get("nome")
        return name.title()

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone and len(telefone) != 11:
            raise forms.ValidationError("O telefone deve conter exatamente 11 dígitos.")
        return telefone

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
        return user

class RemoveUsuarioReasonForm(forms.ModelForm):
    class Meta:
        model = DeactivateReason
        fields = ['choice_reason', 'reason']

class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())  

class AddressForm(forms.ModelForm):
    cidade = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua cidade'
        }),
        label="Cidade",
        required=True
    )

    class Meta:
        model = Endereco
        fields = ['rua', 'bairro', 'numero', 'cep', 'complemento']
        widgets = {
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da rua onde você reside'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o bairro onde você reside'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o número da sua casa'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CEP da sua rua'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite um ponto como referência', })
        }

    def clean_cidade(self):
        cidade_nome = self.cleaned_data['cidade']
        try:
            return Cidade.objects.get(nome=cidade_nome)
        except Cidade.DoesNotExist:
            raise forms.ValidationError("Cidade não encontrada. Verifique o nome digitado.")
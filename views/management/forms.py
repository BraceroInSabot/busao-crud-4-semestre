from django import forms
from .models import Campanha, Onibus, Rota

class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = [
            'titulo',
            'id_onibus',
            'prox_corrida',
        ]
        widgets = {
            'id_onibus': forms.Select(attrs={'class': 'form-control'}),
            'id_rota': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o título da campanha'}),
            'prox_corrida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'id_onibus': 'Ônibus',
            'id_rota': 'Rota',
            'titulo': 'Título',
            'prox_corrida': 'Próxima Corrida',
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 3:
            raise forms.ValidationError("O título deve ter pelo menos 3 caracteres.")
        return titulo


class OnibusForm(forms.ModelForm):
    class Meta:
        model = Onibus
        fields = [
            'nome',
            'imagem',
            'placa',
            'marca',
            'modelo',
            'ultima_manutencao',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do ônibus'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC1234'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o modelo'}),
            'ultima_manutencao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'nome': 'Nome do Ônibus',
            'imagem': 'Imagem do Ônibus',
            'placa': 'Placa',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'ultima_manutencao': 'Última Manutenção',
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if len(placa) != 7:
            raise forms.ValidationError("A placa deve conter exatamente 7 caracteres alfanuméricos.")
        return placa

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome.strip()) < 3:
            raise forms.ValidationError("O nome deve conter pelo menos 3 caracteres.")
        return nome


class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = [ 'id_rota_comeco', 'id_rota_final']
        labels = {
            'id_rota_comeco': 'Início da Rota',
            'id_rota_final': 'Final da Rota',
            
        }
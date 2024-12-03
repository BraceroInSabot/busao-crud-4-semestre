from views.application.models import Cidade

from django.db import models
from django.contrib.auth import get_user_model
import hashlib
from django.utils.timezone import now
import os

User = get_user_model()

def bus_image_upload_path(instance, filename):
        """
        Gera um caminho único para salvar a imagem do usuário.
        """
        # Gera o hash do nome do arquivo usando o horário atual e o ID do usuário
        timestamp = now().strftime('%Y%m%d%H%M%S')
        file_hash = hashlib.sha256(f"{instance.id}_{timestamp}".encode()).hexdigest()[:10]
        ext = filename.split('.')[-1]  # Mantém a extensão original
        return os.path.join('userImage', f"{file_hash}.{ext}")

class Onibus(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='CodigoOnibus')
    nome = models.TextField(max_length=150, blank=False, null=False, verbose_name='NomeOnibus')
    imagem = models.ImageField(default='busDefault/bus.jpg', upload_to=bus_image_upload_path, verbose_name='Imagem')
    placa = models.CharField(max_length=7, blank=False, null=False, verbose_name='Placa')
    marca = models.TextField(max_length=75, blank=True, null=True, verbose_name='Marca')
    modelo = models.TextField(max_length=75, blank=True, null=True, verbose_name='Modelo')
    ultima_manutencao = models.DateField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='CriadoPor')

    class Meta:
        db_table = "Onibus"
        
    def __str__(self):
        return self.nome

class Campanha(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='CodigoCampanha')
    id_onibus = models.ForeignKey(Onibus, blank=False, null=True, on_delete=models.CASCADE, verbose_name='CodigoOnibus')
    titulo = models.TextField(max_length=150, blank=False, null=False, verbose_name='Titulo')
    data_criacao = models.DateField(auto_now=True, verbose_name='DataCriacao')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='CodigoCriador')
    prox_corrida = models.DateField(verbose_name='DataProximaCorrida')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        db_table = "Campanha"
        
    def __str__(self):
        return self.titulo

class Rota(models.Model):
    id_rota = models.AutoField(primary_key=True, verbose_name='CodigoRota')
    id_campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, verbose_name='CodigoCampanha')
    id_rota_comeco = models.ForeignKey(Cidade, related_name='rota_comeco', on_delete=models.CASCADE, verbose_name="RotaInicio")
    id_rota_final = models.ForeignKey(Cidade, related_name='rota_final', on_delete=models.CASCADE, verbose_name="RotaFinal")

    class Meta:
        db_table = "Rota"
        
    def __str__(self):
        return f"{self.id_rota_comeco} ---> {self.id_rota_final}"
    
class Administrador(models.Model):
    ROLE_CHOICES = [
        ("ADM", "Administrador da Equipe"),
        ("MT", "Motorista"),
        ("AUX", "Auxiliar"),
    ]

    id_administrador = models.AutoField(primary_key=True, verbose_name='CodigoAdministrador')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='CodigoUsuario')
    id_campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, verbose_name='CodigoCampanha')
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, verbose_name="Função")


    class Meta:
        db_table = 'Administrador'

    def __str__(self):
        return f"{self.id_usuario.nome}"

class Passageiro(models.Model):
    id_administrador = models.AutoField(primary_key=True, verbose_name='CodigoAdministrador')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='CodigoUsuario')
    id_campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, verbose_name='CodigoCampanha')

    class Meta:
        db_table = 'Passageiro'

    def __str__(self):
        return f"{self.id_usuario.nome}"
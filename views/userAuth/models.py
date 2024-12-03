from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from views.application.models import Endereco
import hashlib
from django.utils.timezone import now
import os

def user_image_upload_path(instance, filename):
        """
        Gera um caminho único para salvar a imagem do usuário.
        """
        # Gera o hash do nome do arquivo usando o horário atual e o ID do usuário
        timestamp = now().strftime('%Y%m%d%H%M%S')
        file_hash = hashlib.sha256(f"{instance.id}_{timestamp}".encode()).hexdigest()[:10]
        ext = filename.split('.')[-1]  # Mantém a extensão original
        return os.path.join('userImage', f"{file_hash}.{ext}")

class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None

    imagem = models.ImageField(default='userDefault/user.png', upload_to=user_image_upload_path)
    id = models.AutoField(primary_key=True, verbose_name="Código Interno")
    usuario = models.CharField(max_length=150, unique=True, verbose_name="Nome de Usuário")
    nome = models.CharField(max_length=255, verbose_name='Nome Completo')
    telefone = models.CharField(max_length=11, null=True, verbose_name='Telefone')
    is_motorista = models.BooleanField(default=False, verbose_name='Motorista?')
    endereco = models.ForeignKey(Endereco, unique=False, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Endereço")

    USERNAME_FIELD = 'usuario'

    class Meta:
        db_table = "Usuario"
        
    def __str__(self):
        return self.nome
    
    def delete_image(self):
        """
        Exclui a imagem atual do usuário ao atualizar ou deletar.
        """
        if self.imagem:
            self.imagem.delete(save=False)


class DeactivateReason(models.Model):
    codigo = models.AutoField(primary_key=True, verbose_name="CodigoDesativacao")
    choice_reason = models.CharField(max_length=2, choices={
          "NG": "Não gostei do Sistema",
          "MG": "Estou mudando de sistema",
          "ER": "Muitos erros",
          "OU": "Outros motivos..."
     }, verbose_name="Campo de Escolha")
    reason = models.TextField(max_length=255, null=True, blank=True, verbose_name="Motivo da desativação do Usuário")
    
    class Meta:
        db_table = "Desativacao"
        
    def __str__(self):
        return self.choice_reason
    
    
class Usuario_Desativacao(models.Model):
    codigo = models.AutoField(primary_key=True, verbose_name="CodigoUsuarioDesativacao")
    codigousuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='CodigoUsuario')
    codigodesativacao = models.ForeignKey(DeactivateReason, on_delete=models.CASCADE, verbose_name='CodigoDesativacao')
    data = models.DateField(auto_now=True, auto_created=True, verbose_name='Data Realizada')

    class Meta:
        db_table = "Usuario_Desativacao"

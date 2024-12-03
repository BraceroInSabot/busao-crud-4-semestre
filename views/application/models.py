from django.db import models

# class Onibus(models.Model):
#     # Chave primária
#     id_onibus = models.IntegerField(verbose_name="CodigoOnibus", primary_key=True, serialize=True, null=False)

#     # Campo de muitos para muitos
#     lista_passageiros = models.ManyToManyField('Passageiro', verbose_name="Codigo")
#     lista_motoristas = models.ManyToManyField('Motorista', verbose_name="ListaMotoristas")

#     # Campos de um para muitos
#     lista_administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE, verbose_name="Administrador")
#     lista_rotas = models.ForeignKey('Rota', on_delete=models.CASCADE, verbose_name="Rotas")

#     # Nome do ônibus
#     nome_onibus = models.CharField(verbose_name="NomeOnibus", max_length=255)

#     def __str__(self):
#         """Retorna o nome do ônibus em questão ao chamar o objeto.

#         Returns:
#             STR: Nome do ônibus
#         """
#         return self.nome_onibus
    
class Estado(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Estado')
    sigla = models.CharField(max_length=2, verbose_name='Sigla')
    codigo_uf_importacao = models.IntegerField(blank=True, null=True, verbose_name='CodigoImportacao')

    class Meta:
        db_table = "Estado"

    def __str__(self):
        return f'{self.nome} [{self.sigla}]'

class Cidade(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Cidade')
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='cidades')

    class Meta:
        db_table = "Cidade"
        
    def __str__(self):
        return f'{self.nome} / {self.estado.sigla}'

class Endereco(models.Model):
    rua = models.CharField(max_length=255, verbose_name='Rua')
    bairro = models.CharField(max_length=255, verbose_name='Bairro')
    numero = models.CharField(max_length=10, verbose_name='Número')
    cep = models.CharField(max_length=10, verbose_name='CEP')
    complemento = models.CharField(max_length=255, blank=True, null=True, verbose_name='Complemento')
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='enderecos')

    class Meta:
        db_table = "Endereco"
        
    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro} - {self.cidade}"


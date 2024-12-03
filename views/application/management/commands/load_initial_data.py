import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from views.application.models import Estado, Cidade  # Substitua pelo nome do seu app

class Command(BaseCommand):
    help = "Carrega dados iniciais de estados e cidades a partir de arquivos JSON."

    def handle(self, *args, **kwargs):
        try:
            # Define os caminhos absolutos para os arquivos JSON
            estados_path = os.path.join(settings.BASE_DIR, "static/json", "estados.json")
            municipios_path = os.path.join(settings.BASE_DIR, "static/json", "municipios.json")

            # Carregar dados de estados
            with open(estados_path, "r", encoding="utf-8-sig") as estados_file:
                estados_data = json.load(estados_file)
                for estado in estados_data:
                    obj, created = Estado.objects.get_or_create(
                        nome=estado["nome"],
                        sigla=estado["uf"],
                        codigo_uf_importacao=estado['codigo_uf']
                    )
                    if created:
                        self.stdout.write(f"Estado {obj.nome} criado com sucesso.")

            # Carregar dados de municípios
            with open(municipios_path, "r", encoding="utf-8-sig") as municipios_file:
                municipios_data = json.load(municipios_file)
                for municipio in municipios_data:
                    estado = Estado.objects.filter(codigo_uf_importacao=municipio["codigo_uf"]).first()
                    if estado:
                        obj, created = Cidade.objects.get_or_create(
                            nome=municipio["nome"],
                            estado=estado,
                        )
                        if created:
                            self.stdout.write(f"Cidade {obj.nome} criada com sucesso.")
                    else:
                        self.stderr.write(f"Estado com código {municipio['codigo_uf']} não encontrado.")
        
            self.stdout.write(self.style.SUCCESS("Dados iniciais carregados com sucesso!"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao carregar dados: {e}"))

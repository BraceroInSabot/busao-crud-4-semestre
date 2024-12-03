import json

ARQUIVO_ESTADO = 'static/json/estados.json'
ARQUIVO_MUNICIPIO = 'static/json/municipios.json'
GET_ESTADO = {}
GET_CIDADE = {}

def estado_convert():
    with open(ARQUIVO_ESTADO, 'r', encoding='utf-8') as f:
        dados = json.load(f)

        print(dados)

estado_convert()
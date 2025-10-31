import json

try:
    with open('codigos/pistas.json', 'r', encoding='utf-8') as f:
        TEXTOS = json.load(f)
    print(f"Arquivo 'pistas.json' carregado com sucesso.")
except FileNotFoundError:
    print(f"ERRO CRITICO [pistas.py]: Arquivo 'pistas.json' nao encontrado no caminho!")
    TEXTOS = {} # Define um dicionario vazio para evitar que o resto quebre
except json.JSONDecodeError:
    print(f"ERRO CRITICO [pistas.py]: 'pistas.json' contem um erro de sintaxe (JSON invalido)!")
    TEXTOS = {}

print(TEXTOS)
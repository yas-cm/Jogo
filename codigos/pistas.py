# -*- coding: utf-8 -*-
import json
import random
from classes import *
try:
    with open('pistas.json', 'r', encoding='utf-8') as f:
        TEXTOS = json.load(f)
    print("Debug [pistas.py]: Arquivo 'pistas.json' carregado com sucesso.")
except FileNotFoundError:
    print("ERRO CRITICO [pistas.py]: Arquivo 'pistas.json' nao encontrado!")
    TEXTOS = {} # Define um dicionario vazio para evitar que o resto quebre
except json.JSONDecodeError:
    print("ERRO CRITICO [pistas.py]: 'pistas.json' contem um erro de sintaxe (JSON invalido)!")
    TEXTOS = {}

PAPEIS_PARA_PISTAS = [
    Cidadao("").papel,
    Lobisomem("").papel, 
    Medico("").papel, 
    Vidente("").papel, 
    Bruxa("").papel, 
    Pistoleiro("").papel
]

EQUIPES_PARA_PISTAS = ["Inocente", "Ameaca", "Neutro"]

def gerar_pista(jogo, rodada):
    
    vivos = [j for j in jogo.jogadores if j.esta_vivo]
    
    # 4. Debug (Para sabermos que funcionou)
    print(f"Debug [pistas.py]: Filtro OK. {len(vivos)} jogadores vivos encontrados.")
    
    # 5. Placeholder (Até implementarmos a lógica real)
    placeholder = "(Uma nova pista sera gerada aqui na proxima etapa...)"
    
    return placeholder
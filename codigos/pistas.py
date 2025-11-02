# -*- coding: utf-8 -*-
import json
import random
import textwrap
import time
from classes import *

try:
    # --- Mantido (presume que 'codigos/pistas.json' é o caminho certo) ---
    with open('codigos/pistas.json', 'r', encoding='utf-8') as f:
        TEXTOS = json.load(f)
    # Mensagem de debug removida
except FileNotFoundError:
    print(f"ERRO CRITICO [pistas.py]: Arquivo 'pistas.json' nao encontrado no caminho!")
    TEXTOS = {} 
except json.JSONDecodeError:
    print(f"ERRO CRITICO [pistas.py]: 'pistas.json' contem um erro de sintaxe (JSON invalido)!")
    TEXTOS = {}

PAPEIS_PARA_PISTAS = [
    Lobisomem("").papel,    
    Medico("").papel,       
    Vidente("").papel,      
    Bruxa("").papel,        
    Pistoleiro("").papel,
    Cidadao("").papel
]

EQUIPES_PARA_PISTAS = ["Inocente", "Ameaca", "Neutro"]

anotacoes = {}

def formatar_paragrafo(texto):
    """
    Imprime o texto formatado (largura 80) letra por letra.
    Isso é o que exibe as "Informações coletadas" na tela.
    """
    texto_formatado = textwrap.fill(texto, width=80, replace_whitespace=False)
    for letra in texto_formatado:
        print(letra, end='', flush=True) 
        time.sleep(0.05)
    print()

def _obter_objs_aleatorios(lista_vivos_obj, qtd=1):
    if len(lista_vivos_obj) < qtd:
        return None
    sorteados_obj = random.sample(lista_vivos_obj, qtd)
    return sorteados_obj

def obter_personagens_aleatorios(lista_vivos_obj, qtd=1):
    objetos = _obter_objs_aleatorios(lista_vivos_obj, qtd)
    if objetos:
        return [personagem.nome for personagem in objetos]
    return None

def obter_papel_aleatorio(excluir=[]):
    papeis_disponiveis = [p for p in PAPEIS_PARA_PISTAS if p not in excluir]
    if not papeis_disponiveis:
        return random.choice(PAPEIS_PARA_PISTAS) # Fallback
    return random.choice(papeis_disponiveis)

def obter_equipe_aleatoria(excluir=[]):
    equipes_disponiveis = [e for e in EQUIPES_PARA_PISTAS if e not in excluir]
    if not equipes_disponiveis:
        return random.choice(EQUIPES_PARA_PISTAS) # Fallback
    return random.choice(equipes_disponiveis)

def _obter_pistas_fatos(eventos):
    pistas_fatos = []
    
    # --- Mortes ---
    if eventos["mortos"]:
        for info_morte in eventos["mortos"]:
            pessoa_morta = info_morte["pessoa"]
            causa_morte = info_morte["causa"]
            
            pista_m = TEXTOS["fatos"]["morte"].format(pessoa=pessoa_morta)
            pistas_fatos.append(pista_m)
            formatar_paragrafo(pista_m)
            
            pista_c = TEXTOS["fatos"]["causa_morte"].format(pessoa=pessoa_morta, causa=causa_morte)
            pistas_fatos.append(pista_c)
            formatar_paragrafo(pista_c)

    # --- Sobreviventes ---
    if eventos["sobreviventes"]:
        for nome_sobrevivente in eventos["sobreviventes"]:
            pista = TEXTOS["fatos"]["sobreviveu"].format(pessoa=nome_sobrevivente)
            pistas_fatos.append(pista)
            formatar_paragrafo(pista)
    
    # --- Revelação do Pistoleiro ---
    if eventos["eventos_pistoleiro"]:
        for pista in eventos["eventos_pistoleiro"]:
            pistas_fatos.append(pista)
            formatar_paragrafo(pista)
            
    if not eventos["mortos"] and not eventos["sobreviventes"]:
        pista = TEXTOS["fatos"]["sem_mortes"]
        pistas_fatos.append(pista)
        formatar_paragrafo(pista)

    return pistas_fatos

def _obter_pistas_eventos(eventos):
    pistas_eventos = []

    # --- Visão da Vidente ---
    if eventos["pistas_vidente"]:
        for pista in eventos["pistas_vidente"]:
            pistas_eventos.append(pista)
            formatar_paragrafo(pista)

    # --- Uso da Bruxa ---
    if eventos["eventos_bruxa"]:
        pista = TEXTOS["pistas_eventos"]["bruxa_uso"]
        pistas_eventos.append(pista)
        formatar_paragrafo(pista)
        
    return pistas_eventos

def _gerar_pistas_logicas(personagens_vivos_obj, rodada, qtd=4):
    pistas_logicas = []
    
    tipos_disponiveis = list(TEXTOS["pistas_logicas"].keys())
    
    tentativas = 0
    while len(pistas_logicas) < qtd and tentativas < 10: 
        tentativas += 1
        pista_gerada = None
        tipo_sorteado = random.choice(tipos_disponiveis)
        
        try:
            # --- TIPO 1: (P1 ou P2 é Papel) ---
            if tipo_sorteado == "tipo1_disj_simples" and len(personagens_vivos_obj) >= 2:
                jogadores = _obter_objs_aleatorios(personagens_vivos_obj, 2)
                if jogadores:
                    papel_real = jogadores[0].papel
                    nomes = [jogadores[0].nome, jogadores[1].nome]
                    random.shuffle(nomes)
                    
                    pista_gerada = TEXTOS["pistas_logicas"]["tipo1_disj_simples"].format(p1=nomes[0], p2=nomes[1], papel=papel_real)
            
            # --- TIPO 2: (P1 ou P2 ou P3 é Papel) ---
            elif tipo_sorteado == "tipo2_disj_tripla" and len(personagens_vivos_obj) >= 3:
                jogadores = _obter_objs_aleatorios(personagens_vivos_obj, 3)
                if jogadores:
                    papel_real = jogadores[0].papel 
                    nomes = [jogadores[0].nome, jogadores[1].nome, jogadores[2].nome]
                    random.shuffle(nomes) 
                    
                    pista_gerada = TEXTOS["pistas_logicas"]["tipo2_disj_tripla"].format(p1=nomes[0], p2=nomes[1], p3=nomes[2], papel=papel_real)
            
            # --- TIPO 3: (P1 NÃO é Papel) ---
            elif tipo_sorteado == "tipo3_negacao" and len(personagens_vivos_obj) >= 1:
                jogador = _obter_objs_aleatorios(personagens_vivos_obj, 1)
                if jogador:
                    jogador = jogador[0]
                    papel_real = jogador.papel
                    
                    papel_falso = obter_papel_aleatorio(excluir=[papel_real, "Lobisomem"])
                        
                    pista_gerada = TEXTOS["pistas_logicas"]["tipo3_negacao"].format(p1=jogador.nome, papel=papel_falso)

            # --- TIPO 4: (P1 é da Equipe X) ---
            elif tipo_sorteado == "tipo4_afirm_equipe" and len(personagens_vivos_obj) >= 1:
                jogador = _obter_objs_aleatorios(personagens_vivos_obj, 1)
                if jogador:
                    jogador = jogador[0]
                    
                    if rodada == 1 and isinstance(jogador, Lobisomem):
                        pass # Impede que a pista revele o Lobo na Rodada 1
                    else:
                        equipe_real = jogador.equipe
                        pista_gerada = TEXTOS["pistas_logicas"]["tipo4_afirm_equipe"].format(p1=jogador.nome, equipe=equipe_real)
            
            # --- TIPO 5: (Se P1 é Papel1, então P2 é Papel2) ---
            elif tipo_sorteado == "tipo5_cond_simples" and len(personagens_vivos_obj) >= 2:
                jogadores = _obter_objs_aleatorios(personagens_vivos_obj, 2)
                if jogadores:
                    p1 = jogadores[0]
                    p2 = jogadores[1]
                    
                    # Usa os papéis reais de P1 e P2 para criar uma pista (True -> True)
                    papel1_real = p1.papel
                    papel2_real = p2.papel
                    
                    pista_gerada = TEXTOS["pistas_logicas"]["tipo5_cond_simples"].format(
                        p1=p1.nome, papel1=papel1_real, 
                        p2=p2.nome, papel2=papel2_real
                    )

            # --- TIPO 6: (Se P1 é Papel1, então P2 NÃO é Papel_falso) ---
            elif tipo_sorteado == "tipo6_cond_negacao" and len(personagens_vivos_obj) >= 2:
                jogadores = _obter_objs_aleatorios(personagens_vivos_obj, 2)
                if jogadores:
                    p1 = jogadores[0]
                    p2 = jogadores[1]
                    
                    # Usa o papel real de P1
                    papel1_real = p1.papel
                    # Pega um papel que P2 realmente NÃO é
                    papel_falso_para_p2 = obter_papel_aleatorio(excluir=[p2.papel, "Lobisomem"])
                    
                    pista_gerada = TEXTOS["pistas_logicas"]["tipo6_cond_negacao"].format(
                        p1=p1.nome, papel1=papel1_real, 
                        p2=p2.nome, papel_falso=papel_falso_para_p2
                    )

            # --- TIPO 7: (Se P1 é Equipe1 E P2 é Equipe2, então P3 é Papel) ---
            elif tipo_sorteado == "tipo7_cond_composta" and len(personagens_vivos_obj) >= 3:
                jogadores = _obter_objs_aleatorios(personagens_vivos_obj, 3)
                if jogadores:
                    p1 = jogadores[0]
                    p2 = jogadores[1]
                    p3 = jogadores[2]
                    
                    # Usa as equipes e papéis reais dos jogadores
                    equipe1_real = p1.equipe
                    equipe2_real = p2.equipe
                    papel_real_p3 = p3.papel
                    
                    pista_gerada = TEXTOS["pistas_logicas"]["tipo7_cond_composta"].format(
                        p1=p1.nome, equipe1=equipe1_real,
                        p2=p2.nome, equipe2=equipe2_real,
                        p3=p3.nome, papel=papel_real_p3
                    )

            if pista_gerada and pista_gerada not in pistas_logicas:
                pistas_logicas.append(pista_gerada)
                formatar_paragrafo(pista_gerada)

        except Exception as e:
            print(f"Erro ao gerar pista logica '{tipo_sorteado}': {e}")
            
    return pistas_logicas

def _gerar_pistas_ruido(personagens_vivos_obj):
    qtd = random.randint(0,2)
    pistas_ruido = []
    
    tipos_disponiveis = list(TEXTOS["ruido"].keys())
    
    for _ in range(qtd):
        pista_gerada = None
        tipo_sorteado = random.choice(tipos_disponiveis)
        
        try:
            if tipo_sorteado in ["clima", "testemunha_vulto", "locais_corpo"]:
                pista_gerada = random.choice(TEXTOS["ruido"][tipo_sorteado])
            
            elif tipo_sorteado == "pessoa_abalada" and len(personagens_vivos_obj) >= 1:
                template_ruido = random.choice(TEXTOS["ruido"]["pessoa_abalada"])
                
                if "{outra_pessoa_viva}" in template_ruido and len(personagens_vivos_obj) >= 2:
                    nomes = obter_personagens_aleatorios(personagens_vivos_obj, 2)
                    if nomes:
                        pista_gerada = template_ruido.format(pessoa_viva=nomes[0], outra_pessoa_viva=nomes[1])
                elif "{pessoa_viva}" in template_ruido:
                     nomes = obter_personagens_aleatorios(personagens_vivos_obj, 1)
                     if nomes:
                        pista_gerada = template_ruido.format(pessoa_viva=nomes[0])
            
            elif tipo_sorteado == "template_objeto":
                objeto_sorteado = random.choice(TEXTOS["ruido"]["objetos_ruido"])
                pista_gerada = TEXTOS["ruido"]["template_objeto"].format(objeto=objeto_sorteado)
            
            if pista_gerada:
                 pistas_ruido.append(pista_gerada)
                 formatar_paragrafo(pista_gerada)
        
        except Exception as e:
            print(f"Erro ao gerar pista de ruido '{tipo_sorteado}': {e}")
             
    return pistas_ruido

def gerar_pista(jogo_obj, rodada):
    
    eventos = jogo_obj.eventos_noite 
    vivos_obj = [j for j in jogo_obj.jogadores if j.esta_vivo] 
    
    qtd_logicas = 3
    
    # A função formatar_paragrafo() é chamada DENTRO de cada uma dessas funções
    pistas_fatos = _obter_pistas_fatos(eventos) 
    pistas_eventos = _obter_pistas_eventos(eventos)
    pistas_logicas = _gerar_pistas_logicas(vivos_obj, rodada, qtd_logicas)
    pistas_ruido = _gerar_pistas_ruido(vivos_obj)
    
    todas_pistas = pistas_fatos + pistas_eventos + pistas_logicas + pistas_ruido
    
    if not todas_pistas:
        # Fallback caso nada aconteça
        formatar_paragrafo("A noite foi surpreendentemente calma. Nenhuma pista foi encontrada.")
        
    # Salva tudo no diário
    anotacoes[rodada] = "\n".join(f"• {p}" for p in todas_pistas)
# -*- coding: utf-8 -*-
import random
from classes import *
import time # Usado apenas no __main__
from pistas import TEXTOS 

# Importa a interface que acabamos de criar
import interface as ui

class Jogo:
    def __init__(self):
        
        self.nomes = ["Maria", "Isabella", "Angelina", "Diego", "Carlos", "Victor", "Guilherme"]
        
        self.papeis_da_partida = [] 
        self.jogadores = []         

        self._definir_papeis_partida()
        self.distribui_papeis()
        self.eventos_noite = {}

    def _definir_papeis_partida(self): 
        base_garantida = [Lobisomem, Medico, Cidadao, Cidadao] 
        pool_extra = [Medico, Cidadao, Vidente, Bruxa, Pistoleiro]
        random.shuffle(pool_extra)
        papeis_sorteados_extra = pool_extra[:3]
        self.papeis_da_partida = base_garantida + papeis_sorteados_extra
        nomes_papeis = [p.__name__ for p in self.papeis_da_partida]

    def distribui_papeis(self):
        papeis_embaralhados = self.papeis_da_partida[:] 
        random.shuffle(papeis_embaralhados)
        for nome_personagem, classe_papel in zip(self.nomes, papeis_embaralhados):     
            jogador_objeto = classe_papel(nome_personagem)
            self.jogadores.append(jogador_objeto)

    def simular_noite(self, rodada):
        
        self.eventos_noite = {
            "mortos": [], "sobreviventes": [], "pistas_vidente": [],
            "eventos_bruxa": [], "eventos_pistoleiro": [],
        }
        
        vivos = [j for j in self.jogadores if j.esta_vivo]
        
        lobo = None
        medico = None
        vidente = None
        bruxa = None
        pistoleiro = None
        
        for j in vivos:
            if isinstance(j, Lobisomem): lobo = j
            elif isinstance(j, Medico): medico = j
            elif isinstance(j, Vidente): vidente = j
            elif isinstance(j, Bruxa): bruxa = j
            elif isinstance(j, Pistoleiro): pistoleiro = j
        
        alvo_lobo = None
        alvo_medico = None
        alvo_vidente_obj = None
        alvo_bruxa_veneno = None
        cura_bruxa = False
        alvo_pistoleiro = None
        ataques_da_noite = {}

        # --- Ação do Lobo ---
        if lobo:
            alvos_possiveis = [j for j in vivos if j != lobo]
            if alvos_possiveis:
                alvo_lobo = lobo.matar(random.choice(alvos_possiveis))
                if alvo_lobo:
                    ataques_da_noite[alvo_lobo] = "Ataque de Lobisomem"

        # --- Ação do Médico ---
        if medico:
            alvos_possiveis = vivos[:] 
            if alvos_possiveis:
                alvo_medico = medico.salvar(random.choice(alvos_possiveis))

        # --- Ação da Vidente ---
        if vidente:
            alvos_possiveis = [j for j in vivos if j != vidente]
            if rodada == 1:
                alvos_possiveis = [j for j in alvos_possiveis if not isinstance(j, Lobisomem)]
            if alvos_possiveis:
                alvo_vidente_obj = random.choice(alvos_possiveis)
                info_vidente = vidente.investigar(alvo_vidente_obj) 
                
                if random.random() < 0.75: 
                    if info_vidente == "Lobisomem":
                        pista = TEXTOS["pistas_eventos"]["vidente_equipe"].format(pessoa=alvo_vidente_obj.nome, equipe="Ameaça")
                    elif info_vidente == "Pistoleiro" or info_vidente == "Bruxa":
                        pista = TEXTOS["pistas_eventos"]["vidente_equipe"].format(pessoa=alvo_vidente_obj.nome, equipe="Neutro")
                    else:
                        pista = TEXTOS["pistas_eventos"]["vidente_equipe"].format(pessoa=alvo_vidente_obj.nome, equipe="Inocente")
                else:
                    pista = TEXTOS["pistas_eventos"]["vidente_papel"].format(pessoa=alvo_vidente_obj.nome, papel=info_vidente)

                self.eventos_noite["pistas_vidente"].append(pista)

        # --- Ação da Bruxa ---            
        if bruxa:
            chance = random.random()
            if chance < 0.25 and bruxa.pocao_cura:
                cura_bruxa = bruxa.usar_cura()
                if cura_bruxa:
                    self.eventos_noite["eventos_bruxa"].append("cura")
            elif chance > 0.25 and chance < 0.50 and bruxa.pocao_veneno:
                alvos_possiveis = [j for j in vivos if j != bruxa]
                if rodada == 1:
                    alvos_possiveis = [j for j in alvos_possiveis if not isinstance(j, Lobisomem)]
                if alvos_possiveis:
                    alvo_escolhido = random.choice(alvos_possiveis)
                    alvo_bruxa_veneno = bruxa.usar_veneno(alvo_escolhido)
                    if alvo_bruxa_veneno:
                        ataques_da_noite[alvo_bruxa_veneno] = "Envenenamento"
                        self.eventos_noite["eventos_bruxa"].append("veneno")
                        
                        
        # --- Ação do Pistoleiro ---
        if pistoleiro and pistoleiro.balas > 0:
            if random.random() < 0.50: 
                alvos_possiveis = [j for j in vivos if j != pistoleiro]
                if alvos_possiveis:
                    alvo_escolhido = random.choice(alvos_possiveis)
                    alvo_pistoleiro = pistoleiro.atirar(alvo_escolhido)
                    if alvo_pistoleiro:
                        ataques_da_noite[alvo_pistoleiro] = "Tiro (Pistoleiro)"
                        pista_pistoleiro = TEXTOS["fatos"]["pistoleiro_revelado"].format(pessoa=pistoleiro.nome)
                        self.eventos_noite["eventos_pistoleiro"].append(pista_pistoleiro)


        # --- Resolução de Conflitos ---
        salvos_pelo_medico = set()
        if alvo_medico:
            salvos_pelo_medico.add(alvo_medico)

        for alvo_obj, causa_da_morte in ataques_da_noite.items():
            personagem_salvo = False
            if alvo_obj in salvos_pelo_medico:
                self.eventos_noite["sobreviventes"].append(alvo_obj.nome)
                personagem_salvo = True
            if cura_bruxa:
                if not personagem_salvo: 
                    self.eventos_noite["sobreviventes"].append(alvo_obj.nome)
                personagem_salvo = True

            if not personagem_salvo:
                alvo_obj.morrer()
                info_morte = {"pessoa": alvo_obj.nome, "causa": causa_da_morte}
                self.eventos_noite["mortos"].append(info_morte)


# =============================================================
# PONTO DE ENTRADA DO JOGO
# =============================================================

if __name__ == "__main__":
    
    ui.introducao() 
    
    while True:
        resultado = ui.rodar_partida(Jogo) 
        
        if resultado == "SAIR":
            break
        
        ui.limpar_tela()
        print(ui.ROXO + "Reiniciando uma nova investigação..." + ui.RESETAR)
        time.sleep(2)

    print("\nObrigado por jogar Wolvesville! Até a próxima.")
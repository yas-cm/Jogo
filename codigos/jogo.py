# -*- coding: utf-8 -*-
import random
from classes import *
import textwrap
import time
import sys
LARGURA_MAXIMA = 80

PRETO = "\033[30m"
VERMELHO = "\033[31m"
VERDE = "\033[32m"
AMARELO = "\033[38;2;255;203;87m"
AZUL = "\033[34m"
ROXO = "\033[35m"
CIANO = "\033[36m"
BRANCO = "\033[37m"
RESETAR = "\033[0m"

class Jogo:
    def __init__(self):
        
        self.nomes = ["Maria", "Isabella", "Angelina", "Diego", "Carlos", "Victor", "Guilherme"]
        
        self.papeis_da_partida = [] # Quais 7 papeis estao neste jogo
        self.jogadores = []         # A lista final de objetos (ex: Medico("Maria"))

        # 1. Define os 7 papeis (1 Lobo + 6 sorteados)
        self._definir_papeis_partida()
        
        # 2. Distribui esses papeis aleatoriamente para os nomes
        self.distribuir_papeis()

    # 2. Metodo para definir os 7 papeis da partida
    def _definir_papeis_partida(self): # Metodo privado

        base_garantida = [Lobisomem, Medico, Cidadao, Cidadao] # Garantidos
        pool_extra = [Lobisomem, Medico, Cidadao, Vidente, Bruxa, Pistoleiro] # Ultimos 3 sorteados entre esses

        random.shuffle(pool_extra)
        papeis_sorteados_extra = pool_extra[:3]
        self.papeis_da_partida = base_garantida + papeis_sorteados_extra

        nomes_papeis = [p.__name__ for p in self.papeis_da_partida]
        print(f"Debug       ---- Papeis na partida (antes de embaralhar):\n{nomes_papeis}")


    # 3. Metodo para distribuir os papeis aos nomes
    def distribuir_papeis(self):

        # Embaralhar a lista de papeis
        papeis_embaralhados = self.papeis_da_partida[:] 
        random.shuffle(papeis_embaralhados)

        # O 'zip' une as duas listas (nome[0] com papel[0], nome[1] com papel[1], ...)
        for nome_personagem, classe_papel in zip(self.nomes, papeis_embaralhados):     
            # Cria o objeto (ex: Medico("Maria"))
            jogador_objeto = classe_papel(nome_personagem)
            
            self.jogadores.append(jogador_objeto)

def lista_suspeitos(default):
    print(CIANO+"Lista de suspeitos"+RESETAR)
    if default == True:
        print(PRETO+"Maria        ||  Cidadao")
        print("Isabella     ||  Lobisomem")
        print("Angelina     ||  Medico")
        print("Diego        ||  ")
        print("Carlos       ||  ")
        print("Victor       ||  Vidente")
        print("Guilherme    ||  "+RESETAR)

def finalizar_jogo(default):
    print(CIANO+"Finalizar investigação"+RESETAR)
    print("Sua pontuação final é calculada somando os bônus e subtraindo as penalidades")
    print(VERDE+"Ganhos (Bônus)"+RESETAR)
    print(VERDE+"+30 pontos:"+RESETAR+" Ao identificar corretamente o Lobisomem.")
    print(VERDE+"+10 pontos:"+RESETAR+" Por cada suspeito (não-lobisomem) com o perfil identificado corretamente.\n")
    print(VERMELHO+"Penalidades (Perdas)"+RESETAR)
    print(VERMELHO+"-30 pontos:"+RESETAR+" Ao identificar erroneamente o Lobisomem.")
    print(VERMELHO+"-5 pontos:"+RESETAR+" Por cada rodada (noite) que passa.")
    print(VERMELHO+"-5 pontos:"+RESETAR+" Por cada morte de inocentes.")
    print(VERMELHO+"-5 pontos:"+RESETAR+" Por cada perfil de suspeito identificado erroneamente.")
    if default == True:
        print("Seu palpite:")
        lista_suspeitos(True)
        print("\nSua pontuação:")
        print(VERDE+"+30 pontos +10 pontos"+VERMELHO+" -5 pontos -5 pontos -5 pontos -5 pontos -5 pontos"+RESETAR)
        print("Total: "+VERDE+"+15 pontos"+RESETAR)

def formatar_paragrafo(texto):
    texto_formatado = textwrap.fill(texto, width=LARGURA_MAXIMA, replace_whitespace=False)
    for letra in texto_formatado:
        print(letra, end='', flush=True) 
        time.sleep(0.05)

# Contexto e tutorial inicial
def inicio():
    texto = """Você é um detetive renomado, e seu novo caso o leva à misteriosa cidade de Wolvesville, onde eventos estranhos têm tirado o sono dos moradores."""
    formatar_paragrafo(texto)
    print()
    texto = """Antes mesmo de arrumar as malas, você fez uma pesquisa preliminar. O que descobriu foi alarmante: os "eventos incomuns" eram apenas a ponta do iceberg. O mistério era muito mais profundo e perigoso do que as notícias locais sugeriam. Percebendo a gravidade da situação, você decidiu que este caso exigia sua presença pessoal."""
    formatar_paragrafo(texto)
    print()
    formatar_paragrafo("Agora, em Wolvesville, sua rotina é clara:")
    print()
    formatar_paragrafo(ROXO+"Durante o dia: "+RESETAR+"Você investiga a cidade, segue pistas e entrevista os vários suspeitos.")
    print()
    texto = ROXO+"""Durante a noite:"""+RESETAR+""" Você se mantém em segurança, revisando e organizando as informações coletadas em seu diário de investigação."""
    formatar_paragrafo(texto)
    print()
    input(PRETO+"Clique 'Enter' para continuar"+RESETAR)
    print(ROXO+"\n                           Como o jogo funciona"+RESETAR)
    print("" + "="*80 + "")
    texto = """O jogo avança em rodadas (cada noite é uma rodada). A partir da primeira noite, você terá estas opções principais:"""
    formatar_paragrafo(texto)
    print()
    texto = ROXO+"""A. Atualizar lista de suspeitos: """+RESETAR+"""Use esta opção para registrar seus palpites sobre os papéis de cada suspeito. Além de ajudar na sua organização, cada palpite correto renderá pontos de bônus ao final do jogo."""
    formatar_paragrafo(texto)
    print()
    print(PRETO+"Exemplo da lista de suspeitos:"+RESETAR)
    lista_suspeitos(True)
    print(PRETO+"="*80+RESETAR)
    input(PRETO+"\nClique 'Enter' para continuar"+RESETAR)
    print()
    texto = ROXO+"""B. Finalizar investigação: """+RESETAR+"""Esta opção encerra o jogo. Ao selecioná-la e confirmar, sua pontuação total será revelada, mostrando o detalhamento dos seus acertos."""
    formatar_paragrafo(texto)
    print()
    print(PRETO+"Exemplo da finalização da investigação:"+RESETAR)
    finalizar_jogo(True)
    print(PRETO+"="*80+RESETAR)
    texto = ROXO+"""C. Passar para a noite (dormir): """+RESETAR+"""Passa para a proxima noite"""
    formatar_paragrafo(texto)
    print()

if __name__ == "__main__":
    print(ROXO+"\n\n\t\t\tBem vindo a Wolvesville!"+RESETAR)
    print("" + "="*80 + "")
    op = input(PRETO+"Para pular a explicação, pressione 0\nPara continuar, pressione 'Enter'\n"+RESETAR)
    if op == '0':
        print("Iniciando jogo.....")
    else:
        inicio()

    print("\n\n" + "="*80 + "")
    meu_jogo = Jogo()

    print("\nDebug       ---- Estes sao os papeis dos suspeitos:") 
    for jogador in meu_jogo.jogadores:
        print(jogador) 
    print("\n" + "="*80 + "\n\n")

    # =============================================================
    # JOGO LOGICAS

    jogo_ativo = True
    rodada = 1
    pontuacao = 0
    palpites_jogador = {}

    while jogo_ativo:
        print(AMARELO + f"\n\t\t\t\tDIA {rodada}" + RESETAR)
        print(AMARELO + "="*80 + RESETAR)

        while True: # Dia
            print("\nO que voce, detetive, deseja fazer?")
            print(AMARELO + "[A]" + RESETAR + " Atualizar lista de suspeitos")
            print(AMARELO + "[B]" + RESETAR + " Finalizar investigacao")
            print(AMARELO + "[C]" + RESETAR + " Passar para a noite (Dormir)")
            
            op = input(PRETO+"Sua escolha: "+RESETAR+"\n-> ").strip().upper()
            
            # --- A ---
            if op == 'A':
                print("\nOpção A\n")

            # --- B  ---
            elif op == 'B':
                print(VERMELHO + "\nTEM CERTEZA? Essa opção finalizara o jogo, você não poderá voltar." + RESETAR)
                confirmar = input("(S/N)\n-> ").strip().upper()
                if confirmar == 'S':
                    jogo_ativo = False # Parar o jogo
                    break
                else:
                    print("Investigacao retomada.")

            # --- C  ---
            elif op == 'C':
                print()
                texto = PRETO + "Voce revisa suas notas e a noite cai em Wolvesville..." + RESETAR
                formatar_paragrafo(texto)
                break

            else:
                print()
                texto = VERMELHO + "Opcao invalida. Escolha A, B ou C." + RESETAR
                formatar_paragrafo(texto)

        # --- Fim do Dia ---
        if not jogo_ativo:
            break

        # Noite
        print(AZUL + f"\n\n\t\t\t\tNOITE {rodada}" + RESETAR)
        print(AZUL + "="*80 + RESETAR)
        time.sleep(2) # Pausa dramática
        print("Auuuuuuuuuuuuuuuuuuuuuuuuu")
        rodada += 1

    print()
    print(ROXO + "A investigacao foi encerrada." + RESETAR)
    print(ROXO + "" + "="*80 + RESETAR)
    
    print()
    finalizar_jogo(True)

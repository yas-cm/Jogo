# -*- coding: utf-8 -*-
import random
from classes import *
import textwrap
LARGURA_MAXIMA = 80

PRETO = "\033[30m"
VERMELHO = "\033[31m"
VERDE = "\033[32m"
AMARELO = "\033[33m"
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

def formatar_paragrafo(texto):
    return textwrap.fill(texto, width=LARGURA_MAXIMA, replace_whitespace=False)

def inicio():
    print(ROXO+"\n\n                        Bem vindo a Wolvesville!"+RESETAR)
    print("" + "="*80 + "")
    texto = """Você é um detetive renomado, e seu novo caso o leva à misteriosa cidade de Wolvesville, onde eventos estranhos têm tirado o sono dos moradores."""
    print(formatar_paragrafo(texto))
    print()
    texto = """Antes mesmo de arrumar as malas, você fez uma pesquisa preliminar. O que descobriu foi alarmante: os "eventos incomuns" eram apenas a ponta do iceberg. O mistério era muito mais profundo e perigoso do que as notícias locais sugeriam. Percebendo a gravidade da situação, você decidiu que este caso exigia sua presença pessoal."""
    print(formatar_paragrafo(texto))
    print("\nAgora, em Wolvesville, sua rotina é clara:")
    print(ROXO+"Durante o dia: "+RESETAR+"Você investiga a cidade, segue pistas e entrevista os vários suspeitos.")
    texto = ROXO+"""Durante a noite:"""+RESETAR+""" Você se mantém em segurança, revisando e organizando as informações coletadas em seu diário de investigação."""
    print(formatar_paragrafo(texto))
    print("\n")
    print(ROXO+"                           Como o jogo funciona"+RESETAR)
    print("" + "="*80 + "")
    texto = """O jogo avança em rodadas (cada noite é uma rodada). A partir da primeira noite, você terá estas opções principais:"""
    print(formatar_paragrafo(texto))
    texto = ROXO+"""A. Atualizar lista de suspeitos: """+RESETAR+"""Use esta opção para registrar seus palpites sobre os papéis de cada suspeito. Além de ajudar na sua organização, cada palpite correto renderá pontos de bônus ao final do jogo."""
    print(formatar_paragrafo(texto))
    print(PRETO+"Exemplo da lista de suspeitos:"+RESETAR)
    lista_suspeitos(True)
    print()
    texto = ROXO+"""B. Finalizar investigação: """+RESETAR+"""Esta opção encerra o jogo. Ao selecioná-la e confirmar, sua pontuação total será revelada, mostrando o detalhamento dos seus acertos."""
    print(formatar_paragrafo(texto))
    print("" + "="*80 + "")
    

if __name__ == "__main__":
    inicio()
    # print("Criando o primeiro jogo...")
    # meu_jogo = Jogo()
    

    # print("\nDebug       ---- Estes sao os papeis dos suspeitos:") 
    # for jogador in meu_jogo.jogadores:
    #     print(jogador) 
        
    # print("\n" + "="*40 + "\n")
    
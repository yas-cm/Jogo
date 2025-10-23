import random
from classes import *

class Jogo:
    def __init__(self):

        print("--- Bem vindo a Wolvesville ---")
        
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


if __name__ == "__main__":
    print("Criando o primeiro jogo...")
    meu_jogo = Jogo()
    

    print("\nDebug       ---- Estes sao os papeis dos suspeitos:") 
    for jogador in meu_jogo.jogadores:
        print(jogador) 
        
    print("\n" + "="*40 + "\n")
    
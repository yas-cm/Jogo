# -*- coding: utf-8 -*-
import random
from classes import *
import textwrap
import time
import os
from pistas import gerar_pista, TEXTOS, anotacoes, PAPEIS_PARA_PISTAS
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

        # Define os 7 papeis (1 Lobo + 6 sorteados)
        self._definir_papeis_partida()
        # Distribui esses papeis aleatoriamente para os nomes
        self.distribuir_papeis()

        # Guarda os resultados da noite
        self.eventos_noite = {}

    # Metodo para definir os 7 papeis da partida
    def _definir_papeis_partida(self): # Metodo privado

        base_garantida = [Lobisomem, Medico, Cidadao, Cidadao] # Garantidos
        pool_extra = [Medico, Cidadao, Vidente, Bruxa, Pistoleiro] # Ultimos 3 sorteados entre esses

        random.shuffle(pool_extra)
        papeis_sorteados_extra = pool_extra[:3]
        self.papeis_da_partida = base_garantida + papeis_sorteados_extra

        nomes_papeis = [p.__name__ for p in self.papeis_da_partida]
        print(f"Debug       ---- Papeis na partida (antes de embaralhar):\n{nomes_papeis}")

    # Metodo para distribuir os papeis aos nomes
    def distribuir_papeis(self):

        # Embaralhar a lista de papeis
        papeis_embaralhados = self.papeis_da_partida[:] 
        random.shuffle(papeis_embaralhados)

        # O 'zip' une as duas listas (nome[0] com papel[0], nome[1] com papel[1], ...)
        for nome_personagem, classe_papel in zip(self.nomes, papeis_embaralhados):     
            # Cria o objeto (ex: Medico("Maria"))
            jogador_objeto = classe_papel(nome_personagem)
            
            self.jogadores.append(jogador_objeto)

    # Executa todas as acoes da noite (Lobo, Medico, Vidente, etc), e armazena os resultados em self.eventos_noite.
    def simular_noite(self, rodada):

        print(f"\nDebug       ---- Iniciando simulacao da noite {rodada}...")
        
        self.eventos_noite = {
            "mortos": [],                 # Lista de nomes (str) de quem morreu
            "sobreviventes": [],          # Lista de nomes (str) de quem foi salvo
            "pistas_vidente": [],         # O que a Vidente descobriu
            "eventos_bruxa": [],          # O que a Bruxa fez
            "eventos_pistoleiro": [],     # Se o pistoleiro atirou
        }
        
        vivos = [j for j in self.jogadores if j.esta_vivo]
        
        lobo = None
        medico = None
        vidente = None
        bruxa = None
        pistoleiro = None
        
        for j in vivos:
            if isinstance(j, Lobisomem):
                lobo = j
            elif isinstance(j, Medico):
                medico = j
            elif isinstance(j, Vidente):
                vidente = j
            elif isinstance(j, Bruxa):
                bruxa = j
            elif isinstance(j, Pistoleiro):
                pistoleiro = j
        
        alvo_lobo = None
        alvo_medico = None
        alvo_vidente_obj = None
        alvo_bruxa_veneno = None
        cura_bruxa = False
        alvo_pistoleiro = None

        ataques_da_noite = {}

        # --- Ação do Lobo ---
        if lobo:
            # Lobo nao pode se matar
            alvos_possiveis = [j for j in vivos if j != lobo]
            if alvos_possiveis:
                # O metodo matar() apenas retorna o alvo escolhido
                alvo_lobo = lobo.matar(random.choice(alvos_possiveis))
                if alvo_lobo:
                    # Causa base (pode ser sobrescrita por causas piores)
                    ataques_da_noite[alvo_lobo] = "Ataque de Lobisomem"

        # --- Ação do Médico ---
        if medico:
            # Medico pode salvar qualquer um, inclusive ele mesmo
            alvos_possiveis = vivos[:] 
            if alvos_possiveis:
                # O metodo salvar() apenas retorna o alvo escolhido
                alvo_medico = medico.salvar(random.choice(alvos_possiveis))

        # --- Ação da Vidente ---
        if vidente:
            # Vidente nao pode se investigar
            alvos_possiveis = [j for j in vivos if j != vidente]

            if rodada == 1:
                alvos_possiveis = [j for j in alvos_possiveis if not isinstance(j, Lobisomem)]

            if alvos_possiveis:
                alvo_vidente_obj = random.choice(alvos_possiveis)
                # O metodo investigar() retorna o papel (str) do alvo
                info_vidente = vidente.investigar(alvo_vidente_obj) 
                
                if random.random() < 0.75: # 75% de chance de ser a equipe
                    if info_vidente == "Lobisomem":
                        pista = TEXTOS["pistas_eventos"]["vidente_equipe"].format(pessoa=alvo_vidente_obj.nome, equipe="Ameaça")
                    elif info_vidente == "Pistoleiro" or info_vidente == "Bruxa":
                        pista = TEXTOS["pistas_eventos"]["vidente_equipe"].format(pessoa=alvo_vidente_obj.nome, equipe="Neutro")
                    else:
                        pista = TEXTOS["pistas_eventos"]["vidente_equipe"].format(pessoa=alvo_vidente_obj.nome, equipe="Inocente")
                else:
                    pista = TEXTOS["pistas_eventos"]["vidente_papel"].format(pessoa=alvo_vidente_obj.nome, papel=info_vidente)

                self.eventos_noite["pistas_vidente"].append(pista)
                # O Debug continua o mesmo
                print(f"\nDebug       ----  Vidente investigou {alvo_vidente_obj.nome} e descobriu: {info_vidente}")
                print(f"Debug       ----  Pista gerada para o detetive: {pista}\n")

        # --- Ação da Bruxa ---            
        if bruxa:
            chance = random.random() # Sorteia 0.0 a 1.0
            
            # 25% de chance de Cura
            if chance < 0.25 and bruxa.pocao_cura:
                cura_bruxa = bruxa.usar_cura()
                if cura_bruxa:
                    self.eventos_noite["eventos_bruxa"].append("cura")
                    print(f"\nDebug       ----  Bruxa ({bruxa.nome}) usou a POCAo DE CURA.\n")
            
            # 25% de chance de Veneno (entre 0.25 e 0.50)
            elif chance > 0.25 and chance < 0.50 and bruxa.pocao_veneno:
                alvos_possiveis = [j for j in vivos if j != bruxa] # Nao pode se envenenar
                if rodada == 1:
                    alvos_possiveis = [j for j in alvos_possiveis if not isinstance(j, Lobisomem)]
                if alvos_possiveis:
                    alvo_escolhido = random.choice(alvos_possiveis)
                    alvo_bruxa_veneno = bruxa.usar_veneno(alvo_escolhido)
                    if alvo_bruxa_veneno:
                        ataques_da_noite[alvo_bruxa_veneno] = "Envenenamento"
                        self.eventos_noite["eventos_bruxa"].append("veneno")
                        print(f"\nDebug       ----  Bruxa ({bruxa.nome}) usou VENENO em {alvo_bruxa_veneno.nome}.\n")
                        
        # --- Ação do Pistoleiro ---
        if pistoleiro and pistoleiro.balas > 0:
            if random.random() < 0.50: # 50% de chance de atirar
                alvos_possiveis = [j for j in vivos if j != pistoleiro]
                if alvos_possiveis:
                    alvo_escolhido = random.choice(alvos_possiveis)
                    alvo_pistoleiro = pistoleiro.atirar(alvo_escolhido)
                    if alvo_pistoleiro:
                        ataques_da_noite[alvo_pistoleiro] = "Tiro (Pistoleiro)"
                        # Salva a pista da revelação
                        pista_pistoleiro = TEXTOS["fatos"]["pistoleiro_revelado"].format(pessoa=pistoleiro.nome)
                        self.eventos_noite["eventos_pistoleiro"].append(pista_pistoleiro)
                        print(f"Debug       ----  Pistoleiro ({pistoleiro.nome}) ATIROU em {alvo_pistoleiro.nome}.")

        # Quem foi salvo pelo medico?
        salvos_pelo_medico = set()
        if alvo_medico:
            salvos_pelo_medico.add(alvo_medico)

        for alvo_obj, causa_da_morte in ataques_da_noite.items():
            
            personagem_salvo = False
            
            # Medico salvou?
            if alvo_obj in salvos_pelo_medico:
                self.eventos_noite["sobreviventes"].append(alvo_obj.nome)
                personagem_salvo = True
                print(f"Debug       ----  {alvo_obj.nome} foi salvo pelo Medico.")

            # Bruxa curou?
            if cura_bruxa:
                # Nao adiciona na lista de sobreviventes se o medico JA salvou
                if not personagem_salvo: 
                    self.eventos_noite["sobreviventes"].append(alvo_obj.nome)
                personagem_salvo = True

            # Ninguém salvou.
            if not personagem_salvo:
                alvo_obj.morrer()
                # Salva o dicionario com NOME e CAUSA
                info_morte = {"pessoa": alvo_obj.nome, "causa": causa_da_morte}
                self.eventos_noite["mortos"].append(info_morte)

        print(f"Debug       ----  Simulacao finalizada. Mortos (info): {self.eventos_noite['mortos']}, Sobreviventes: {self.eventos_noite['sobreviventes']}")

def lista_suspeitos(default, jogo=None, palpites=None):
    print(CIANO+"Lista de suspeitos"+RESETAR)
    print(PRETO + "--------------------------------------" + RESETAR)
    if default == True:
        formatar_paragrafo(PRETO+"Maria        ||  Cidadao")
        formatar_paragrafo("Isabella     ||  Lobisomem")
        formatar_paragrafo("Angelina     ||  Medico")
        formatar_paragrafo("Diego        ||  ")
        formatar_paragrafo("Carlos       ||  ")
        formatar_paragrafo("Victor       ||  Vidente")
        formatar_paragrafo("Guilherme    ||  "+RESETAR)
    else:
        for i, jogador in enumerate(jogo.jogadores):
            nome = jogador.nome           
            palpite_atual = palpites.get(nome, "...")
            nome_formatado = f"[{i+1}] {nome:<10}"
            print(PRETO + f"{nome_formatado} ||  {palpite_atual}" + RESETAR)
    print(PRETO + "--------------------------------------" + RESETAR)

def atualizar_lista_suspeitos(jogo_obj, palpites_jogador):
    papeis_disponiveis = PAPEIS_PARA_PISTAS + ["Não sei"] # Adiciona a opção "Não sei"
    
    while True:
        limpar_tela()
        print(CIANO + "\t\tATUALIZAR LISTA DE SUSPEITOS" + RESETAR)
        print("Estes são seus palpites atuais:\n")
        
        lista_suspeitos(default=False, jogo=jogo_obj, palpites=palpites_jogador)
        
        print("\n" + CIANO + "Qual suspeito você quer atualizar?" + RESETAR)
        op_suspeito = input(PRETO + "Digite o número [1-7] ou [S] para Sair: " + RESETAR + "-> ").strip().upper()

        if op_suspeito == 'S':
            break 

        # --- Validação do Suspeito ---
        try:
            indice = int(op_suspeito) - 1
            if 0 <= indice < len(jogo_obj.jogadores):
                suspeito_obj = jogo_obj.jogadores[indice]
            else:
                print(VERMELHO + "Número inválido." + RESETAR)
                time.sleep(1)
                continue
        except ValueError:
            print(VERMELHO + "Entrada inválida. Digite um número." + RESETAR)
            time.sleep(1)
            continue 

        # --- Escolha do Papel ---
        limpar_tela()
        print(CIANO + f"Atualizando palpite para: {AMARELO}{suspeito_obj.nome}{RESETAR}")
        print("Quais são suas suspeitas sobre este jogador?\n")

        # Mostra a lista de papéis numerada
        for i, papel in enumerate(papeis_disponiveis):
            print(PRETO + f"  [{i+1}] {papel}" + RESETAR)

        op_papel = input(PRETO + "\nDigite o número do palpite: " + RESETAR + "-> ").strip()

        # --- Validação do Papel ---
        try:
            indice_papel = int(op_papel) - 1
            if 0 <= indice_papel < len(papeis_disponiveis):
                papel_escolhido = papeis_disponiveis[indice_papel]
                
                # Salva o palpite no dicionário
                if papel_escolhido == "Não sei":
                    palpites_jogador[suspeito_obj.nome] = "..." # Reseta para o padrão
                else:
                    palpites_jogador[suspeito_obj.nome] = papel_escolhido
                
                print(VERDE + f"\nSalvo: {suspeito_obj.nome} || {papel_escolhido}" + RESETAR)
                time.sleep(1.5)
            else:
                print(VERMELHO + "Número de papel inválido." + RESETAR)
                time.sleep(1)
        except ValueError:
            print(VERMELHO + "Entrada inválida. Digite um número." + RESETAR)
            time.sleep(1)

    limpar_tela()

def finalizar_jogo(default):
    formatar_paragrafo(CIANO+"Finalizar investigação"+RESETAR)
    formatar_paragrafo("Sua pontuação final é calculada somando os bônus e subtraindo as penalidades")
    formatar_paragrafo(VERDE+"Ganhos (Bônus)"+RESETAR)
    formatar_paragrafo(VERDE+"+30 pontos:"+RESETAR+" Ao identificar corretamente o Lobisomem.")
    formatar_paragrafo(VERDE+"+10 pontos:"+RESETAR+" Por cada suspeito (não-lobisomem) com o perfil identificado corretamente.\n")
    formatar_paragrafo(VERMELHO+"Penalidades (Perdas)"+RESETAR)
    formatar_paragrafo(VERMELHO+"-30 pontos:"+RESETAR+" Ao identificar erroneamente o Lobisomem.")
    formatar_paragrafo(VERMELHO+"-5 pontos:"+RESETAR+" Por cada rodada (noite) que passa.")
    formatar_paragrafo(VERMELHO+"-5 pontos:"+RESETAR+" Por cada morte de inocentes.")
    formatar_paragrafo(VERMELHO+"-5 pontos:"+RESETAR+" Por cada perfil de suspeito identificado erroneamente.")
    if default == True:
        formatar_paragrafo("Seu palpite:")
        lista_suspeitos(True)
        formatar_paragrafo("\nSua pontuação:")
        formatar_paragrafo(VERDE+"+30 pontos +10 pontos"+VERMELHO+" -5 pontos -5 pontos -5 pontos -5 pontos -5 pontos"+RESETAR)
        formatar_paragrafo("Total: "+VERDE+"+15 pontos"+RESETAR)

def formatar_paragrafo(texto):
    texto_formatado = textwrap.fill(texto, width=LARGURA_MAXIMA, replace_whitespace=False)
    for letra in texto_formatado:
        print(letra, end='', flush=True) 
        time.sleep(0.05)
    print()

def informacoes_noite(jogo, rodada):
    print()
    texto = PRETO+"""O alívio de acordar dura pouco. Você liga o jornal e a primeira notícia te traz de volta a realidade. O trabalho começou."""
    formatar_paragrafo(texto)
    texto = """No fim do dia, após várias entrevistas com os moradores (suspeitos), retorna ao hotel para organizar o que coletou."""+RESETAR
    formatar_paragrafo(texto)
    print(AZUL+"\nInformações coletadas:"+RESETAR)
    print()
    gerar_pista(jogo, rodada)
    
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_diario():
    if not anotacoes:
        print(VERMELHO + "\nO diário ainda está vazio. Nenhuma noite foi registrada." + RESETAR)
        time.sleep(2)
        return

    nomes = ["Maria", "Isabella", "Angelina", "Diego", "Carlos", "Victor", "Guilherme"]
    papeis = [
    {"papel": "Cidadao Comum","descricao": "Não possui habilidades especiais." },
    {"papel": "Medico","descricao": "Pode salvar uma pessoa por noite." },
    {"papel": "Vidente", "descricao": "Pode descobrir o papel de um jogador por noite." },
    {"papel": "Pistoleiro","descricao": "Tem 2 balas para atirar em quem quiser." },
    {"papel": "Bruxa","descricao": "Tem uma poção de cura e uma de veneno." },
    {"papel": "Lobisomem","descricao": "Mata uma pessoa por noite." }
    ]
    total_paginas = len(anotacoes)+1
    pagina_atual = total_paginas # Começa da noite mais recente

    while True:
        limpar_tela()
        
        # --- Cabeçalho e Conteúdo ---
        print(AZUL + "="*80 + RESETAR)
        print(AZUL + f"\n\t\t\tDIÁRIO DE INVESTIGAÇÃO" + RESETAR)

        if pagina_atual == 1:
            print("\nPrincipais suspeitos:")
            for n in nomes:
                print(f"- {n}")
            print("\nPossíveis perfis:")
            for p in papeis:
                print(f"{p['papel']}: {p['descricao']}")
            print()

        else:
            print(AZUL + f"--- NOITE {pagina_atual-1} ---" + RESETAR)
            
            print(anotacoes[pagina_atual-1]) 
            
        # --- Rodapé e Controles ---
        print(AZUL + "\n" + "="*80 + RESETAR)
        print(PRETO + f"Página {pagina_atual} de {total_paginas}" + RESETAR)
        
        controles = []
        # So mostra [A] Anterior se nao estiver na pagina 1
        if pagina_atual > 1:
            controles.append(PRETO + " [A]" + RESETAR + " Anterior ")
        # So mostra [P] Proxima se nao estiver na ultima pagina
        if pagina_atual < total_paginas:
            controles.append(PRETO + " [P]" + RESETAR + " Próxima ")
        
        controles.append(PRETO + " [S]" + RESETAR + " Sair do Diário ")
        
        print(" | ".join(controles))
        
        op = input(PRETO + "Sua escolha: " + RESETAR + "-> ").strip().upper()

        if op == 'S':
            limpar_tela() # Limpa o diário antes de sair
            break # Volta para o menu principal
        elif op == 'A' and pagina_atual > 1:
            pagina_atual -= 1
        elif op == 'P' and pagina_atual < total_paginas:
            pagina_atual += 1
        else:
            print(VERMELHO + "Opção inválida." + RESETAR)
            time.sleep(1)

# Contexto e tutorial inicial
def inicio():
    # Contexto
    texto = """Você é um detetive renomado, e seu novo caso o leva à misteriosa cidade de Wolvesville, onde eventos estranhos têm tirado o sono dos moradores."""
    formatar_paragrafo(texto)
    texto = """Antes mesmo de arrumar as malas, você fez uma pesquisa preliminar. O que descobriu foi alarmante: os "eventos incomuns" eram apenas a ponta do iceberg. O mistério era muito mais profundo e perigoso do que as notícias locais sugeriam. Percebendo a gravidade da situação, você decidiu que este caso exigia sua presença pessoal."""
    formatar_paragrafo(texto)
    formatar_paragrafo("Agora, em Wolvesville, sua rotina é clara:")
    formatar_paragrafo(ROXO+"Durante o dia: "+RESETAR+"Você investiga a cidade, segue pistas e entrevista os vários suspeitos.")
    texto = ROXO+"""Durante a noite:"""+RESETAR+""" Você se mantém em segurança, revisando e organizando as informações coletadas em seu diário de investigação."""
    formatar_paragrafo(texto)

    input(PRETO+"Clique 'Enter' para continuar"+RESETAR)

    # Explicação do jogo
    print(ROXO+"\n                           Como o jogo funciona"+RESETAR)
    print("" + "="*80 + "")
    texto = """O jogo avança em rodadas (cada noite é uma rodada). A partir da primeira noite, você terá estas opções principais:"""
    formatar_paragrafo(texto)

    # --- A ---
    texto = ROXO+"""A. Atualizar lista de suspeitos: """+RESETAR+"""Use esta opção para registrar seus palpites sobre os papéis de cada suspeito. Além de ajudar na sua organização, cada palpite correto renderá pontos de bônus ao final do jogo."""
    formatar_paragrafo(texto)
    print(PRETO+"Exemplo da lista de suspeitos:"+RESETAR)
    lista_suspeitos(True)
    print(PRETO+"="*80+RESETAR)

    input(PRETO+"\nClique 'Enter' para continuar\n"+RESETAR)

    # --- B ---
    texto = ROXO+"""B. Finalizar investigação: """+RESETAR+"""Esta opção encerra o jogo. Ao selecioná-la e confirmar, sua pontuação total será revelada, mostrando o detalhamento dos seus acertos."""
    formatar_paragrafo(texto)
    print()
    print(ROXO+"Exemplo da finalização da investigação:"+RESETAR)
    print()
    finalizar_jogo(True)
    
    print(PRETO+"="*80+RESETAR)

    input(PRETO+"\nClique 'Enter' para continuar\n"+RESETAR)

    # --- C ---
    texto = ROXO+"""C. Passar para a noite (dormir): """+RESETAR+"""Passa para a proxima noite"""
    formatar_paragrafo(texto)
    print()

    # --- D ---
    texto = ROXO+"""D. Ver diário de investigação: """+RESETAR+"""Mostra lista de pistas de cada noite"""
    formatar_paragrafo(texto)
    print()

    print(PRETO+"="*80+RESETAR)

if __name__ == "__main__":
    print(ROXO+"\n\n\t\t\tBem vindo a Wolvesville!"+RESETAR)
    print("" + "="*80 + "")
    op = input(PRETO+"Para pular a explicação, pressione 0\nPara continuar, pressione 'Enter' "+RESETAR)
    if op != '0':
        inicio()

    # Inicio do jogo    
    print(AZUL+"Iniciando jogo.....\n"+RESETAR)
    
    texto = PRETO+"""É a sua primeira noite em Wolvesville, você queria chegar de manhã mas o destino reservou outros planos. No hotel, você se tranca no quarto, e prepara sua 'super barricada de defesa', afinal, um detetive morto não desvenda caso nenhum."""+RESETAR
    formatar_paragrafo(texto)
    formatar_paragrafo(PRETO+"O sono demora, mas finalmente chega, e com ele a esperança de que esta seja sua única noite neste lugar."+RESETAR)
    
    print("\n\n" + "="*80 + "")
    jogo = Jogo()
    print("\nDebug       ---- Estes sao os papeis dos suspeitos:") 
    for jogador in jogo.jogadores:
        print(jogador) 
    print("\n" + "="*80 + "\n")

    # =============================================================
    # JOGO LOGICAS

    jogo_ativo = True
    rodada = 1
    pontuacao = 0
    palpites_jogador = {}
    formatar_paragrafo(PRETO + "A noite cai pela primeira vez em Wolvesville..." + RESETAR)
    time.sleep(1)
    print()
    jogo.simular_noite(rodada)

    while jogo_ativo:
        print(AMARELO + f"\n\t\t\t\tDIA {rodada}" + RESETAR)
        print(AMARELO + "="*80 + RESETAR)
        informacoes_noite(jogo, rodada)
        
        while True: # Dia

            print("\nO que voce, detetive, deseja fazer?")
            print(AMARELO + "[A]" + RESETAR + " Atualizar lista de suspeitos")
            print(AMARELO + "[B]" + RESETAR + " Finalizar investigação" + PRETO + " (essa opção finalizará o jogo)" + RESETAR)
            print(AMARELO + "[C]" + RESETAR + " Passar para a noite (Dormir)")
            print(AMARELO + "[D]" + RESETAR + " Ver diário de investigação")
            
            
            op = input(PRETO+"Sua escolha: "+RESETAR+"\n-> ").strip().upper()
            
            # --- A ---
            if op == 'A':
                print("\nOpção A\n")
                atualizar_lista_suspeitos(jogo, palpites_jogador)

            # --- B  ---
            elif op == 'B':
                print(VERMELHO + "\nTEM CERTEZA? Essa opção finalizará o jogo, você não poderá voltar." + RESETAR)
                confirmar = input("(S/N)\n-> ").strip().upper()
                if confirmar == 'S' or confirmar == "SIM":
                    jogo_ativo = False # Parar o jogo
                    break
                else:
                    print("Investigação retomada.")

            # --- C  ---
            elif op == 'C':
                print()
                formatar_paragrafo(PRETO + "Você revisa suas notas e a noite cai em Wolvesville..." + RESETAR)
                break

            # --- D ---
            elif op == 'D':
                mostrar_diario()

            else:
                print()
                formatar_paragrafo(VERMELHO + "Opção inválida. Escolha A, B, C ou D." + RESETAR)

        # --- Fim do Dia ---
        if not jogo_ativo:
            break

        # Noite
        rodada += 1
        print(AZUL + f"\n\n\t\t\t\tNOITE {rodada}" + RESETAR)
        print(AZUL + "="*80 + RESETAR)
        time.sleep(2) # Pausa dramática
        print("Auuuuuuuuuuuuuuuuuuuuuuuuu")
        
        jogo.simular_noite(rodada)

    print()
    print(ROXO + "A investigacao foi encerrada." + RESETAR)
    print(ROXO + "" + "="*80 + RESETAR)
    
    print()

# -*- coding: utf-8 -*-
import os
import time
import textwrap
from pistas import gerar_pista, TEXTOS, anotacoes, PAPEIS_PARA_PISTAS
from classes import *

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


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def formatar_paragrafo(texto, lento=True, recuo_especial=False):
    """
    Formata e imprime o texto. 
    lento=True: Imprime letra por letra.
    lento=False: Imprime o bloco formatado.
    recuo_especial=True: (Apenas se lento=False) Formata cada linha 
                         individualmente com recuo para sub-linhas 
                         (usado no Diário).
    """
    if lento:
        texto_formatado = textwrap.fill(texto, width=LARGURA_MAXIMA, replace_whitespace=False)
        for letra in texto_formatado:
            print(letra, end='', flush=True) 
            time.sleep(0.05)
        print()
    else:
        if recuo_especial:
            linhas_formatadas = []
            linhas_originais = texto.split('\n')
            
            for linha in linhas_originais:
                linha_processada = textwrap.fill(
                    linha, 
                    width=LARGURA_MAXIMA, 
                    replace_whitespace=False,
                    subsequent_indent="  " 
                )
                linhas_formatadas.append(linha_processada)
            
            print("\n".join(linhas_formatadas))
        
        else:
            texto_formatado = textwrap.fill(texto, width=LARGURA_MAXIMA, replace_whitespace=False)
            print(texto_formatado)

def lista_suspeitos(default, jogo=None, palpites=None, final=False, lobo_morreu=False):
    print(CIANO+"Lista de suspeitos"+RESETAR)
    print(PRETO + "--------------------------------------" + RESETAR)
    
    if default == True:
        formatar_paragrafo(PRETO+"Maria        ||  Cidadao", lento=False)
        formatar_paragrafo("Isabella     ||  Lobisomem", lento=False)
        formatar_paragrafo("Angelina     ||  Medico", lento=False)
        formatar_paragrafo("Diego        ||  ", lento=False)
        formatar_paragrafo("Carlos       ||  ", lento=False)
        formatar_paragrafo("Victor       ||  Vidente", lento=False)
        formatar_paragrafo("Guilherme    ||  "+RESETAR, lento=False)
    
    else:
        if not jogo or palpites is None:
            print(VERMELHO + "Erro: 'jogo' e 'palpites' são necessários." + RESETAR)
            return

        for i, jogador in enumerate(jogo.jogadores):
            nome = jogador.nome
            palpite_atual = palpites.get(nome, "...")
            nome_formatado = f"[{i+1}] {nome:<10}"

            if final:
                papel_real = jogador.papel
                palpite_formatado = f"{palpite_atual:<15}" 
                
                if palpite_atual == papel_real:
                    pontos_str = "(+10)"
                    if papel_real == "Lobisomem":
                        pontos_str = "(+30)" if not lobo_morreu else "(+0)" 
                    print(VERDE + f"{nome_formatado} ||  {palpite_formatado} {pontos_str}" + RESETAR)
                
                elif palpite_atual == "...":
                    print(PRETO + f"{nome_formatado} ||  {palpite_atual}" + RESETAR)
                
                else:
                    pontos_str = "(-10)"
                    if palpite_atual == "Lobisomem": 
                        pontos_str = "(-30)" if not lobo_morreu else "(-10)" 
                    print(VERMELHO + f"{nome_formatado} ||  {palpite_formatado} {pontos_str}" + RESETAR)
            else:
                print(PRETO + f"{nome_formatado} ||  {palpite_atual}" + RESETAR)

                
    print(PRETO + "--------------------------------------" + RESETAR)

def atualizar_lista_suspeitos(jogo_obj, palpites_jogador):
    papeis_disponiveis = PAPEIS_PARA_PISTAS + ["Não sei"] 
    
    while True:
        limpar_tela()
        print(CIANO + "\t\tATUALIZAR LISTA DE SUSPEITOS" + RESETAR)
        print("Estes são seus palpites atuais:\n")
        
        lista_suspeitos(default=False, jogo=jogo_obj, palpites=palpites_jogador, final=False)
        
        print("\n" + CIANO + "Qual suspeito você quer atualizar?" + RESETAR)
        op_suspeito = input(PRETO + "Digite o número [1-7] ou [S] para Sair: " + RESETAR + "-> ").strip().upper()

        if op_suspeito == 'S':
            break 

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

        limpar_tela()
        print(CIANO + f"Atualizando palpite para: {AMARELO}{suspeito_obj.nome}{RESETAR}")
        print("Quais são suas suspeitas sobre este jogador?\n")

        for i, papel in enumerate(papeis_disponiveis):
            print(PRETO + f"  [{i+1}] {papel}" + RESETAR)

        op_papel = input(PRETO + "\nDigite o número do palpite (7 para sair): " + RESETAR + "-> ").strip()

        try:
            indice_papel = int(op_papel) - 1
            if 0 <= indice_papel < len(papeis_disponiveis):
                papel_escolhido = papeis_disponiveis[indice_papel]
                
                if papel_escolhido == "Não sei":
                    palpites_jogador[suspeito_obj.nome] = "..." 
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

def mostrar_diario(jogo_obj):
    if not anotacoes:
        print(VERMELHO + "\nO diário ainda está vazio. Nenhuma noite foi registrada." + RESETAR)
        time.sleep(2)
        return

    nomes = [j.nome for j in jogo_obj.jogadores]
    papeis = [
        {"papel": "Cidadao Comum","descricao": "Não possui habilidades especiais." },
        {"papel": "Medico","descricao": "Pode salvar uma pessoa por noite." },
        {"papel": "Vidente", "descricao": "Pode descobrir o papel ou a equipe de um jogador por noite." },
        {"papel": "Pistoleiro","descricao": "Tem 2 balas para atirar em quem quiser. Após a primeira, sua identidade é revelada." },
        {"papel": "Bruxa","descricao": "Tem uma poção de cura e uma de veneno. A cura salva a todos." },
        {"papel": "Lobisomem","descricao": "Mata uma pessoa por noite. PERIGOSO!" }
    ]
    
    total_paginas = len(anotacoes)+1
    pagina_atual = total_paginas 

    while True:
        limpar_tela()
        print(AZUL + "="*80 + RESETAR)
        print(AZUL + f"\n\t\t\tDIÁRIO DE INVESTIGAÇÃO" + RESETAR)

        if pagina_atual == 1:
            # --- SEÇÃO DE SUSPEITOS ---
            print("\n" + CIANO + "--- PRINCIPAIS SUSPEITOS ---" + RESETAR)
            for n in nomes:
                print(f"- {n}")
            
            # --- SEÇÃO DE MORTOS ---
            print("\n" + CIANO + "--- LISTA DE MORTOS ---" + RESETAR)
            mortos = [j.nome for j in jogo_obj.jogadores if not j.esta_vivo]
            if not mortos:
                print(PRETO + "Nenhuma morte registrada (ainda)." + RESETAR)
            else:
                for m in mortos:
                    print(VERMELHO + f"- {m}" + RESETAR)

            # --- SEÇÃO DE EQUIPES ---
            print("\n" + CIANO + "--- EQUIPES CONHECIDAS ---" + RESETAR)
            print(VERDE + "INOCENTE:" + RESETAR + " Medico, Vidente, Cidadao Comum")
            print(VERMELHO + "AMEAÇA:" + RESETAR + " Lobisomem")
            print(AMARELO + "NEUTRO:" + RESETAR + " Bruxa, Pistoleiro")
            
            # --- SEÇÃO DE PAPÉIS ---
            print("\n" + CIANO + "--- POSSÍVEIS PAPÉIS ---" + RESETAR)
            for p in papeis:
                print(f"{p['papel']}: {p['descricao']}")
            print()
            
        else:
            print(AZUL + f"--- NOITE {pagina_atual-1} ---" + RESETAR)
            formatar_paragrafo(anotacoes[pagina_atual-1], lento=False, recuo_especial=True) 
            
        print(AZUL + "\n" + "="*80 + RESETAR)
        print(PRETO + f"Página {pagina_atual} de {total_paginas}" + RESETAR)
        
        controles = []
        if pagina_atual > 1:
            controles.append(PRETO + " [A]" + RESETAR + " Anterior ")
        if pagina_atual < total_paginas:
            controles.append(PRETO + " [P]" + RESETAR + " Próxima ")
        controles.append(PRETO + " [S]" + RESETAR + " Sair do Diário ")
        print(" | ".join(controles))
        
        op = input(PRETO + "Sua escolha: " + RESETAR + "-> ").strip().upper()

        if op == 'S':
            limpar_tela()
            break
        elif op == 'A' and pagina_atual > 1:
            pagina_atual -= 1
        elif op == 'P' and pagina_atual < total_paginas:
            pagina_atual += 1
        else:
            print(VERMELHO + "Opção inválida." + RESETAR)
            time.sleep(1)

def informacoes_noite(jogo, rodada):
    print()
    texto = PRETO+"""O alívio de acordar dura pouco. Você liga o jornal e a primeira notícia te traz de volta à realidade. O trabalho começou."""
    formatar_paragrafo(texto)
    texto = """No fim do dia, após várias entrevistas com os moradores (suspeitos), retorna ao hotel para organizar o que coletou."""+RESETAR
    formatar_paragrafo(texto)
    print(AZUL+"\nInformações coletadas:"+RESETAR)
    print()
    gerar_pista(jogo, rodada) 
    
def introducao():
    print(ROXO+"\n\n\t\t\tBem vindo a Wolvesville!")
    print("" + "="*80 +RESETAR)
    op = input(PRETO+"\nPara pular a contextualização, pressione 0\nPara continuar, pressione 'Enter' "+RESETAR)
    if op != '0':
        print()
        print(PRETO+"="*80+RESETAR)
        texto = """Você é um detetive renomado, e seu novo caso o leva à misteriosa cidade de Wolvesville, onde eventos estranhos têm tirado o sono dos moradores."""
        formatar_paragrafo(texto)
        texto = """Antes mesmo de arrumar as malas, você fez uma pesquisa preliminar. O que descobriu foi alarmante: os "eventos incomuns" eram apenas a ponta do iceberg. O mistério era muito mais profundo e perigoso do que as notícias locais sugeriam. Percebendo a gravidade da situação, você decidiu que este caso exigia sua presença pessoal."""
        formatar_paragrafo(texto)
        formatar_paragrafo("Agora, em Wolvesville, sua rotina é clara:")
        formatar_paragrafo(ROXO+"Durante o dia: "+RESETAR+"Você investiga a cidade, segue pistas e entrevista os vários suspeitos.")
        texto = ROXO+"""Durante a noite:"""+RESETAR+""" Você se mantém em segurança, revisando e organizando as informações coletadas em seu diário de investigação."""
        formatar_paragrafo(texto)
        print(PRETO+"="*80+RESETAR)
        print()
    op = input(PRETO+"\nPara pular o tutorial, pressione 0\nPara continuar, pressione 'Enter' "+RESETAR)
    limpar_tela()
    if op != '0':
        print(ROXO+"                           Como o jogo funciona"+RESETAR)
        print("" + "="*80 + "")
        texto = """O jogo avança em rodadas (cada noite é uma rodada). A partir da primeira noite, você terá estas opções principais:"""
        formatar_paragrafo(texto)

        print()
        texto = ROXO+"""A. Atualizar lista de suspeitos: """+RESETAR+"""Use esta opção para registrar seus palpites sobre os papéis de cada suspeito. Além de ajudar na sua organização, cada palpite correto renderá pontos de bônus ao final do jogo."""
        formatar_paragrafo(texto)
        print(PRETO+"Exemplo da lista de suspeitos:"+RESETAR)
        lista_suspeitos(True) 
        print(PRETO+"="*80+RESETAR)
        input(PRETO+"\nClique 'Enter' para continuar\n"+RESETAR)
        limpar_tela()

        texto = ROXO+"""B. Finalizar investigação: """+RESETAR+"""Esta opção encerra o jogo. Ao selecioná-la e confirmar, sua pontuação total será revelada, mostrando o detalhamento dos seus acertos."""
        formatar_paragrafo(texto)
        print()
        print(ROXO+"Exemplo da finalização da investigação:"+RESETAR)
        print()
        finalizar_jogo(True) 
        print(PRETO+"="*80+RESETAR)
        input(PRETO+"\nClique 'Enter' para continuar\n"+RESETAR)

        texto = ROXO+"""C. Passar para a noite (dormir): """+RESETAR+"""Passa para a proxima noite"""
        formatar_paragrafo(texto)
        print()
        texto = ROXO+"""D. Ver diário de investigação: """+RESETAR+"""Mostra todas as informações coletadas, inclusive os perfis identificados e pistas de cada noite."""
        formatar_paragrafo(texto)
        print()
        print(PRETO+"="*80+RESETAR)
        input(PRETO+"Clique 'Enter' para continuar"+RESETAR)
        limpar_tela()

def finalizar_jogo(default, jogo=None, palpites=None, rodada=0, lobo_morreu=False):
    
    if default == True:
        # Modo Tutorial
        formatar_paragrafo(CIANO+"Finalizar investigação"+RESETAR)
        formatar_paragrafo("Sua pontuação final é calculada somando os bônus e subtraindo as penalidades")
        formatar_paragrafo(VERDE+"Ganhos (Bônus)"+RESETAR)
        formatar_paragrafo(VERDE+"+30 pontos:"+RESETAR+" Ao identificar corretamente o Lobisomem.")
        formatar_paragrafo(VERDE+"+10 pontos:"+RESETAR+" Por cada suspeito (não-lobisomem) com o perfil identificado corretamente.\n")
        formatar_paragrafo(VERMELHO+"Penalidades (Perdas)"+RESETAR)
        formatar_paragrafo(VERMELHO+"-30 pontos:"+RESETAR+" Ao identificar erroneamente o Lobisomem.")
        formatar_paragrafo(VERMELHO+"-5 pontos:"+RESETAR+" Por cada rodada (noite) que passa.")
        formatar_paragrafo(VERMELHO+"-5 pontos:"+RESETAR+" Por cada morte de inocentes.")
        formatar_paragrafo(VERMELHO+"-10 pontos:"+RESETAR+" Por cada perfil de suspeito identificado erroneamente.")
        formatar_paragrafo("Seu palpite:")
        lista_suspeitos(True)
        formatar_paragrafo("\nSua pontuação:")
        formatar_paragrafo(VERDE+"+30 pontos +10 pontos"+VERMELHO+" -5 pontos -5 pontos -10 pontos -10 pontos -10 pontos"+RESETAR)
        formatar_paragrafo("Total: "+VERDE+"0 pontos"+RESETAR)
        return "SAIR" 

    # --- VERIFICAÇÃO DE GAME OVER (LOBO VENCEU) ---
    if palpites and palpites.get("GAME_OVER") == "LOBO_VENCEU":
        
        def exibir_tela_game_over():
            limpar_tela()
            print(VERMELHO + "\n" + "="*80)
            print("\t\t\tFIM DE JOGO")
            print("="*80 + RESETAR)
            print(AMARELO + "\n\t\tO LOBISOMEM VENCEU. VOCÊ PERDEU.\n" + RESETAR)

            print(CIANO + "--- SITUAÇÃO FINAL ---" + RESETAR)
            print(PRETO + "--------------------------------------" + RESETAR)
            for j in jogo.jogadores:
                nome_formatado = f"{j.nome:<12}"
                papel_real = j.papel
                
                if isinstance(j, Lobisomem):
                    print(AMARELO + f"{nome_formatado} || {papel_real:<15} (VENCEDOR)" + RESETAR)
                elif not j.esta_vivo:
                     print(PRETO + f"{nome_formatado} || {papel_real:<15} (Morto)" + RESETAR)
                else: 
                     print(PRETO + f"{nome_formatado} || {papel_real:<15} (Vivo)" + RESETAR)

            print(PRETO + "--------------------------------------" + RESETAR)
            
            print("\n" + CIANO + "--- SEUS PALPITES FINAIS ---" + RESETAR)
            print(PRETO + "--------------------------------------" + RESETAR)
            for j in jogo.jogadores:
                nome_formatado = f"[*] {j.nome:<10}"
                print(PRETO + f"{nome_formatado} ||  XXX" + RESETAR)
            print(PRETO + "--------------------------------------" + RESETAR)

            print("\n" + ROXO + "="*30)
            print(f"PONTUAÇÃO TOTAL: XXX PONTOS")
            print("="*30 + RESETAR)

        exibir_tela_game_over()

        while True:
            print("\nO que deseja fazer?")
            print(PRETO + "[1]" + RESETAR + " Reiniciar Jogo")
            print(PRETO + "[2]" + RESETAR + " Sair")
            op = input(PRETO + "Sua escolha: " + RESETAR + "-> ").strip()

            if op == '1':
                return "REINICIAR"
            elif op == '2':
                return "SAIR"
            else:
                print(VERMELHO + "Opção inválida." + RESETAR)
                time.sleep(1)
                exibir_tela_game_over()
    # --- FIM DA VERIFICAÇÃO DE GAME OVER ---


    # ==================================
    # MODO DINÂMICO (DEFAULT=FALSE)
    # ==================================
    limpar_tela()
    if not jogo or palpites is None:
        print(VERMELHO + "ERRO: Não foi possível calcular a pontuação." + RESETAR)
        return "SAIR"

    # --- 1. Cálculo Silencioso ---
    pontuacao_total = 0
    resumo_bonus = []
    resumo_penalidades = []
    
    acertou_todos = True 

    for jogador in jogo.jogadores:
        nome = jogador.nome
        papel_real = jogador.papel
        palpite = palpites.get(nome, "...")

        if palpite == papel_real:
            if papel_real == "Lobisomem":
                if not lobo_morreu: 
                    pontuacao_total += 30 
                    resumo_bonus.append(f"+30 pts: Acertou o Lobisomem ({nome})")
                else:
                    resumo_bonus.append(f"+0 pts: Acertou o Lobisomem (mas ele morreu)")
            else:
                pontuacao_total += 10 
                resumo_bonus.append(f"+10 pts: Acertou {nome} ({papel_real})")
        
        elif palpite != "...":
            acertou_todos = False
            if papel_real == "Lobisomem":
                pontuacao_total -= 10 
                resumo_penalidades.append(f"-10 pts: Errou {nome} (Era {papel_real} e você palpitou {palpite})")
            elif palpite == "Lobisomem":
                if not lobo_morreu:
                    pontuacao_total -= 30 
                    resumo_penalidades.append(f"-30 pts: Acusou {nome} de ser o Lobo (Errado! Era {papel_real})")
                else:
                    pontuacao_total -= 10 
                    resumo_penalidades.append(f"-10 pts: Acusou {nome} de ser o Lobo (Errado! Era {papel_real})")
            else:
                pontuacao_total -= 10 
                resumo_penalidades.append(f"-10 pts: Errou {nome} (Era {papel_real} e você palpitou {palpite})")
        
        elif palpite == "...":
            acertou_todos = False
            
    
    penal_rodada = (rodada - 1) * 5 
    if penal_rodada > 0:
        pontuacao_total -= penal_rodada
        resumo_penalidades.append(f"-{penal_rodada} pts: {rodada-1} noites extras (x -5)")

    mortes_nao_ameaca = 0
    for j in jogo.jogadores:
        if j.equipe != "Ameaça" and not j.esta_vivo:
            mortes_nao_ameaca += 1
    penal_mortes = 0
    if mortes_nao_ameaca > 0:
        penal_mortes = mortes_nao_ameaca * 5 
        pontuacao_total -= penal_mortes
        resumo_penalidades.append(f"-{penal_mortes} pts: {mortes_nao_ameaca} mortes (x -5)")
    
    # --- Verificação do Easter Egg ---
    bonus_easter_egg = False
    if acertou_todos and mortes_nao_ameaca < 3 and rodada < 3:
        bonus_easter_egg = True
        pontuacao_total *= 2
    
    # --- 2. Exibição da Tela Final ---
    
    def exibir_tela_final():
        limpar_tela()
        print(CIANO + "\t\tFINAL DA INVESTIGAÇÃO" + RESETAR)
        print("Sua pontuação foi calculada com base nas regras:\n")
        
        print(VERDE+"+30 pontos:"+RESETAR+" Ao identificar corretamente o Lobisomem.")
        print(VERDE+"+10 pontos:"+RESETAR+" Por cada suspeito (não-lobisomem) identificado corretamente.")
        print(VERMELHO+"-30 pontos:"+RESETAR+" Ao identificar erroneamente o Lobisomem (acusar um inocente).")
        print(VERMELHO+"-10 pontos:"+RESETAR+" Por cada perfil de suspeito identificado erroneamente.")
        print(VERMELHO+"-5 pontos:"+RESETAR+" Por cada rodada (noite) que passa (a partir da Noite 2).")
        print(VERMELHO+"-5 pontos:"+RESETAR+" Por cada morte de inocentes.\n")

        print(CIANO + "--- SEUS PALPITES FINAIS ---" + RESETAR)
        lista_suspeitos(default=False, jogo=jogo, palpites=palpites, final=True, lobo_morreu=lobo_morreu)
        
        print("\n" + CIANO + "--- PENALIDADES GERAIS ---" + RESETAR)
        print(VERMELHO + f"Rodadas: {rodada} (-{penal_rodada} pts)" + RESETAR)
        print(VERMELHO + f"Mortes de Inocentes: {mortes_nao_ameaca} (-{penal_mortes} pts)" + RESETAR)

        print("\n" + ROXO + "="*30)
        if bonus_easter_egg:
            print(AMARELO + "INVESTIGAÇÃO IMPECÁVEL! (Bônus x2)" + RESETAR)
            
        print(f"PONTUAÇÃO TOTAL: {pontuacao_total} PONTOS")
        print("="*30 + RESETAR)

    # --- 3. Menu Final Interativo ---
    
    exibir_tela_final() 

    while True:
        print("\nO que deseja fazer?")
        print(PRETO + "[1]" + RESETAR + " Ver Detalhes da Pontuação")
        print(PRETO + "[2]" + RESETAR + " Ver Diário de Investigação")
        print(PRETO + "[3]" + RESETAR + " Reiniciar Jogo")
        print(PRETO + "[4]" + RESETAR + " Sair")
        op = input(PRETO + "Sua escolha: " + RESETAR + "-> ")

        if op == '1':
            limpar_tela()
            print(CIANO + "--- PAPÉIS REAIS ---" + RESETAR)
            for j in jogo.jogadores:
                status = PRETO + "(Morto)" if not j.esta_vivo else ""
                print(f"  {j.nome:<12} || {j.papel} {status}" + RESETAR)
            
            print("\n" + CIANO + "--- DETALHES DA PONTUAÇÃO ---" + RESETAR)
            print("\n" + VERDE + "Bônus:" + RESETAR)
            if not resumo_bonus:
                print("  Nenhum bônus...")
            for b in resumo_bonus:
                print(VERDE + "  " + b + RESETAR)
            
            print("\n" + VERMELHO + "Penalidades:" + RESETAR)
            if not resumo_penalidades:
                print("  Nenhuma penalidade...")
            for p in resumo_penalidades:
                print(VERMELHO + "  " + p + RESETAR)
            
            input("\n(Pressione Enter para voltar...)")
            exibir_tela_final()
        
        elif op == '2':
            mostrar_diario(jogo)
            exibir_tela_final()

        elif op == '3':
            return "REINICIAR"
        elif op == '4':
            return "SAIR"
        else:
            print(VERMELHO + "Opção inválida." + RESETAR)
            time.sleep(1)

# --- Loop Principal do Jogo ---

def rodar_partida(ClasseJogo):
    limpar_tela()
    
    print(AZUL+"Iniciando investigação.....\n"+RESETAR)
    
    texto = PRETO+"""É a sua primeira noite em Wolvesville, você queria chegar de manhã mas o destino reservou outros planos. No hotel, você se tranca no quarto, e prepara sua 'super barricada de defesa', afinal, um detetive morto não desvenda caso nenhum."""+RESETAR
    formatar_paragrafo(texto)
    formatar_paragrafo(PRETO+"O sono demora, mas finalmente chega, e com ele a esperança de que esta seja sua única noite neste lugar."+RESETAR)

    jogo = ClasseJogo() 
    jogo_ativo = True
    rodada = 1
    palpites_jogador = {} 
    aviso_morte_lobo_dado = False
    
    anotacoes.clear()

    formatar_paragrafo(PRETO + "A noite cai pela primeira vez em Wolvesville..." + RESETAR)
    time.sleep(1)
    print()
    jogo.simular_noite(rodada)

    while jogo_ativo:
        
        # --- VITÓRIA DO LOBO ---
        vivos_agora = [j for j in jogo.jogadores if j.esta_vivo]
        if len(vivos_agora) == 1 and isinstance(vivos_agora[0], Lobisomem):
            limpar_tela()
            print()
            formatar_paragrafo(VERMELHO+f"Apenas o Lobisomem, {vivos_agora[0].nome}, continua vivo."+RESETAR)
            print()
            formatar_paragrafo(PRETO+"Você acorda assustado no meio da noite, traumatizado com os acontecimentos dos últimos dias.")
            formatar_paragrafo("Você decide que esse caso saiu do seu controle, e resolve pegar suas coisas e fugir enquanto ainda há tempo.")
            formatar_paragrafo("Em meio ao desespero, você olha para a janela, e percebe que ela está aberta. Será que esqueceu de fechar? Ou será que é tarde demais?")
            print()
            formatar_paragrafo("Antes de processar a informação, você escuta um barulho atrás de você, e percebe que seu tempo acabou.")
            formatar_paragrafo("Você falhou."+RESETAR)
            
            print(VERMELHO + "\n" + "="*80)
            print("\t\t\t\tFIM DE JOGO")
            print("="*80 + RESETAR)
            
            palpites_jogador = {"GAME_OVER": "LOBO_VENCEU"} 
            jogo_ativo = False
            input(PRETO+"Pressione 'Enter' para continuar"+RESETAR)
            continue # Pula direto para o 'finalizar_jogo'
        # --- FIM DA VERIFICAÇÃO ---
            
        lobo = next((j for j in jogo.jogadores if isinstance(j, Lobisomem)), None)
        
        if lobo and not lobo.esta_vivo and not aviso_morte_lobo_dado:
            aviso_morte_lobo_dado = True
            print("\n" + VERMELHO + "="*80)
            print(VERMELHO + "!!! ALERTA !!!" + RESETAR)
            print("O corpo do lobisomem foi encontrado. Quer continuar a investigação?")
            print(PRETO + "(você não ganhará ou perderá pontos extras pelo palpite do lobisomem)" + RESETAR)
            print(VERMELHO + "="*80 + RESETAR)
            
            conf_lobo = input("(S/N) -> ").strip().upper()
            if conf_lobo == 'N':
                print(ROXO + "\nVocê decide encerrar o caso, já que a ameaça principal foi neutralizada." + RESETAR)
                time.sleep(2)
                jogo_ativo = False
                continue 

        
        print(AMARELO + f"\n\t\t\t\tDIA {rodada}" + RESETAR)
        print(AMARELO + "="*80 + RESETAR)
        informacoes_noite(jogo, rodada)
        
        while True: 
            print("\nO que você, detetive, deseja fazer?")
            print(AMARELO + "[A]" + RESETAR + " Atualizar lista de suspeitos")
            print(AMARELO + "[B]" + RESETAR + " Finalizar investigação" + PRETO + " (essa opção finalizará o jogo)" + RESETAR)
            print(AMARELO + "[C]" + RESETAR + " Passar para a noite (Dormir)")
            print(AMARELO + "[D]" + RESETAR + " Ver diário de investigação")
            
            op = input(PRETO+"Sua escolha: "+RESETAR+"\n-> ").strip().upper()
            
            if op == 'A':
                atualizar_lista_suspeitos(jogo, palpites_jogador)

            elif op == 'B':
                print(VERMELHO + "\nTEM CERTEZA? Essa opção finalizará o jogo." + RESETAR)
                confirmar = input("(S/N)\n-> ").strip().upper()
                if confirmar == 'S' or confirmar == "SIM":
                    jogo_ativo = False 
                    break 
                else:
                    print("Investigação retomada.")

            elif op == 'C':
                print()
                formatar_paragrafo(PRETO + "Você revisa suas notas e a noite cai em Wolvesville..." + RESETAR)
                break 

            elif op == 'D':
                mostrar_diario(jogo)

            else:
                print()
                formatar_paragrafo(VERMELHO + "Opção inválida. Escolha A, B, C ou D." + RESETAR)

        if not jogo_ativo:
            break 

        rodada += 1
        print(AZUL + f"\n\n\t\t\t\tNOITE {rodada}" + RESETAR)
        print(AZUL + "="*80 + RESETAR)
        formatar_paragrafo("Auuuuuuuuuuuuuuuuuuuuuuuuu")
        time.sleep(2)
        
        jogo.simular_noite(rodada)

    print()
    print(ROXO + "A investigacao foi encerrada." + RESETAR)
    print(ROXO + "" + "="*80 + RESETAR)
    
    return finalizar_jogo(
        default=False, 
        jogo=jogo, 
        palpites=palpites_jogador, 
        rodada=rodada, 
        lobo_morreu=aviso_morte_lobo_dado
    )
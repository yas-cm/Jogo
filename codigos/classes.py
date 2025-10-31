class Personagem:
    """
    Classe base para todos os personagens do jogo.
    
    Atributos:
        nome (str): O nome do jogador.
        perfil (str): A funcao (ex: "Medico").
        equipe (str): A equipe ("Inocente", "Neutro" ou "Ameaca").
        esta_vivo (bool): O estado do jogador (vivo ou morto).
    """
    def __init__(self, nome, papel, equipe):
        self.nome = nome
        self.papel = papel
        self.equipe = equipe
        self.esta_vivo = True

    def morrer(self):
        """Muda o estado do jogador para morto."""
        self.esta_vivo = False
        print(f"--- NOTICIA: {self.nome} foi eliminado(a). ---")
        if self.papel == "Lobisomem":
            print("\n----------------------------")
            print("O lobisomem foi eliminado!!!")
            print("----------------------------")

    def __str__(self):
        # Debug
        status = "Vivo" if self.esta_vivo else "Morto"
        return f"[{self.nome} | Papel: {self.papel} | Status: {status}]"

# --- INOCENTE ---

class Cidadao(Personagem):
    """
    O Cidadao Comum. Nao possui habilidades especiais.
    """
    def __init__(self, nome):
        # 'super()' chama o construtor da classe 'Personagem'
        super().__init__(nome, "Cidadao Comum", "Inocente")
        # Nenhuma habilidade extra.

class Medico(Personagem):
    """
    O Medico. Pode salvar uma pessoa por noite.
    """
    def __init__(self, nome):
        super().__init__(nome, "Medico", "Inocente")

    def salvar(self, alvo):
        """
        Define a acao de salvar. O 'alvo' deve ser um objeto Personagem.
        A lógica de quem vive ou morre sera tratada pelo 'motor' do jogo.
        """
        if self.esta_vivo:
            print(f"Debug ----        O Medico ({self.nome}) esta tentando salvar {alvo.nome}...")
            return alvo
        return None

class Vidente(Personagem):
    """
    A Vidente. Pode descobrir o papel de um jogador por noite.
    """
    def __init__(self, nome):
        super().__init__(nome, "Vidente", "Inocente")

    def investigar(self, alvo):
        """
        Revela o papel de um jogador (objeto Personagem).
        """
        if self.esta_vivo:
            print(f"Debug ----        A Vidente ({self.nome}) esta investigando {alvo.nome}...")
            # Retorna o papel do alvo para o motor do jogo
            return alvo.papel
        return None

# --- NEUTRO ---

class Pistoleiro(Personagem):
    """
    O Pistoleiro. Tem 2 balas para atirar em quem quiser.
    """
    def __init__(self, nome):
        super().__init__(nome, "Pistoleiro", "Neutro")
        self.balas = 2
        self.identidade_revelada = False

    def atirar(self, alvo):
        """
        Gasta uma bala para tentar atirar em um alvo.
        """
        if not self.esta_vivo:
            return False 

        if self.balas > 0:
            self.balas -= 1
            if not self.identidade_revelada:
                print(f"O Pistoleiro foi revelado! ({self.nome}) atirou em {alvo.nome}!")
                self.identidade_revelada = True 
            else:
                print(f"O Pistoleiro ({self.nome}) atirou novamente, mirando em {alvo.nome}!")
            
            print(f"Debug ----        Balas: {self.balas}")
            return alvo
        else:
            return None

class Bruxa(Personagem):
    """
    A Bruxa. Tem uma pocao de cura e uma de veneno.
    """
    def __init__(self, nome):
        super().__init__(nome, "Bruxa", "Neutro")
        self.pocao_veneno = True 
        self.pocao_cura = True
        self.usou_cura = False

    def usar_veneno(self, alvo):
        """Gasta a pocao de veneno (se disponível) em um alvo."""
        if not self.esta_vivo:
            return False

        if self.pocao_veneno:
            self.pocao_veneno = False 
            print(f"Debug ----        A Bruxa ({self.nome}) usou o veneno em {alvo.nome}.")
            return alvo # Retorna o alvo para o motor do jogo
        else:
            return None

    def usar_cura(self):
        """Gasta a pocao de cura (se disponível) para salvar todos."""
        if not self.esta_vivo:
            return False

        if self.pocao_cura:
            self.pocao_cura = False
            self.usou_cura = True
            print(f"A Bruxa ({self.nome}) usou a pocao de cura! Todos os atacados esta noite estao salvos.")
            return True
        else:
            return False

# --- AMEAcA ---

class Lobisomem(Personagem):
    """
    O Lobisomem. Mata uma pessoa por noite.
    """
    def __init__(self, nome):
        super().__init__(nome, "Lobisomem", "Ameaca")

    def matar(self, alvo):
        """Define o alvo do ataque do Lobisomem."""
        if self.esta_vivo:
            print(f"Debug ----        O Lobisomem ({self.nome}) esta atacando {alvo.nome}...")
            return alvo
        return None

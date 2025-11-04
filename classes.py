class Personagem:
    """
    Classe base para todos os personagens do jogo.
    
    Atributos:
        nome (str): O nome do jogador.
        perfil (str): A função (ex: "Medico").
        equipe (str): A equipe ("Inocente", "Neutro" ou "Ameaça").
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

    def __str__(self):
        status = "Vivo" if self.esta_vivo else "Morto"
        return f"[{self.nome} | Papel: {self.papel} | Status: {status}]"

# --- INOCENTE ---

class Cidadao(Personagem):
    """
    O Cidadao Comum. Nao possui habilidades especiais.
    """
    def __init__(self, nome):
        super().__init__(nome, "Cidadao Comum", "Inocente")

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
                self.identidade_revelada = True 
            
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
            return alvo
        else:
            return None

    def usar_cura(self):
        """Gasta a pocao de cura (se disponível) para salvar todos."""
        if not self.esta_vivo:
            return False

        if self.pocao_cura:
            self.pocao_cura = False
            self.usou_cura = True
            return True
        else:
            return False

# --- AMEAÇA ---

class Lobisomem(Personagem):
    """
    O Lobisomem. Mata uma pessoa por noite.
    """
    def __init__(self, nome):
        super().__init__(nome, "Lobisomem", "Ameaça")

    def matar(self, alvo):
        """Define o alvo do ataque do Lobisomem."""
        if self.esta_vivo:
            return alvo
        return None
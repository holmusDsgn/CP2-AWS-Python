"""Classes do jogo: atributos comuns, herança e ataques polimórficos."""


class Combatente:
    """Estrutura compartilhada pelas classes pai Personagem e Monstro."""

    def __init__(self, nome, hp, mp, speed, atk, matk, defense, mdefense):
        self.nome = nome
        self.hp = hp
        self.mp = mp
        self.speed = speed
        self.atk = atk
        self.matk = matk
        self.defense = defense
        self.mdefense = mdefense

    def esta_vivo(self):
        return self.hp > 0

    def receber_dano(self, dano):
        # Nunca deixa a vida negativa e retorna o dano realmente recebido.
        dano_real = min(self.hp, max(0, dano))
        self.hp -= dano_real
        return dano_real

    def aplicar_ataque(self, alvo, poder, defesa, habilidade):
        if not self.esta_vivo() or not alvo.esta_vivo():
            return "Ataque cancelado: atacante ou alvo derrotado."
        dano = alvo.receber_dano(max(1, poder - defesa))
        texto = (f"{self.nome} usa {habilidade} em {alvo.nome}: "
                 f"{dano} de dano | HP do alvo: {alvo.hp}")
        if not alvo.esta_vivo():
            texto += " [DERROTADO]"
        return texto


class Personagem(Combatente):
    """Classe pai dos heróis. O ataque padrão é físico."""

    def atacar(self, alvo):
        return self.aplicar_ataque(alvo, self.atk, alvo.defense, "Ataque básico")


class Guerreiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, hp=140, mp=0, speed=12, atk=30,
                         matk=4, defense=15, mdefense=7)

    def atacar(self, alvo):
        # Abaixo de metade da vida, a coragem aumenta seu ataque.
        bonus = 8 if self.hp <= 70 else 0
        golpe = "Espada da coragem" if bonus else "Golpe de espada"
        return self.aplicar_ataque(alvo, self.atk + bonus, alvo.defense, golpe)


class Mago(Personagem):
    def __init__(self, nome):
        super().__init__(nome, hp=85, mp=40, speed=16, atk=12,
                         matk=38, defense=6, mdefense=18)

    def atacar(self, alvo):
        if not self.esta_vivo() or not alvo.esta_vivo():
            return "Ataque cancelado: atacante ou alvo derrotado."
        if self.mp >= 10:
            self.mp -= 10
            return self.aplicar_ataque(alvo, self.matk, alvo.mdefense,
                                      "Chama arcana (-10 MP)")
        return self.aplicar_ataque(alvo, self.atk, alvo.defense,
                                  "Cajadada (sem mana)")


class Arqueiro(Personagem):
    def __init__(self, nome):
        super().__init__(nome, hp=100, mp=24, speed=24, atk=27,
                         matk=8, defense=9, mdefense=9)

    def atacar(self, alvo):
        if not self.esta_vivo() or not alvo.esta_vivo():
            return "Ataque cancelado: atacante ou alvo derrotado."
        if self.mp >= 6:
            self.mp -= 6
            # Flecha especial ignora metade da defesa física (arredondada).
            return self.aplicar_ataque(alvo, self.atk, alvo.defense // 2,
                                      "Flecha perfurante (-6 MP)")
        return self.aplicar_ataque(alvo, self.atk, alvo.defense, "Flecha comum")


class Monstro(Combatente):
    """Classe pai dos monstros, que também pode ser instanciada diretamente."""

    def atacar(self, alvo):
        return self.aplicar_ataque(alvo, self.atk, alvo.defense, "Garras")


class Xama(Monstro):
    """Um inimigo que usa magia enquanto possui mana."""

    def __init__(self, nome):
        super().__init__(nome, hp=90, mp=30, speed=15, atk=14,
                         matk=29, defense=7, mdefense=16)

    def atacar(self, alvo):
        if not self.esta_vivo() or not alvo.esta_vivo():
            return "Ataque cancelado: atacante ou alvo derrotado."
        if self.mp >= 10:
            self.mp -= 10
            return self.aplicar_ataque(alvo, self.matk, alvo.mdefense,
                                      "Sombra antiga (-10 MP)")
        return super().atacar(alvo)

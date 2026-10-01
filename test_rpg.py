"""Testes das regras que podem alterar o resultado das batalhas."""

import io
import unittest
from contextlib import redirect_stdout

from batalha import batalha_1v1, batalha_3v3
from main import criar_herois, criar_monstros
from personagens import Arqueiro, Guerreiro, Mago, Monstro, Personagem


class RegrasRPG(unittest.TestCase):
    def alvo(self, hp=200, speed=1, atk=1, defense=10, mdefense=5):
        return Monstro("Alvo", hp, 0, speed, atk, 0, defense, mdefense)

    def executar(self, funcao, *args):
        saida = io.StringIO()
        with redirect_stdout(saida):
            resultado = funcao(*args)
        return resultado, saida.getvalue()

    def test_estrutura_e_heranca(self):
        for heroi in criar_herois():
            self.assertIsInstance(heroi, Personagem)
        for objeto in criar_herois() + criar_monstros():
            for atributo in ("hp", "mp", "speed", "atk", "matk", "defense", "mdefense"):
                self.assertTrue(hasattr(objeto, atributo))

    def test_mago_mana_e_defesa_magica(self):
        mago, alvo = Mago("M"), self.alvo(hp=1000)
        for _ in range(4):
            mago.atacar(alvo)
        self.assertEqual((mago.mp, alvo.hp), (0, 868))
        mago.atacar(alvo)
        self.assertEqual((mago.mp, alvo.hp), (0, 866))

    def test_arqueiro_perfuracao_e_fim_da_mana(self):
        arqueiro, alvo = Arqueiro("A"), self.alvo()
        for _ in range(4):
            arqueiro.atacar(alvo)
        self.assertEqual((arqueiro.mp, alvo.hp), (0, 112))
        arqueiro.atacar(alvo)
        self.assertEqual(alvo.hp, 95)

    def test_coragem_e_dano_minimo(self):
        guerreiro, alvo = Guerreiro("G"), self.alvo()
        guerreiro.hp = 70
        guerreiro.atacar(alvo)
        self.assertEqual(alvo.hp, 172)
        alvo.defense = 1000
        guerreiro.atacar(alvo)
        self.assertEqual(alvo.hp, 171)

    def test_derrotado_nao_ataca_nem_gasta_mana(self):
        mago, alvo = Mago("M"), self.alvo()
        mago.receber_dano(999)
        mago.atacar(alvo)
        self.assertEqual((mago.hp, mago.mp, alvo.hp), (0, 40, 200))

    def test_iniciativa_monstro_e_derrota(self):
        heroi = Guerreiro("Herói")
        monstro = self.alvo(speed=99, atk=999)
        resultado, saida = self.executar(batalha_1v1, heroi, monstro)
        self.assertEqual(resultado, "monstros")
        self.assertNotIn("Herói usa", saida)

    def test_empate_de_velocidade_favorece_heroi(self):
        resultado, _ = self.executar(batalha_1v1, Guerreiro("G"),
                                     self.alvo(hp=1, speed=12, atk=999))
        self.assertEqual(resultado, "herois")

    def test_3v3_termina_e_preserva_limites(self):
        herois, monstros = criar_herois(), criar_monstros()
        resultado, _ = self.executar(batalha_3v3, herois, monstros)
        perdedores = monstros if resultado == "herois" else herois
        self.assertTrue(all(c.hp == 0 for c in perdedores))
        self.assertTrue(all(c.hp >= 0 and c.mp >= 0 for c in herois + monstros))

    def test_3v3_pode_terminar_em_derrota(self):
        monstros = [self.alvo(speed=99, atk=999) for _ in range(3)]
        resultado, _ = self.executar(batalha_3v3, criar_herois(), monstros)
        self.assertEqual(resultado, "monstros")

    def test_3v3_rejeita_tamanho_errado(self):
        with self.assertRaises(ValueError):
            batalha_3v3(criar_herois()[:2], criar_monstros())


if __name__ == "__main__":
    unittest.main()

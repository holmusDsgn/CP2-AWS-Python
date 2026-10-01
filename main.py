"""Execute: python main.py; demonstração automática: python main.py --demo."""

import sys

from batalha import batalha_1v1, batalha_3v3
from personagens import Arqueiro, Guerreiro, Mago, Monstro, Xama


def criar_herois():
    return [Guerreiro("Ayla"), Mago("Orion"), Arqueiro("Lina")]


def criar_monstros():
    return [
        Monstro("Sentinela de pedra", hp=130, mp=0, speed=9, atk=26,
                matk=0, defense=14, mdefense=6),
        Monstro("Lobo das ruínas", hp=80, mp=0, speed=26, atk=22,
                matk=0, defense=6, mdefense=5),
        Xama("Xamã do eclipse"),
    ]


def ler_opcao(mensagem, opcoes):
    while True:
        resposta = input(mensagem).strip()
        if resposta in opcoes:
            return resposta
        print("Opção inválida. Tente novamente.")


def demonstracao():
    print("\nDESAFIO 1: o guardião da entrada")
    batalha_1v1(Guerreiro("Ayla"), criar_monstros()[0])
    print("\nDESAFIO 2: a defesa do cristal")
    batalha_3v3(criar_herois(), criar_monstros())


def main():
    print("CRÔNICAS DO CRISTAL — CP2")
    print("Três aventureiros defendem o último cristal de luz das ruínas.")
    if "--demo" in sys.argv:
        demonstracao()
        return
    while True:
        print("\n1 - Duelo 1v1\n2 - Batalha 3v3\n3 - Demonstração\n0 - Sair")
        opcao = ler_opcao("Escolha: ", {"0", "1", "2", "3"})
        if opcao == "0":
            print("Até a próxima aventura!")
            return
        if opcao == "3":
            demonstracao()
            continue
        manual = ler_opcao("Selecionar alvos manualmente? (s/n): ", {"s", "n"}) == "s"
        # Instâncias novas a cada partida restauram HP e MP sem compartilhar estado.
        if opcao == "1":
            print("1 - Guerreiro\n2 - Mago\n3 - Arqueiro")
            classe = ler_opcao("Seu herói: ", {"1", "2", "3"})
            heroi = criar_herois()[int(classe) - 1]
            batalha_1v1(heroi, criar_monstros()[0], manual)
        else:
            batalha_3v3(criar_herois(), criar_monstros(), manual)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nJogo encerrado.")

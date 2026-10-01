"""Combate por rodadas; as mesmas regras atendem ao duelo e às equipes."""


def vivos(equipe):
    return [membro for membro in equipe if membro.esta_vivo()]


def escolher_alvo(alvos):
    while True:
        for numero, alvo in enumerate(alvos, start=1):
            print(f"{numero} - {alvo.nome} | HP: {alvo.hp} | MP: {alvo.mp}")
        escolha = input("Escolha o alvo: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(alvos):
            return alvos[int(escolha) - 1]
        print("Opção inválida. Digite o número de um alvo vivo.")


def combater(herois, monstros, manual=False):
    if not herois or not monstros:
        raise ValueError("As duas equipes precisam ter combatentes.")
    if not all(c.esta_vivo() for c in herois + monstros):
        raise ValueError("Todos devem começar a batalha vivos.")
    if len({id(c) for c in herois + monstros}) != len(herois + monstros):
        raise ValueError("Cada posição precisa conter um objeto diferente.")

    # sorted é estável: no empate, heróis vêm antes dos monstros;
    # dentro do mesmo time, vale a ordem da lista.
    ordem = sorted(herois + monstros, key=lambda c: c.speed, reverse=True)
    print("\nOrdem de ação: " + " > ".join(c.nome for c in ordem))
    rodada = 1
    while vivos(herois) and vivos(monstros):
        print(f"\n--- RODADA {rodada} ---")
        for atacante in ordem:
            if not atacante.esta_vivo():
                continue
            inimigos = monstros if atacante in herois else herois
            alvos = vivos(inimigos)
            if not alvos:
                break
            if manual and atacante in herois:
                print(f"\nTurno de {atacante.nome} | MP: {atacante.mp}")
                alvo = escolher_alvo(alvos)
            else:
                # Estratégia automática: eliminar primeiro o menor HP atual.
                alvo = min(alvos, key=lambda c: c.hp)
            # Polimorfismo: cada objeto executa sua própria versão de atacar.
            print(atacante.atacar(alvo))
        rodada += 1

    vencedor = "herois" if vivos(herois) else "monstros"
    print("\nVITÓRIA DOS HERÓIS!" if vencedor == "herois"
          else "DERROTA! OS MONSTROS VENCERAM.")
    print("\nEstado final:")
    for membro in herois + monstros:
        print(f"{membro.nome}: HP {membro.hp} | MP {membro.mp}")
    return vencedor


def batalha_1v1(heroi, monstro, manual=False):
    return combater([heroi], [monstro], manual)


def batalha_3v3(herois, monstros, manual=False):
    if len(herois) != 3 or len(monstros) != 3:
        raise ValueError("A batalha 3v3 exige três heróis e três monstros.")
    return combater(herois, monstros, manual)

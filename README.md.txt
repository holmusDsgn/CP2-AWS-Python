Crônicas do Cristal
Trabalho da CP2 de Python sobre Programação Orientada a Objetos.
O jogo acontece no terminal e tem dois modos: um duelo entre um herói e um monstro (1v1) e uma batalha com três personagens de cada lado (3v3). A história é sobre um grupo de aventureiros que precisa proteger um cristal dos monstros das ruínas.
Integrantes
* FELIPE MAHTUK RM570946
* MATHEUS REBELO RM570260
* GUILHERME RM573486
Como jogar
Com o Python 3.8 ou superior instalado, abra o terminal na pasta do projeto e execute:
python main.py

Escolha uma opção no menu. É possível selecionar os alvos durante a batalha ou deixar o combate automático. Para assistir a uma demonstração dos dois modos:
python main.py --demo

Não é necessário instalar bibliotecas adicionais.
Personagens e combate
* Guerreiro: tem mais vida e defesa física. Quando fica com metade da vida ou menos, ganha um bônus de ataque.
* Mago: usa magia que consome mana e atinge a defesa mágica do inimigo. Quando a mana acaba, ataca com o cajado.
* Arqueiro: é o mais rápido dos heróis. Usa mana para disparar uma flecha que ignora metade da defesa física. Sem mana, usa uma flecha comum.
Os inimigos são a Sentinela de Pedra, o Lobo das Ruínas e o Xamã do Eclipse.
Todos possuem vida (hp), mana (mp), velocidade (speed), ataque físico (atk), ataque mágico (matk), defesa física (defense) e defesa mágica (mdefense).
Quem tem mais velocidade age primeiro. Em caso de empate entre herói e monstro, o herói começa. O dano é o ataque menos a defesa correspondente, com mínimo de 1. Personagens derrotados deixam de agir, e vence o time que derrotar todos os adversários.
No modo automático, o alvo escolhido é o inimigo vivo com menos vida. Cada nova partida começa com a vida e a mana restauradas.
Organização do código
* personagens.py: classes e ataques dos personagens e monstros.
* batalha.py: controle dos turnos, escolha de alvos e resultado da batalha.
* main.py: menu e criação dos personagens.
* test\_rpg.py: testes das regras do jogo. Para executar: python -m unittest -v.
As classes Personagem e Monstro herdam os atributos comuns de Combatente. Guerreiro, Mago e Arqueiro herdam de Personagem e cada um tem sua própria versão do método atacar(). Assim, a batalha chama o mesmo método, mas o ataque muda conforme a classe do personagem, demonstrando o polimorfismo.
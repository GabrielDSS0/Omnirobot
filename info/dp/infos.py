from src.minigames.subroom.dp.data.classes.classes import *

warrior = f"""Warrior
Base de Status - HP {Warrior.hp} || ATK {Warrior.atk} || TC {Warrior.cr} || TD {Warrior.dr}

Passiva) Ao causar dano à um inimigo eu provoco ele, fazendo com que o próximo ataque que ele usar seja redirecionado para mim.
Habilidade de Ataque) [Cooldown 1] Cause 10 de dano a um inimigo, ele ficará 20% enfraquecido durante esta rodada e a próxima.
Habilidade de Suporte) [Cooldown 2] [Priority +1] Escolha você ou um aliado para ficar 60% protegido durante esta rodada e a próxima. 
Habilidade Especial) Power Sword: [Cooldown 3] Cause 33 de dano ao inimigo com mais HP. """

mage = f"""Mage
Base de Status - HP {Mage.hp} || Atk {Mage.atk} || TC {Mage.cr} || TD {Mage.dr}

Passiva) Quando eu causar um crítico em um inimigo ele ficará queimado.
Habilidade de Ataque) [Cooldown 1] Cause 6 de dano a todos os inimigos.
Habilidade de Suporte) [Cooldown 2] [Priority +1] Escolha você ou um aliado para receber um escudo de fogo, o escudo explodirá quando seu portador sofrer dano, e em seguida causará 14 (podendo causar crítico) de dano no inimigo que o explodiu.
Habilidade Especial) [Cooldown 3] Cause 18 de dano a um inimigo e queime-o.  Se ele já estiver queimado, cause o dobro de dano."""

cleric = f"""Cleric
Base de Status - HP {Cleric.hp} || Atk {Cleric.atk} || TC {Cleric.cr} || TD {Cleric.dr}

Passiva) No início de cada rodada há 30% de chance do aliado com menos HP ser curado em 7 pontos.
Habilidade de Ataque) [Cooldown 1]  Cause 8 de dano em um inimigo e cure os aliados em 2 pontos.
Habilidade de Suporte) [Cooldown 2] Escolha você ou um aliado para ser curado em 8 pontos, depois cure os outros aliados em 3 pontos também.
Habilidade Especial) [Cooldown 4] Cure todos os aliados em 15 pontos e remova os efeitos negativos deles."""

ninja = f"""Ninja
Base de Status - HP {Ninja.hp} || Atk {Ninja.atk} || TC {Ninja.cr} || TD {Ninja.dr}

Passiva) Quando eu desviar de um golpe causo 7 de dano fixo em quem errou.
Habilidade de Ataque) [Cooldown 1] Cause 6 de dano em dois inimigos o dano é dobrado em inimigos com efeitos negativos.
Habilidade de Suporte) [Cooldown 2] [Priority +1] Escolha um aliado e deixa a TD dele igual a minha durante essa rodada e a próxima.
Habilidade Especial) [Cooldown 3] Aumente meu Atk, TC e TD em 10 pontos durante essa rodada e a próxima. Depois eu utilizo um Ataque Básico no inimigo com menos HP.
"""

paladin = f"""Paladin
Base de Status - HP {Paladin.hp} || Atk {Paladin.atk} || TC {Paladin.cr} || TD {Paladin.dr}

Passiva) Quando eu causar dano, cure o aliado ferido com menos HP em 50% do dano que causei.
Habilidade de Ataque) [Cooldown 1] Cause 8 de dano em um inimigo, depois, se ele era o inimigo com mais HP, utilize este ataque novamente nele, ativa somente uma vez por turno.
Habilidade de Suporte) [Cooldown 1] Durante esta rodada e a próxima todos os aliados ficam 20% protegidos.
Habilidade Especial) [Cooldown 2] Escolha um aliado, para ficar 50% fortalecido e 50% protegido durante esta rodada e a próxima."""

trapper = f"""Trapper
Base de Status - HP {Trapper.hp} || Atk {Trapper.atk} || TC {Trapper.cr} || TD {Trapper.dr}

Passiva) No fim de cada turno, escolha um aliado e plante uma armadilha nele. O time inimigo não saberá quem possui a armadilha.
Durante o próximo turno, sempre que aquele aliado sofrer dano vindo de um inimigo, cause 7 de dano fixo.
Habilidade de Ataque) [Cooldown 1] [Priority +1] Eu ganho 10 pontos de escudo durante esta rodada. No início da próxima rodada cause 10 de dano em um inimigo aleatório, causa 1 de dano adicional para cada ponto de escudo restante.
Habilidade de Suporte) [Cooldown 2] [Priority + 5] Escolha um inimigo e uma habilidade que ele possui, desabilite aquela habilidade durante esta rodada e a próxima. (Se ele utilizar nesta rodada a habilidade irá falhar, e a habilidade não poderá ser selecionada na próxima rodada)
Habilidade Especial) [Cooldown 2] [Priority + 2] Crie uma armadilha defensiva com 20 de HP, ela absorverá dano para os aliados até ser quebrada. No início do próximo turno se ela não foi quebrada, destrua-a e cause dano igual ao HP restante da armadilha ao inimigo com menos HP."""

archer = f"""Archer
Base de Status - HP {Archer.hp} || Atk {Archer.atk} || TC {Archer.cr} || TD {Archer.dr}

Passiva) Eu ignoro a Taxa de Desvio dos inimigos que eu ataco.
Habilidade de Ataque) [Cooldown 2] Escolha um inimigo, eu utilizo três ataques básicos nele.
Habilidade de Suporte) [Cooldown 1] Aumente a Taxa de Crítico dos aliados em 10 durante esta rodada. Depois eu utilizo um ataque básico no inimigo com mais HP.
Habilidade Especial) [Cooldown 2] Escolha entre meu Ataque, Taxa Crítica e Taxa de Desvio para aumentar permanentemente em 10. Depois eu utilizo um ataque básico no inimigo com menos HP."""

berserker = f"""Berserker
Base de Status - HP {Berserker.hp} || Atk {Berserker.atk} || TC {Berserker.cr} || TD {Berserker.dr}

Passiva) Minhas habilidades não possuem cooldown, em vez disso eu perco HP para utilizá-las.
Habilidade de Ataque) [10 HP] Cause 10 de dano a um inimigo, causa 2 de dano adicional para cada 10 pontos de HP que eu perdi.
Habilidade de Suporte) [10 HP] Todos os aliados ganham 50% de roubo de vida durante esta rodada. Eu ganho durante a próxima rodada também.
Habilidade Especial) [30 HP] Remova todos os meus efeitos negativos. No início de cada uma das próximas 3 rodadas eu me curo em 15 pontos. Não pode ser utilizada se esta habilidade já estiver ativa."""

bard = f"""Bard
Base de Status - HP {Bard.hp} || Atk {Bard.atk} || TC {Bard.cr} || TD {Bard.dr}

Passiva) Quando um aliado receber um efeito positivo que não seja escudo, ele também ganhará 3 pontos de escudo.
Habilidade de Ataque) [Cooldown 1] Cause 10 de dano em um inimigo e remova todos os efeitos positivos dele.
Habilidade de Suporte) [Cooldown 1] Fortaleça em 20% todos os aliados  durante esta rodada e a próxima, também remova todos os efeitos negativos deles.
Habilidade Especial) [Cooldown 3] Cause 18 de dano em um inimigo, atordoe outro inimigo e deixe outro inimigo enfraquecido em 50% durante esta rodada e a próxima."""

necromancer = f"""Necromancer
Base de Status - HP {Necromancer.hp} || Atk {Necromancer.atk} || TC {Necromancer.cr} || TD {Necromancer.dr}

Passiva) [Cooldown 1] Em vez da ação do seu turno você poderá utilizar a habilidade de um aliado ou inimigo morto.
Habilidade de Ataque) [Cooldown 2] Cause 13 de dano a um inimigo, ele ficará envenenado durante esta rodada e as próximas duas.
Habilidade de Suporte) [Cooldown 1] Enfraqueça em 50% um inimigo durante esta rodada e a próxima, também remova todos os efeitos positivos dele.
Habilidade Especial) [Cooldown 2] Escolha um aliado vivo, ele ficará envenenado e fortalecido em 100% durante esta rodada e a próxima, ou escolha um aliado morto para reviver com 30% de seu HP total e envenenado."""

gambler = f"""Gambler
Base de Status - HP {Gambler.hp} || Atk {Gambler.atk} || TC {Gambler.cr} || TD {Gambler.dr}

Passiva) Eu possuo uma chance adicional para causar crítico e para desviar de ataques. Quando eu causar crítico ou desviar eu ganho 5 de ouro.
Habilidade de Ataque) [Cooldown 1] Escolha um inimigo e role dois d10, cause dano ao inimigo igual ao número de cada dado, cada dado pode causar crítico individualmente.
Habilidade de Suporte) [Cooldown 1] [Priority +2] Eu fico imune a tudo durante esta rodada e ganho 10 de ouro.
Habilidade Especial) [Gaste 30 Ouros] Escolha um inimigo e role dois d20 e armazene o maior resultado entre eles. Depois o inimigo irá rolar um d20, se ele tirar um número menor que o seu ele perderá metade do HP atual dele."""

spirit = f"""Spirit
Base de Status - HP {Spirit.hp} || Atk {Spirit.atk} || TC {Spirit.cr} || TD {Spirit.dr}

Passiva) No início da partida eu possuo um aliado e ele ganhará 10 pontos de escudo. Eu deixarei de possuir o aliado quando ele morrer.
Eu sou imune a tudo enquanto estiver possuindo.
Habilidade de Ataque) [Cooldown 1] Meu aliado utiliza a Habilidade de Ataque dele. Caso seja necessário escolher um inimigo o alvo será o inimigo com mais HP. (Não pode ser utilizado caso não esteja possuindo)
Habilidade de Suporte) [Cooldown 2] Cure em 5 pontos o aliado que estou possuindo, e escolha um novo aliado para eu possuir, o novo aliado ganhará 10 pontos de escudo. (Caso eu não esteja possuindo, realize apenas a segunda parte da ação)
Habilidade Especial) [Cooldown 0] Me sacrifique para curar em 100% o aliado possuído e remova todos os efeitos negativos dele. (Não pode ser utilizado caso não esteja possuindo)

"""
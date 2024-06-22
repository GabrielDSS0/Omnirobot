playGame = """Funcionamento do jogo:

- O jogo será iniciado num groupchat.
- Terão duas equipes no jogo (Equipe 1 e Equipe 2).
- Os usuários que desejam participar irão falar no chat deste groupchat que irão jogar.
- Estes usuários serão definidos como jogadores e serão colocados em uma das duas equipes.
- Será criado um groupchat para cada equipe, onde o host irá adicionar todos os jogadores das equipes respectivamente em cada groupchat.
- Quando todos os jogadores estiverem em uma equipe, eles irão escolher suas classes. Eles podem fazer isso usando @defclass (classe que eles querem) dentro da PM do DPBot, ou mesmo dizer para o host que querem a classe tal, e o host então adicionará ao bot. Vale lembrar que dentro de uma equipe não se pode haver repetição de classes. Todas as classes estão especificadas nesta thread do fórum: https://pspt.boards.net/thread/701/projeto-dungeons-pokemon
- Assim que todos os jogadores escolherem as suas classes, o jogo começará e eles poderão mandar suas ações.
- As ações serão as habilidades que eles irão mandar. Todas as classes tem habilidades, e todas estão especificadas na thread do jogo.
- As ações serão enviadas pelo groupchat da equipe, e os jogadores da equipe podem interagir entre si para combinar habilidades ou discutir estratégias entre si. Os jogadores enviarão a habilidade que desejam usar neste groupchat, e, se houver a possiblidade de usarem em jogadores do jogo, eles deverão dizer os jogadores que desejam mirar usando a habilidade. Exemplo: O jogador Gabriel Gottapok, que está em posse da classe Warrior, e que quer usar uma habilidade no jogador 1Coffy da equipe adversária.
+Gabriel Gottapok: quero usar sword slash no usuário 1Coffy.
Host na PM do DPBot: @act Gabriel Gottapok, sword slash, 1Coffy
- Depois de enviadas todas as habilidades, o host irá mandar o comando @actsconfirm na PM do bot que fará com que o DPBot compile todas as habilidades e comece a mandar as ações no chat do jogo.
- Quando o HP de uma classe de um jogador chega a 0, esse jogador morre no jogo e não poderá fazer mais nada.
- Quando o HP de todas as classes de uma determinada equipe chegar a 0, o jogo terminará e essa equipe será a perdedora. A outra equipe será a vencedora do jogo.
- Se você quiser saber mais sobre uma classe, digite @nomedaclasse no chat ou na PM do DPBot. Se deseja saber mais sobre um termo do jogo (como sangramento, aumento de prioridade por equipe, vulneravel, etc), digite @comandos na PM do DPBot ou no chat da sala. Se deseja saber mais sobre o jogo em geral, digite @dp na sala ou na PM do DPBot para ver o link do jogo Dungeons & Pokémon no fórum, onde se consta todas as informações do RPG."""


warrior = """Warrior
Base de Status - HP 70 || ATK 70 || TC 20 || TD 20

0) Iron Shield: [Passive] No início da partida eu ganho 20 pontos de escudo permanentemente.
1) Sword Slash: [Cooldown 1] Cause 10 de dano a um adversário, possui 10% de chance de causar atordoamento. (Corpo a Corpo)
2) Defense Force: [Cooldown 2] Eu recebo 10 pontos de escudo. 
3) Taunt: [Cooldown 2] [Priority +3] Provoco todos os inimigos. """

mage = """Mage
Base de Status - HP 65 || Atk 65 || TC 20 || TD 30

0) Fire Force: [Passive] Meus ataques básicos não são corpo a corpo e possuem 25% chance de queimar, quando eu usar uma magia aumente o dano dela em 2.
1) Fire Fall: [Cooldown 1] Cause 6 de dano a 3 inimigos, possui 25% de chance de queimar. (Magia) 
2) Believe of Burn: [Cooldown 1] Queime um inimigo. Seu próximo Ataque Básico será considerado uma Magia.
3) Ignite: [Cooldown 2] Cause 8 de dano a um inimigo, se ele estiver queimado, dobre esse dano. (Magia)"""

cleric = """Cleric
Base de Status - HP 65 || Atk 55 || TC 20 || TD 40

0) Beyond Help: [Passive] Armadilha: Pode ser ativada infinitas vezes, possui 20% de chance de curar um aliado aleatório em 4.
1) Spiritual Exchange: [Cooldown 1] Escolha um aliado e um inimigo, eles trocam de keywords, depois disso o aliado escolhido terá sua TC dobrada e o inimigo terá sua TD reduzida pela metade.
2) Equilibrium [Cooldown 2] Cure um aliado em 10 ou cause 10 de dano em um inimigo. (Magia)
3) Be Brave: [Cooldown 3] [Priority +1] Todos os aliados tem seu dano aumentado em 4 e ganham 7 pontos de escudo neste turno."""

ninja = """Ninja
Base de Status - HP 30 || Atk 50 || TC 40 || TD 70

0) Furtive: [Passive] Meu ataque básico e minhas habilidades são rápidas. Quando eu desviar de um golpe causo 2 de dano em quem errou.
1) Shuriken: [Cooldown 1] Cause 6 de dano a 2 inimigos, possui 60% de chance de causar sangramento.
2) Death Dance: [Cooldown 1] Uso 4 Ataques Básicos em um inimigo que esteja atordoado. 
3) Smoke Bomb: [Cooldown 2] [Priority +3] Provoco um inimigo, caso eu desvie de seu golpe, eu lhe aplico Atordoamento."""

druid = """Druid
Base de Status - HP 65 || Atk 60 || TC 20 || TD 30

0) Natural Cure: Armadilha: Pode ativar infinitas vezes, 35% de chance de curar um status negativos de um aliado.
1) Dual Vine: [Cooldown 1] Cause 5 de dano duas vezes em um inimigo, cada golpe possui 20% de chance de atordoá-lo.
2) Magic Plant: [Cooldown 1] Armadilha: Posso ser ativada até três vezes, possuo 35% de chance de curar um aliado aleatório em 7.
3) Wild Power: [Cooldown 2] Cause 15 de dano em um aliado para ele dobrar o dano do próximo dano que ele causar. (Magia)"""

pirate = """Pirate
Base de Status - HP 80 || Atk 60 || TC 30 || TD 20

0) BAAARRRgain: [Passive] Sempre que eu causar um Crítico aumente o dano que eu causo permanentemente em 1.
1) BAAARRRel: [Cooldown 1] Ative a Armadilha: Possui 90% de chance de ativar, cause 3 de dano em todos os inimigos.
2) Giving ScAAARRRs: [Cooldown 1] Cause 8 de dano a um inimigo e 2 de dano e sangramento em outro.
3) Hook AAARRRm: [Cooldown 2] Atordoe e conceda Vulnerável um inimigo e cause 4 de dano a ele. Caso você use em um inimigo atordoado em vez disso cause 14 de dano a ele."""

archer = """Archer
Base de Status - HP 50 || Atk 20 || TC 50 || TD 50

0) Eagle Eye: [Passive] Ignoro 30 pontos de TD ao causar dano.
1) Arrow Row: [Passive] No início de cada turno eu ganho um stack de flecha permanente que é aplicada ao meu Ataque Básico, quando eu usar meu ataque básico eu usarei a mesma quantidade de ataques básicos que o número de stacks.
2) Level Up: [Cooldown 5] Eu posso escolher um entre quatro upgrades, há limite de 2 na partida. Aumento meu Atk em 10 pontos / Aumento minha TC em 10 / Aumento minha TD em 10.
3) Last Breath: [Passive] Quando eu morrer quem me matou ganha todos os upgrades de Level Up, porém irei usar Ataque Básico nele."""

squire = """Squire
Base de Status - HP 30 || Atk 40 || TC 30 || TD 30

0) Shield Blessing: No início da partida eu ganho 70 pontos de escudo permanentemente.
1) Defense is the best Offense: [Passive] Aliados com escudo tem seu dano causado aumentado. O aumento é equivalente a casa da dezena do escudo que ele tem. Excessões: Caso seja entre 1 e 9, o aumento será 1, Caso seja maior que 99 o aumento será de 10.
2) Damage Reflection: [Cooldown 2] [Priority +2] Escolha um aliado, eu recebo dano por ele, reflita metade do dano que eu sofrer em quem causou.
3) Stand United: [Cooldown 2] [Priority +2] Eu escolho um aliado, nós dois ganhamos 8 pontos de escudo. """

vampire = """Vampire
Base de Status - HP 60 || Atk 60 || TC 30 || TD 30

0) Bloodthirsty: [Passive] Meus ataques básicos me curam em 50% do dano que eu causei. Quando um inimigo morrer eu me curo em 10.
1) Blood Shards: [Passive] Sempre que algo (que não seja eu) sofrer dano, ganho stack de sangue equivalente a 25% do dano que ele sofreu. Eu posso ativar essa habilidade, quando eu ativar curo o meu HP equivalente ao valor stackado. Após usar consome todos os stacks.
2) Batification: [Cooldown 2] [Priority +2] Roube três de HP de um inimigo.
3) Transfusion: [Cooldown 5] Troco de HP com um aliado ou com um inimigo."""

assassin = """Assassin
Base de Status - HP 50 || Atk 60 || TC 30 || TD 40

0) Scary: [Passive] Caso eu receba dano de um inimigo com menos Atk que eu, reduzo o dano causado em 1.
1) Stealthy: [Cooldown 2] Escolha um inimigo, minha TC é dobrada neste turno, use dois Ataques Básicos no inimigo escolhido.
2) Stakeout: [Cooldown 1] [Priority +1] Cause 7 de dano em um inimigo. Ele recebe Vulnerável neste turno. (Corpo a Corpo)
3) Maniac: [Cooldown 3] Dobre meu Atk, TC e TD neste turno e use um Ataque Básico em um inimigo. Caso ele morra reduza o Cooldown dessa habilidade para 0 e eu me curo em 70% do dano que causei."""

clairvoyant = """Clairvoyant
Base de Status - HP 55 || Atk 55 || TC 20 || TD 40

0) Karma: [Passive] Quando um aliado morrer cause 6 de dano em todos os inimigos.
1) Prevision: [Cooldown 1] [Priority +2] Escolha um inimigo, caso ele me alveje, desviarei do golpe, caso contrário cause 8 de dano a ele. (Magia)
2) Crystal Ball: [Cooldown 2] [Priority -2] Escolha um inimigo, cause metade do dano que ele sofreu nesse turno. (Magia)
3) Miracle Eye: [Cooldown 3] Você saberá todas as ações que a equipe inimiga usará nesse turno. Sua equipe irá mandar as ações depois da do inimigo."""

atordoamento = """Atordoamento: Quando alguém estiver atordoado, sua próxima ação não irá acontecer."""

taunt = """Provocar: Quando você provoca algo o ataque que ele usaria em um aliado seu será redirecionado para você."""

burn = """Queimadura: Uma unidade queimada perderá 3 pontos de hp no primeiro turno, 4 pontos no segundo e 5 de hp nos próximos."""

atkb = """Ataque Básico: É um ataque que você disfere em um inimigo, não possui cooldown, você pode usar qualquer turno como sua ação, o dano que ele causa é calculado através do seu status de Atk dividido por 10. Todos os ataques básicos serão "Corpo a Corpo"."""

escudo = """Escudo: Escudos absorvem dano que você recebe. Escudos duram 2 turnos caso não digam o contrário."""

sangramento = """Sangramento: Todo fim de turno a unidade em sangramento sofre 7 de dano."""

vulneravel = """Vulnerável: Unidade vulnerável recebe 1 de dano a mais de todas as fontes."""

armadilha = """Armadilha: O efeito possui chance de ativar no próximo turno, caso não seja especificado a chance será 100%, elas duram o jogo todo (caso não digam o contrário) até serem ativadas (podem ser ativadas mais que uma vez caso seja especificado nela)."""

rapido = """Rápido: O jogador pode escolher se quer que seu ataque tenha priority +1."""

hp = """HP: Sua vida, quando ele chegar a 0 você morre."""

atk = """Ataque (Atk): É usado para desferir um ataque básico em um alvo (Ataque Básico = Ataque da classe dividido por 10)."""

critico = """Taxa Crítica (TC): A chance do seu personagem causar crítico (10 de taxa crítica terá 10% de chance do personagem causar crítico). Críticos multiplicam o dano por 1.5 (Se o dano causado normal for 4, com crítico passará a ser 6)."""

desvio = """Taxa de Desvio (TD): A chance do seu personagem desviar do dano que sofreria (10 de taxa de desvio terá 10% de chance do personagem desviar do golpe)"""

equipePrioridade = """A equipe que tiver a **vantagem de prioridade** em um turno irá ganhar 0.5 de prioridade a mais em suas ações no turno."""

cooldown = """Cooldown: O número de turnos que você precisa realizar a habilidade novamente. Vale constatar que o Cooldown das suas habilidades é 0 quando o jogo começa."""



classesInfos = {
    "warrior": warrior,
    "mage": mage,
    "cleric": cleric,
    "ninja": ninja,
    "druid": druid,
    "pirate": pirate,
    "archer": archer,
    "squire": squire,
    "vampire": vampire,
    "assassin": assassin,
    "clairvoyant": clairvoyant,
}

keywordsInfos = {
    "atordoamento": atordoamento,
    "stun": atordoamento,
    "atordo": atordoamento,
    "taunt": taunt,
    "provocar": taunt,
    "burn": burn,
    "queimar": burn,
    "queimadura": burn,
    "atkb": atkb,
    "ataquebasico": atkb,
    "atkbasico": atkb,
    "escudo": escudo,
    "esc": escudo,
    "shield": escudo,
    "sangramento": sangramento,
    "bleed": sangramento,
    "bleeding": sangramento,
    "blood": sangramento,
    "vulneravel": vulneravel,
    "vulnerabilidade": vulneravel,
    "vulne": vulneravel,
    "vul": vulneravel,
    "trap": armadilha,
    "armadilha": armadilha,
    "arma": armadilha,
    "rapido": rapido,
    "hp": hp,
    "vida": hp,
    "atk": atk,
    "ataque": atk,
    "atkbase": atk,
    "statatk": atk,
    "crit": critico,
    "critico": critico,
    "critical": critico,
    "crit": critico,
    "taxac": critico,
    "tc": critico,
    "desvio": desvio,
    "desv": desvio,
    "taxad": desvio,
    "taxadesvio": desvio, 
    "td": desvio,
    "equipepriority": equipePrioridade,
    "ep": equipePrioridade,
    "equipep": equipePrioridade,
    "cd": cooldown,
    "cooldown": cooldown,
    "coold": cooldown,
}
class MoveDefault:
	type_name: str
	cooldown: int
	priority: int = 0
	damages: dict = {}
	effects: dict = {}
	expected_targets = []


class Warrior_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	damages = {"DAMAGE": 10, "CRITICAL": 10 * 1.5}
	expected_targets = ["enemyPlayer"]


class Warrior_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 2
	priority = 1
	effects = {"PROTEGIDO": {"ROUNDS": 2, "POWER": 20, "TYPE": "positive"}}
	expected_targets = ["allyPlayer"]


class Warrior_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 3
	damages = {"DAMAGE": 33, "CRITICAL": 33 * 1.5}


class Mage_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	damages = {"DAMAGE": 6, "CRITICAL": 6 * 1.5}


class Mage_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 2
	priority = 1
	expected_targets = ["allyPlayer"]


class Mage_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 3
	damages = {
		"DAMAGE": 18,
		"CRITICAL": 18 * 1.5,
		"DAMAGE_BURNED": 18 * 2,
		"CRITICAL_BURNED": 18 * 1.5 * 2,
	}
	expected_targets = ["enemyPlayer"]


class Cleric_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	damages = {"DAMAGE": 8, "CRITICAL": 8 * 1.5}
	expected_targets = ["enemyPlayer"]


class Cleric_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 2
	expected_targets = ["allyPlayer"]


class Cleric_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 4


class Ninja_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	damages = {
		"DAMAGE": 6,
		"CRITICAL": 6 * 1.5,
		"DOUBLE_DAMAGE": 6 * 1.5,
		"DOUBLE_CRITICAL": 6 * 1.5 * 2,
	}
	expected_targets = ["enemyPlayer", "enemyPlayer"]


class Ninja_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 2
	priority = 1
	expected_targets = ["allyPlayer"]


class Ninja_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 3


class Paladin_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	damages = {"DAMAGE": 8, "CRITICAL": 8 * 1.5}
	expected_targets = ["enemyPlayer"]


class Paladin_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 1


class Paladin_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 2
	expected_targets = ["allyPlayer"]


class Trapper_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	priority = 1
	damages = {"DAMAGE": 10, "CRITICAL": 10 * 1.5}


class Trapper_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 2
	priority = 5
	expected_targets = ["enemyPlayer", "ability"]


class Trapper_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 2
	priority = 2
	damages = {
		"DAMAGE": 18,
		"CRITICAL": 18 * 1.5,
	}


class Archer_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 2
	expected_targets = ["enemyPlayer"]


class Archer_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 1


class Archer_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 2
	expected_targets = ["stat"]


class Berserker_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 0
	damages = {"DAMAGE": 10, "CRITICAL": 10 * 1.5}
	expected_targets = ["enemyPlayer"]


class Berserker_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 0


class Berserker_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 0


class Bard_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	damages = {"DAMAGE": 10, "CRITICAL": 10 * 1.5}
	expected_targets = ["enemyPlayer"]


class Bard_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 1


class Bard_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 3
	damages = {
		"DAMAGE": 18,
		"CRITICAL": 18 * 1.5,
	}
	expected_targets = ["enemyPlayer", "enemyPlayer", "enemyPlayer"]


class Necromancer_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 2
	damages = {"DAMAGE": 13, "CRITICAL": 13 * 1.5}
	expected_targets = ["enemyPlayer"]


class Necromancer_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 1
	expected_targets = ["enemyPlayer"]


class Necromancer_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 2
	expected_targets = ["sameTeam"]


class Gambler_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	expected_targets = ["enemyPlayer"]


class Gambler_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 1
	priority = 2


class Gambler_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 0
	expected_targets = ["enemyPlayer"]


class Spirit_01(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 1
	damages = {"DAMAGE": 6, "CRITICAL": 6 * 1.5}


class Spirit_02(MoveDefault):
	type_name = "Habilidade de Suporte"
	cooldown = 2
	expected_targets = ["allyPlayer"]


class Spirit_03(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 0


class Basic_Atk(MoveDefault):
	type_name = "Ataque Básico"
	cooldown = 0
	expected_targets = ["enemyPlayer"]


abilities_dict = {
	"warrior1": Warrior_01,
	"warrior2": Warrior_02,
	"warrior3": Warrior_03,
	"mage1": Mage_01,
	"mage2": Mage_02,
	"mage3": Mage_03,
	"cleric1": Cleric_01,
	"cleric2": Cleric_02,
	"cleric3": Cleric_03,
	"ninja1": Ninja_01,
	"ninja2": Ninja_02,
	"ninja3": Ninja_03,
	"paladin1": Paladin_01,
	"paladin2": Paladin_02,
	"paladin3": Paladin_03,
	"trapper1": Trapper_01,
	"trapper2": Trapper_02,
	"trapper3": Trapper_03,
	"archer1": Archer_01,
	"archer2": Archer_02,
	"archer3": Archer_03,
	"berserker1": Berserker_01,
	"berserker2": Berserker_02,
	"berserker3": Berserker_03,
	"bard1": Bard_01,
	"bard2": Bard_02,
	"bard3": Bard_03,
	"necromancer1": Necromancer_01,
	"necromancer2": Necromancer_02,
	"necromancer3": Necromancer_03,
	"gambler1": Gambler_01,
	"gambler2": Gambler_02,
	"gambler3": Gambler_03,
	"spirit1": Spirit_01,
	"spirit2": Spirit_02,
	"spirit3": Spirit_03,
	"batk": Basic_Atk,
}

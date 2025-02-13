class MoveDefault:
	type_name: str
	cooldown: int
	priority: int = 0
	damages: dict = {}
	effects: dict = {}


class Escudo_de_Fogo(MoveDefault):
	type_name = "Escudo de Fogo"
	cooldown = 0
	damages = {"DAMAGE": 14, "CRITICAL": 14 * 1.5}


class Trapper_1_On(MoveDefault):
	type_name = "Habilidade de Ataque"
	cooldown = 0
	damages = {"DAMAGE": 10, "CRITICAL": 10 * 1.5}


class Trapper_3_On(MoveDefault):
	type_name = "Habilidade Especial"
	cooldown = 0
	damages = {"DAMAGE": 0, "CRITICAL": 0}


extrabilities_dict = {
	"escudodefogo": Escudo_de_Fogo,
	"trapper1_on": Trapper_1_On,
	"trapper3_on": Trapper_3_On,
}

commands_misc = {
            'addpoints': {'params': ["sala", "usuário", "pontos"], 'perm': 'adm', 'type': 'both', 'need_room': True},
            'removepoints': {'params': ["sala", "usuário", "pontos"], 'perm': 'adm', 'type': 'both', 'need_room': True},
            'clearpoints': {'params': ["sala"], 'perm': 'adm', 'type': 'both', 'need_room': True},
            'leaderboard': {'params': ["sala"], 'perm': 'general', 'type': 'both', 'need_room': True},
            'timer': {'params': ["tempo", "unidade (min ou sec)"], 'perm': 'general', 'type': 'both', 'need_room': False},
        }

commands_dp = {
            'startdp':  {'params': [""], 'perm': 'host', 'type': 'room', 'need_room': True},
            'defplayers':  {'params': ["jogadores"], 'perm': 'host', 'type': 'both', 'need_room': False},
            'defclass':  {'params': ["jogador", "classe"], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'confirmclass':  {'params': [], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'act':  {'params': ["jogador", "ação"], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'cancelact':  {'params': [], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'actsconfirm':  {'params': [], 'perm': 'host', 'type': 'both', 'need_room': False},
            'trapper': {'params': ["jogador", "alvo"], 'perm': 'host', 'type': 'both', 'need_room': False},
            'spirit': {'params': ["jogador", "possuído"], 'perm': 'host', 'type': 'both', 'need_room': False},
            'makehost': {'params': ["novo host"], 'perm': 'host', 'type': 'both', 'need_room': False},
            'finishdp':  {'params': [""], 'perm': 'host', 'type': 'room', 'need_room': True},
}

commands_mq = {
            'makequestion': {'params': ["sala", "pergunta"], 'perm': 'host', 'type': 'pm', 'need_room': True},
            'cancelquestion': {'params': [], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'addalternative': {'params': ["alternativa"], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'defineanswer': {'params': ["alternativa correta"], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'showquestion': {'params': [], 'perm': 'host', 'type': 'pm', 'need_room': False},
            'sendquestion': {'params': [], 'perm': 'host', 'type': 'both', 'need_room': False},
            'respondquestion': {'params': ["usuário-host", "alternativa"], 'perm': 'user', 'type': 'pm', 'need_room': False},
            'definetimer': {'params': ["sala", "tempo"], 'perm': 'adm', 'type': 'both', 'need_room': True},
        }

allCommands = commands_misc | commands_mq | commands_dp

allCommands_keys = commands_misc.keys() | commands_mq.keys() | commands_dp.keys()

aliases = {
    "mq": "makequestion",
    "cancel": "cancelquestion",
    "c": "cancelquestion",
    "add": "addalternative",
    "rempoints": "removepoints",
    "defanswer": "defineanswer",
    "danswer": "defineanswer",
    "show": "showquestion",
    "send": "sendquestion",
    "respond": "respondquestion",
    "lb": "leaderboard"
}
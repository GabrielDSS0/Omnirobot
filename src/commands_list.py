commands_dp = {}
commands_mq = {
            'makequestion': {'params': ["sala", "pergunta"], 'perm': 'host', 'type': 'pm', 'need_room': True},
            'cancelquestion': {'params': ["sala"], 'perm': 'host', 'type': 'pm', 'need_room': True},
            'addalternative': {'params': ["sala", "alternativa"], 'perm': 'host', 'type': 'pm', 'need_room': True},
            'defineanswer': {'params': ["sala", "alternativa correta"], 'perm': 'host', 'type': 'pm', 'need_room': True},
            'showquestion': {'params': ["sala"], 'perm': 'host', 'type': 'pm', 'need_room': True},
            'sendquestion': {'params': ["sala"], 'perm': 'host', 'type': 'both', 'need_room': True},
            'respondquestion': {'params': ["sala", "usuário-host", "alternativa"], 'perm': 'user', 'type': 'pm', 'need_room': True},
        }

allCommands = commands_mq.keys() | commands_dp.keys()

aliases = {
    "mq": "makequestion",
    "cancel": "cancelquestion",
    "c": "cancelquestion",
    "add": "addalternative",
    "defanswer": "defineanswer",
    "danswer": "defineanswer",
    "show": "showquestion",
    "send": "sendquestion",
    "respond": "respondquestion"
}
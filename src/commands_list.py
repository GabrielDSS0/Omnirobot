commands_dp = {}
commands_mq = {
            'makequestion': {'params': ["sala", "pergunta"], 'perm': 'host', 'type': 'pm'},
            'cancelquestion': {'params': ["sala"], 'perm': 'host', 'type': 'pm'},
            'addalternative': {'params': ["sala", "alternativa"], 'perm': 'host', 'type': 'pm'},
            'defineanswer': {'params': ["sala", "alternativa correta"], 'perm': 'host', 'type': 'pm'},
            'showquestion': {'params': ["sala"], 'perm': 'host', 'type': 'pm'},
            'sendquestion': {'params': ["sala"], 'perm': 'host', 'type': 'both'},
            'respondquestion': {'params': ["sala", "usuário-host", "alternativa"], 'perm': 'user', 'type': 'pm'},
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
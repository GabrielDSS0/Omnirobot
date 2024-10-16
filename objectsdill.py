import dill
import config
import os

import src.vars as vars

pkl_file = config.pkl_file

def save():
    with open(pkl_file, "wb") as f:
        dill.dump(vars.Varlist.dpGames, f)
        dill.dump(vars.Varlist.hosts_groupchats, f)

def load():
    if not (os.path.exists(pkl_file)):
        open(pkl_file, "x")

    with open(pkl_file, 'rb') as f:
        if not (os.stat(pkl_file).st_size == 0) and not (vars.Varlist.dpGames or vars.Varlist.hosts_groupchats):
            vars.Varlist.dpGames = dill.load(f)
            vars.Varlist.hosts_groupchats = dill.load(f)
        open(pkl_file, "w").close()
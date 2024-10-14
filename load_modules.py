"""from os.path import dirname, basename, isfile, join
import importlib
import glob
paths = glob.glob(join(dirname(__file__), "*"))
for path in paths:
    if isfile(path) and path.endswith(".py"):
        print(path.split("\\")[-1])
    elif not (isfile(path)):
        print(path.split("\\")[-1])"""
import importlib

def importmodules():
    module = importlib.import_module("src.misc_commands.commands")
    importlib.reload(module)
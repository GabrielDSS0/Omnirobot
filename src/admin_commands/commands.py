import importlib
import logging
import subprocess
import sys

import config
import objectsdill
import src.sending as sending
import src.vars as vars


class Admin_Commands:
	def __init__(self):
		self.senderID = vars.Varlist.senderID

	def redirect_command(self, inst, name_func):
		func = getattr(inst, name_func)
		func()

	def kill(self):
		objectsdill.save()
		logging.debug("Exiting the process... (kill command)")
		sys.exit()

	def gitpull(self):
		command = ["git", "pull", config.remote_repository]
		output_git = subprocess.run(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			check=False,
		)
		results_git = (
			(output_git.stdout + output_git.stderr).decode("utf-8").strip()
		)

		sending.respondPM(self.senderID, f"!code {results_git}")

		if results_git.split("\n")[0] == "Already up to date.":
			return

		results_git = results_git.split("\n")

		for result in results_git:
			if result.startswith(" "):
				pipes = result.count("|")
				if not pipes:
					continue
				result = result.split("|", 1)[0].strip()
				if not (result.endswith(".py")):
					return
				result = result.replace("/", ".")
				result = result.replace(".py", "")
				module = importlib.import_module(result)
				importlib.reload(module)

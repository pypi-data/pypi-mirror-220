from src.common.utility import *
from src.common.const import *
import os


class UninstallCmd():
	def __init__(self, args):
		self.args = args
		self.force = args.yes

	def confirmation_prompt(self):
		yes_list = ["yes", "y"]
		prompt = f"Are you sure want to continue uninstall {module_type(self.args)} (yes/y/no)? "
		if not self.force:
			if input(prompt).lower().strip() not in yes_list:
				print_colored(f"cancel uninstall with {module_type(self.args)}", "yellow")
				sys.exit(2)

	def exec(self, pip_path):
		self.confirmation_prompt()
		if self.args.module:
			module_name = self.args.module
		else:
			module_name = fmt_requirement_content(self.args.requirement, "string")
		uninstall_pip_pkg_cmd = "pip-autoremove {} -y".format(module_name)
		cmd_result = exec_cmd(uninstall_pip_pkg_cmd)
		if cmd_result is None:
			print_colored(f"{module_type(self.args)} module and dependencies have been uninstalled", "green")
		else:
			if ignore_errors[self.args.sub_cmd] in cmd_result:
				print_colored(f"{cmd_result}", "blue")
			else:
				print_colored(cmd_result, "red")

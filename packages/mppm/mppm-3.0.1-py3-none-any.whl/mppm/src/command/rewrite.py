from src.common.utility import *
from src.config.pip_conf import *
import os


class RewriteCmd():
    def __init__(self, args):
        self.rewrite_config = args.yes

    def confirmation_prompt(self):
        yes_list = ["yes", "y"]
        prompt = "Are you sure want to continue rewrite the pip configuration: (yes/y/no)? "
        if not self.rewrite_config:
            if input(prompt).lower().strip() not in yes_list:
                print_colored("Skip pip repositories configuration.", "yellow")
            else:
                verification_pypi_url()
        else:
            verification_pypi_url()

    def exec(self, pip_path):
        self.confirmation_prompt()

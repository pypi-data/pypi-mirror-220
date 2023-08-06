from src.common.utility import *
from src.config.pip_conf import *
import os


class DownloadCmd():
    def __init__(self, args):
        self.args = args
        self.rewrite_config = args.yes

    def confirmation_prompt(self):
        yes_list = ["yes", "y"]
        prompt = "Do you need to rewrite the pip configuration: (yes/y/no)? "
        if self.rewrite_config:
            if input(prompt).lower().strip() not in yes_list:
                print_colored("cancel rewrite the pip configuration", "yellow")
            else:
                verification_pypi_url()

    def exec(self, pip_path):
        self.confirmation_prompt()
        if self.args.module:
            create_dir(self.args.module)
            download_pip_pkg_cmd = "{} download {} -d {}".format(pip_path, self.args.module, self.args.module)
        else:
            create_dir(ARG_DOWNLOAD_REQUIREMENT)
            download_pip_pkg_cmd = "{} download {} {} -d {}".format(pip_path, "-r", self.args.requirement,
                                                                    ARG_DOWNLOAD_REQUIREMENT)
        print(download_pip_pkg_cmd)
        cmd_result = exec_cmd(download_pip_pkg_cmd)
        if cmd_result is None or ignore_errors[self.args.sub_cmd] in cmd_result:
            pkg_save_path = os.path.abspath(ARG_DOWNLOAD_REQUIREMENT)
            print_colored(f"package download path: {pkg_save_path}", "green")
        else:
            print_colored(cmd_result, "red")

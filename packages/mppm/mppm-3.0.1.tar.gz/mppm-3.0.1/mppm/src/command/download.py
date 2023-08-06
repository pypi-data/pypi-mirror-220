from src.common.utility import *
from src.config.pip_conf import *
import os


class DownloadCmd():
    def __init__(self, args):
        self.args = args

    def exec(self, pip_path):
        if self.args.module:
            create_dir(self.args.module)
            download_pip_pkg_cmd = "{} download {} -d {}".format(pip_path, self.args.module, self.args.module)
        else:
            create_dir(ARG_DOWNLOAD_REQUIREMENT)
            download_pip_pkg_cmd = "{} download -r {} -d {}".format(pip_path, self.args.requirement,
                                                                    ARG_DOWNLOAD_REQUIREMENT)
        cmd_result = exec_cmd(download_pip_pkg_cmd)
        if cmd_result is None or ignore_errors[self.args.sub_cmd] in cmd_result:
            print_colored(f"the module and dependencies have been downloaded. Please check the current path", "green")
        else:
            print_colored(cmd_result, "red")

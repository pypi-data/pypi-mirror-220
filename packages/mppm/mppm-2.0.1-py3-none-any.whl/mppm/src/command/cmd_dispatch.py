from src.common.const import *
from src.common.utility import *
from src.command.download import DownloadCmd
from src.command.uninstall import UninstallCmd

cmd_mapping = {
    SUB_CMD_DOWNLOAD: DownloadCmd,
    SUB_CMD_UNINSTALL: UninstallCmd
}


def dispatch(args):
    pip_path = check_pip_version()
    if pip_path:
        if cmd_mapping.get(args.sub_cmd):
            cmd_mapping[args.sub_cmd](args).exec(pip_path)
    else:
        sys.exit(2)

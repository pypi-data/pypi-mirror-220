import os
import sys
import subprocess


def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
    }

    if color not in colors:
        raise ValueError("Invalid color. Available colors are: red, green, yellow, blue, magenta, cyan")

    colored_text = colors[color] + text + colors["reset"]
    print(colored_text)


def create_dir(targetPath):
    """
    :param targetPath: mkdir dir
    """
    if os.path.exists(targetPath):
        pass
    else:
        os.makedirs(targetPath)


def check_pip_version():
    """
    :return: check python & pip is available
    """
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    print_colored(f"Usage Python version:\t{python_version}", "cyan")
    print_colored(f"Usage Python path:\t{sys.executable}", "cyan")
    try:
        pip_path = subprocess.check_output(["which", f"pip{python_version}"]).decode().strip()
        print_colored(f"Usage Python path\t{pip_path}", "cyan")
        return pip_path
    except subprocess.CalledProcessError:
        print_colored("pip{} command is not available.".format(python_version), "red")
        return False


def exec_cmd(cmd):
    """
    :param cmd: exec shell cmd 
    :return: cmd exec result
    """
    cmd_result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if len(cmd_result.stderr.decode("utf8")) == 0:
        return
    else:
        return cmd_result.stderr.decode("utf8")

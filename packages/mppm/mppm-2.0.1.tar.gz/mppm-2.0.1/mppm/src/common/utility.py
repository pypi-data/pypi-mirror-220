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
    # cmd_result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    cmd_result_stderr = ""
    while True:
        # output stdout
        cmd_result = process.stdout.readline()
        if cmd_result == b'' and process.poll() is not None:
            break
        if cmd_result:
            print_colored(cmd_result.decode('utf-8').strip(), "magenta")
        
    while True:
        # output stderr
        stderr = process.stderr.readline()
        if not stderr and not process.poll() is None:
            break
        if stderr:
            cmd_result_stderr += stderr.decode('utf-8')

    if len(cmd_result_stderr) == 0:
        return
    else:
        return cmd_result_stderr

def module_type(args):
    if args.module:
        module_name = args.module
    else:
        module_name = args.requirement
    return module_name

def fmt_requirement_content(source_file, fmt_type):
    with open(source_file, "r", encoding="utf8") as sourceFile:
        if fmt_type == "string":
            fmt_content = ""
            for module in sourceFile:
                fmt_content += module.strip() + " "
        elif fmt_type == "list":
            return 
        elif fmt_type == "dict":
            return
    return fmt_content
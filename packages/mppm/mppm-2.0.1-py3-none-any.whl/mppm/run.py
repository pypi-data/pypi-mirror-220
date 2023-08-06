import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

from src.common.const import *
from src.command.cmd_dispatch import dispatch
from src.command.argpass import Parser


def main():
    cli_parser = Parser()
    args = cli_parser.parse()
    dispatch(args)


if __name__ == '__main__':
    main()

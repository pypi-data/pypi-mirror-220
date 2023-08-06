from src.common.const import *
from src.common.utility import *
from pick import pick
import os
import configparser


def choice_pipy_source():
    """
    :return: choose pypi source url
    """
    title = "Please choose a PyPI Configuration Source: "
    options = [f"{source['name']: <20}{source['url']}" for source in pypi_configuration_sources]
    option, index = pick(options, title, indicator="=>")
    url = pypi_configuration_sources[index]["url"]
    timeout = pypi_configuration_sources[index]["timeout"]
    return url, timeout


def rewrite_pypi_config(url, timeout):
    """
    :param url: pip source url
    :return: configparser obj
    """
    config = configparser.ConfigParser(allow_no_value=True)

    config.add_section("global")
    config.set('global', 'timeout', timeout)
    config.set('global', 'index-url', url)
    config.set('global', 'trusted-host', url.split("/")[2])
    return config


def verification_pypi_url():
    pypi_source_url, timeout = choice_pipy_source()
    if pypi_source_url == "None":
        print_colored("Skip pip repositories configuration.", "yellow")
    else:
        config = rewrite_pypi_config(pypi_source_url, timeout)
        home = os.path.expanduser("~")
        config_file = os.path.join(home, ".pip", "pip.conf")
        with open(config_file, "w", encoding="utf8") as f:
            config.write(f)
        print_colored("Successfully updated pip repositories configuration[{}]".format(config_file), "green")

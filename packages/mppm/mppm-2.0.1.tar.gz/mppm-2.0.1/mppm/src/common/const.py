APP_NAME = 'mppm'  # 程序名称
EXIT_WITH_ERROR = 9999  # 错误退出码12 为用户自定义信号

pypi_configuration_sources = [
    {"name": "pypi", "url": "https://pypi.org/simple/", "timeout": "120"},
    {"name": "tuna", "url": "https://pypi.tuna.tsinghua.edu.cn/simple/", "timeout": "60"},
    {"name": "aliyun", "url": "https://mirrors.aliyun.com/pypi/simple/", "timeout": "60"},
    {"name": "douban", "url": "http://pypi.douban.com/simple/", "timeout": "60"},
    {"name": "None", "url": "None", "timeout": "None"}
]

pip_configuration_name = "pip.conf"

ignore_errors = {
    "download": "You should consider upgrading",
    "uninstall": "not an installed pip module"
}

# Download specified modules and dependencies
SUB_CMD_DOWNLOAD = "download"
ARG_DOWNLOAD_MODULE = "module"
ARG_DOWNLOAD_MODULE_SHORT = "m"
ARG_DOWNLOAD_REQUIREMENT = "requirement"
ARG_DOWNLOAD_REQUIREMENT_SHORT = "r"
ARG_DOWNLOAD_REWRITE_PIP_CONFIG = "yes"
ARG_DOWNLOAD_REWRITE_PIP_CONFIG_SHORT = "y"

# Uninstall specified modules and dependencies
SUB_CMD_UNINSTALL = "uninstall"
ARG_UNINSTALL_MODULE = "module"
ARG_UNINSTALL_MODULE_SHORT = "m"
ARG_UNINSTALL_REQUIREMENT = "requirement"
ARG_UNINSTALL_REQUIREMENT_SHORT = "r"
ARG_UNINSTALL_FORCE = "yes"
ARG_UNINSTALL_FORCE_SHORT = "y"

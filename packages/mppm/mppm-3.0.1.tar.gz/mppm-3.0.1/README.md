# mppm

## Introduce

Configure the pypi source repository, support for downloading specified modules or files and its dependent packages.

## My Use Case

The project project is offline and requires downloading the dependent package locally. 
The project project can only be started after the installation of the dependent package is completed.

## Installation

    pip install mppm

## Usage

    usage: mppm  <sub-commands>  [<args>] 

    mppm Manage pip sources and dependent packages
    
    positional arguments:
      {download,uninstall,config}
        download            download modules
        uninstall           uninstall modules
        config              rewrite pip configuration
    
    options:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit

### SubCommand: config
    usage: mppm  <sub-commands>  [<args>] config [-h] [-y]

    options:
      -h, --help  show this help message and exit
      -y, --yes   force rewrite pip configuration

#### examples

    mppm config

### SubCommand: download

    usage: mppm  <sub-commands>  [<args>] download [-h] (-m MODULE | -r REQUIREMENT) [-y]
    
    options:
      -h, --help            show this help message and exit
      -m MODULE, --module MODULE
                            download specified modules and dependencies
      -r REQUIREMENT, --requirement REQUIREMENT
                            download the modules and dependencies specified in the file. like requirements.txt
      -y, --yes             rewrite the pip configuration


  #### examples
    mppm download -m flask  
    mppm download -r /tmp/requiremen.txt

### SubCommand: uninstall

    usage: mppm  <sub-commands>  [<args>] uninstall [-h] (-m MODULE | -r REQUIREMENT) [-y]

    options:
      -h, --help            show this help message and exit
      -m MODULE, --module MODULE
                            uninstall specified modules and dependencies
      -r REQUIREMENT, --requirement REQUIREMENT
                            uninstall the modules and dependencies specified in the file. like requirements.txt
      -y, --yes             interactive

  #### examples
    mppm uninstall -m flask
    mppm download -r /tmp/requiremen.txt -y

## Configuration

You can add package indexes to your `~/.pip/pip.conf` file. Example:

    [global]
    timeout = 120
    index-url = https://pypi.org/simple/
    trusted-host = pypi.org


import time, click, os, sys, shutil, fnmatch, json, shutil
from modules import fs, constants as const

@click.group()
@click.version_option(version='0.0.1', prog_name='Project creator')
@click.option('--name', '-n', default='Yanick le pythonier', help='Creator name')
def main(name):
    click.echo(f'Welcom scripter, developer, programmer and automater {name}')
    config = fs.read_config()
        
    if config['cli_dir'] == None:
        while True:
            cli_path = click.prompt('Enter the path/to/proj_creator map')
            if os.path.exists(cli_path):
                click.secho(('Path added to config file, for any path changes see yanr global_confi --help'), fg=const.CMD_CLR)
                fs.update_configFile('cli_dir', cli_path)
                break
            else:
                click.secho((f'Directory {cli_path} don t exist'), fg=const.ERROR_CLR, bold=True)
    else:
        pass

import time, click, os, sys, shutil, fnmatch, json, shutil
from modules import fs, constants as const

@click.group()
@click.version_option(version='0.0.1', prog_name='Project creator')
@click.option('--name', '-n', default='Yanick le pythonier', help='Creator name')
def main(name):
    click.echo(f'Welcom scripter, developer, programmer and automater {name}')
    config = fs.read_config()
        
    if config['cli_dir'] == None:
        while True:
            cli_path = click.prompt('Enter the path/to/proj_creator map')
            if os.path.exists(cli_path):
                click.secho(('Path added to config file, for any path changes see yanr global_confi --help'), fg=const.CMD_CLR)
                fs.update_configFile('cli_dir', cli_path)
                break
            else:
                click.secho((f'Directory {cli_path} don t exist'), fg=const.ERROR_CLR, bold=True)
    else:
        pass
    
@main.command()
@click.option('--operatingsys', '-os', is_flag=True, help='Your operatingssystem, don t use it in a venv')
def install_yanr(operatingsys):
    """
    Make yanr executable from anywhere in de command line.
    Ex. users/computer/Documents/project_creator>python proj_creator.py install_yanr -os(for linux and mac users)
    if project_creator map is in your Documnnets
    """
    if operatingsys:
        os.system('pip install --editable . --user')
    else:
        os.system('pip install --editable .')

if __name__ == '__main__':
    main()
    
@main.command()
@click.option('--operatingsys', '-os', is_flag=True, help='Your operatingssystem, don t use it in a venv')
def install_yanr(operatingsys):
    """
    Make yanr executable from anywhere in de command line.
    Ex. users/computer/Documents/project_creator>python proj_creator.py install_yanr -os(for linux and mac users)
    if project_creator map is in your Documnnets
    """
    if operatingsys:
        os.system('pip install --editable . --user')
    else:
        os.system('pip install --editable .')
    
from scripts.proj_creator import *
from scripts.bank_cli import *

if __name__ == '__main__':
    main()

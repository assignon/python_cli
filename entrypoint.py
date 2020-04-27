import time, click, os, sys, shutil, fnmatch, json, shutil
from modules import fs, constants as const
from scripts.data_base import DataBase as db
import pandas as pd

@click.group()
@click.version_option(version='0.1.0', prog_name='Project creator')
@click.option('--name', '-n', default='Yanick le pythonier', help='Creator name')
def main(name):
    click.echo(f'Welcom scripter, developer, programmer and automater {name}')
    config = fs.read_config()
        
    if config['cli_dir'] == None:
        # while True:
        #     cli_path = click.prompt('Enter the path/to/proj_creator map')
        #     if os.path.exists(cli_path):
        #         click.secho(('Path added to config file, for any path changes see yanr global_config --help'), fg=const.CMD_CLR)
        #         fs.update_configFile('cli_dir', cli_path)
        #         break
        #     else:
                # click.secho((f'Directory {cli_path} don t exist'), fg=const.ERROR_CLR, bold=True)
        cli_path = os.getcwd()
        const.COFIG_PATH = os.path.join(cli_path, 'global_config.json')
        fs.update_configFile('cli_dir', cli_path)
    else:
        pass


@main.command()  
@click.option('--projectpath', '-pp', help='The path to the project. If is not given initialize yanr in the cwd')
def init(projectpath):
    """
    initialize a project who is not created  with yanr with yanr to be able to use
    yanr inside it
    """
    #check if .yaml file exist in the current foder
    cwd = os.getcwd() #current working dir
    current_dir = os.path.join(cwd, '.yaml')
    if os.paths.exists(current_dir) or os.path.exists(projectpath):
        click.secho(('This project is already inialized with yanr.'), fg=const.INFO_CLR)
    else:
        # click.secho(('Enter the name of the project. Leave it blank if you want to use the folder name as project name.'), fg=const.INFO_CLR)
        # proj_name = click.prompt('Project name:')
        github = click.prompt('Is this project already on GitHub?[y,N]')
        proj_on_github = False
        if github == 'y':
            proj_on_github = True
        else:
            proj_on_github = False
            
        if projectpath == None:
            proj_name = os.path.basename(cwd)
            fs.create_yanr_file(cwd, proj_name, proj_on_github)
            db().insert(
                'projects',
                project_name=proj_name, 
                project_dir=cwd, 
                on_github=0, 
                add_on=datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
            )
        else:
            proj_name = os.path.basename(projectpath)
            fs.create_yanr_file(projectpath, proj_name, proj_on_github)
            db().insert(
                'projects',
                project_name=proj_name, 
                project_dir=projectpath, 
                on_github=0, 
                add_on=datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
            )
            
        click.secho(('Project succesfully initialezed. yanr info to view alle info about the project'), fg=const.SUCCES_CLR)
        #add it to db
            
@main.command()  
@click.option('--projectname', '-pn', help='Get the project by his name')
def list(projectname):
    """
    list all project initialized with yarn out the database
    """
    projects_list = db().select('projects', False).fetchall()
    if projectname == None:
        projects_frame = pd.DataFrame(projects_list, columns = ['ID', 'NAME', 'PATH', 'ADDED_ON_GITHUB', 'ADD_ON'])
        print(projects_frame)
    else:
        conn = db().db_instance()
        get_one = conn.execute("SELECT * from projects WHERE project_name=?", [projectname])
        fetch_project = get_one.fetchone()
        click.secho((f"{fetch_project}"), fg=const.INFO_CLR)
        
@main.command()
@click.option('--projectpath', '-pp', help='Specified the path to the project if yanr not detected in the cwd')
@click.argument('projectname')
def info(projectname):
    """
    return the information(already initialize with yar or not/is already added to git) about the project
    """
    
    
@main.command()
@click.option('--operatingsys', '-os', is_flag=True, help='Your operatingssystem, don t use it in a venv')
def install_yanr(operatingsys):
    """
    Make yanr executable from anywhere in the command line.
    Ex. users/computer/Documents/project_creator>python entrypoint.py install_yanr -os(for linux and mac users)
    if cli_creator map is in your Documnnets
    """
    #ask the user to give the path to the cli_creator(not optional)
    #the default project path(opt)
    #git username and password(opt)
    if operatingsys:
        os.system('pip install --editable . --user')
    else:
        os.system('pip install --editable .')
        
    db().create_tables()
    click.secho(("Github credentials,do it later? Check yanr global-config --help"), fg=const.INFO_CLR)
    usrname = click.prompt("Github username")
    passwrd = click.prompt("Github psswrd")
    db().insert('config', cli_dir=os.getcwd(),
                github_username=usrname, github_password=passwrd, add_on=const.NOW)
        
    
from scripts.proj_creator import *
from scripts.bank_cli import *

if __name__ == '__main__':
    main()

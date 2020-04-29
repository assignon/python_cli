import time, click, os, sys, shutil, fnmatch, json, datetime
from modules import fs, constants as const, github_web as gw
from entrypoint import main
from scripts.data_base import DataBase as db
from scripts.models import Projects
            
def terminate_proces():
    """
    set project_dir, current_project_dir and yanr_init to null when project added succesfully to git,
    then yanr can be reused to create another project
    """
    pass
    # config = fs.read_config()
    # fs.update_configFile('current_project_dir', None)
    # fs.update_configFile('project_name', None)
    # fs.update_configFile('yanr_init', False)
        
def create_with_git(path):
    user_input = click.prompt('Add the project directly to GitHub?[y/N]')
    if user_input == 'y':
        click.secho(('enter a repository name or leave it blank if you want to use the project name as repository name.'), fg=const.INFO_CLR)
        repo_name = click.prompt('Repo name')
        os.chdir(path)
        if repo_name != None:
            os.system(f'yanr git-repo add -rn {repo_name} -rm')
        else:
            os.system(f'yanr git-repo add -rn {os.path.basename(path)} -rm')
        click.secho(('project added to github.'), fg=const.SUCCES_CLR)
    else:
        click.secho(('yanr git-repo --help'), fg=const.CMD_CLR)
        click.secho(('for more information about how to added your project to github.'), fg=const.INFO_CLR)

def python_frameworksBasic_install():
    #install virtual env
    os.system('pip install pipenv')
    #activate virtual env
    os.system('exit') #exit Venv if it already actvated
    # os.system('pipenv lock --clear')
    
def create_pipfile(path, pkg):
    #if for any reason pipfile and pipfile.lock does'n appear in the project
    #directory this function will create it and install the dependenties
    if os.path.exists(path):
        pass
    else:
        os.system(f'pipenv install {pkg}')
    
def vue_init(proj_name, osys):
    user_package = click.prompt('Vue cli need a package manager to be installed. Do you wanna installed with NPM or YARN? [npm/yarn]')
    while True:
        if user_package == 'npm':
            if osys:
                os.system('sudo npm install -g @vue/cli')
                os.system('vue create {}'.format(proj_name))
            else:
                os.system('sudo npm install -g @vue/cli')
                os.system('vue create {}'.format(proj_name))
            break
        elif user_package == 'yarn':
            if osys:
                os.system('sudo yarn global add @vue/cli')
                os.system('vue create {}'.format(proj_name))
            else:
                os.system('yarn global add @vue/cli')
                os.system('vue create {}'.format(proj_name))
            break
        else:
            click.secho(('Command not recognize, you have to choose npm or yarn.'), fg=const.ERROR_CLR)


@main.group(chain=True)
# @click.option('--hashtype', type=click.Choice(['MD5', 'SHA1'], case_sensitive=False))
@click.argument('proj_name')
@click.option('--path', '-pa', help='Path of the directory where the project gona be stored')
@click.option('--operatingsys', '-os', is_flag=True, help='Give this option if your OS is Linux base distribution, it will install the packages with sudo')
@click.pass_context
def create(ctx, proj_name, path, operatingsys):

    """
    \b
    create cmd optional arguments:
    \b
    -dj (create a django base project):
        # --packages, -p   : Install additional packages (max=2). See also yanr packages --help for more information about packages install
        
        # --req, -rq       : (default=requirements.txt)  pip freeze all your dependenties in a txt file, the default is requirements.txt, specify this option when you want another name. 
        
        # --frontend, -fr  : (default=False)  Install vue.js as frontend framework in django project if it is specify.  
        
        # --drestapi, -dra : Initialize the django project with a given restfull api framework.
    \b  
    -vue (create a vue.js base project):
        # No optional option
    \b
    -scrp (create a simple python scripting project):
        # No optional option
    """

    ctx.ensure_object(dict) #send data to nested command
    # config = fs.read_config()
    ctx.obj['operatingsys'] = operatingsys
    ctx.obj['proj_name'] = proj_name
    # if config['yanr_init']:
    #     click.secho(('The {} project is already initialized but not yet added to Git'.format(config['project_name'])),fg=const.INFO_CLR, bg='white')
    #     click.secho(('yanr git_repo --help for more information'.format(config['project_name'])),fg=const.CMD_CLR)
    #     click.secho(('Or you have to terminate the ongoing proces to be able to create a new project.'),fg=const.INFO_CLR, bg='white')
    #     click.secho(('yanr terminate --help for more information'),fg=const.CMD_CLR)
    #     # user_input = click.prompt('Are you sure you don t want to add the current project to Git? [y/N]:')
    #     # if user_input == 'y':
    #     #     os.chdir(os.path.join(config['cli_dir'], const.CLI_NAME))
    #     #     terminate_proces()
    #     # elif user_input == 'N':
    #     #     sys.exit('See yanr git_repo --help for more detail')
    #     # else:
    #     #     click.secho(('Command don t exist'), fg=const.ERROR_CLR, bold=True)
    #     sys.exit()
    # else:
    #     if path == None and config['project_dir'] == None:
    #         path = click.prompt('Enter the path to the directory where you want the project to be stored')
    #         fs.store_dataIn_configFile(ctx, path, proj_name)
    #         default_path = click.prompt('Do you wanna use this path als defalt project path?[y/N')
    #         if default_path == 'y':
    #             fs.update_configFile('project_dir', path )
    #         else:
    #             pass
    #     elif config['project_dir'] != None:
    #         fs.store_dataIn_configFile(ctx, config['project_dir'], proj_name)
    #     elif path != None:
    #         fs.store_dataIn_configFile(ctx, path, proj_name)
    
    if path == None:
        ctx.obj['path'] = os.getcwd()
    #     path = click.prompt('Enter the path to the directory where you want the project to be stored')
    #     fs.store_dataIn_configFile(ctx, path, proj_name)
    #     default_path = click.prompt('Do you wanna use this path als defalt project path?[y/N')
    #     if default_path == 'y':
    #         fs.update_configFile('project_dir', path )
    #     else:
    #         pass
    # elif config['project_dir'] != None:
    #     fs.store_dataIn_configFile(ctx, config['project_dir'], proj_name)
    else:
        # fs.store_dataIn_configFile(ctx, path, proj_name)
        if fs.check_path(path, False):
            ctx.obj['path'] = path
    
@create.command('dj')
# @click.option('--packages', '-pk', nargs=2, default='basic', help='Install additional packages (max=2). See also yanr packages --help for more information about packages install')
@click.option('--req', '-rq', default='requirements.txt', help='pip freeze all your dependenties in a txt file, the default is requirements.txt, specify this option when you want another name.')
@click.option('--frontend', '-fr', is_flag=True, help='Install vue.js as frontend framework in django project if it is specify.')
@click.option('--drestapi', '-dra', help='Initialize the django project with a given restfull api framework.')
@click.pass_context
def django(ctx, req, frontend, drestapi):
    """
    This command create a Django project with or without Vue.js.
    """
    # config = fs.read_config()
    # pipfile_path = os.path.join(config['current_project_dir'], config['project_name']+'/Pipfile')
        
    proj_name = ctx.obj['proj_name']
    project_dir = ctx.obj['path'] #project parent path
    operatingsys = ctx.obj['operatingsys']
    #check the existing of the project folder
    fs.check_path(os.path.join(project_dir, proj_name), True)
    #create project directory
    os.mkdir(os.path.join(project_dir, proj_name))
    os.chdir(os.path.join(project_dir, proj_name))
    click.secho(('Project Directory create succesfully'), fg=const.SUCCES_CLR, bold=True)
    
    python_frameworksBasic_install()
    os.system('pipenv install django')
    # a implementer, si le nom du proj contient (-) le remplace avec (_)
    os.system(f'pipenv run django-admin startproject {proj_name}')
    #initialize project with fronted framework
    if frontend:
        os.system('pipenv install djangorestframework')
        current_project_dir = os.path.join(project_dir, proj_name)
        os.chdir(os.path.join(current_project_dir, proj_name))
        vue_init('frontend', operatingsys)
    #initialize project as a restfull api
    if drestapi != None:
        os.system(f'pipenv install {drestapi}')

    os.system(f'pipenv run pip freeze > {req}')
    #create a track file or identifier file for project
    fs.create_yanr_file(os.path.join(project_dir, proj_name), proj_name, False)
    Projects().insert(
        proj_name, 
        os.path.join(project_dir, proj_name), 
        0
    )
    create_with_git(os.path.join(project_dir, proj_name))
    

# @create.command('-fl')
# @click.option('--packages', '-pk', nargs=2, default='basic', help='Install additional packages (max=2). See also yanr packages --help for more information about packages install')
# @click.option('--req', '-rq', default='requirements.txt', help='pip freeze all your dependenties in a txt file, the default is requirements.txt, specify this option when you want another name.')
# @click.option('--frestapi', '-fra', help='Initialize the flask project with a given restfull api framework.')
# @click.pass_context
# def flask(ctx, packages, req, frestapi):
    # """
    # This command create a Flask project.
    # """
    # proj_name = ctx.obj['proj_name']
    # fs.check_path(ctx.obj['proj_name'], ctx.obj['path'])
    # python_frameworksBasic_install()
    
    # if packages == 'basic':
    #     os.system('pip install Flask')
    #     if frestapi:
    #         os.system(f'git clone {}')
    #     else:
    #         os.system(f'git clone {}')
    # else:
    #     os.system('pipenv install Flask')
    #     if frestapi:
    #         os.system(f'git clone {}')
    #     else:
    #         os.system(f'git clone {}')
    #     #install user given packages
    #     for package in packages:
    #         os.system(f'pipenv install {package}')
    # os.system(f'pipenv run pip freeze > {req}')
    # create_with_git()

@create.command('vue')
@click.pass_context
def vue(ctx):
    """
    This command initialize a Vue.js project.
    """
    proj_name = ctx.obj['proj_name']
    project_dir = ctx.obj['path'] #project parent path
    fs.check_path(os.path.join(project_dir, proj_name), True)
    #create project directory
    os.mkdir(os.path.join(project_dir, proj_name))
    os.chdir(os.path.join(project_dir, proj_name))
    
    vue_init(proj_name, ctx.obj['operatingsys'])
    fs.create_yanr_file(os.path.join(ctx.obj['path'], ctx.obj['proj_name']), ctx.obj['proj_name'], False)
    Projects().insert(
        proj_name, 
        os.path.join(project_dir, proj_name),
        0, 
    )
    create_with_git(os.path.join(project_dir, proj_name))

@create.command('scrp')
@click.option('--scriptpath', '-sp', help='Specify the path to the directory where you want your project to be stored.')
@click.option('--project', '-p', is_flag=True, help='if true create a folder with python file in, if false just create a file in the cwd.')
@click.pass_context
def scripting(ctx, scriptpath, project):
    """
    This command create a simple scripting project.
    """
    proj_name = ctx.obj['proj_name']
    path = None
    if scriptpath == None:
        fs.check_path(os.path.join(os.getcwd(), project), False)
        path = os.getcwd()
    else:
        fs.check_path(os.path.join(scriptpath, proj_name), False)
        path = scriptpath
        
    data = """
        import time, click, os, sys, shutil, fnmatch, json, shutil
        from modules import fs, constants as const
        from entrypoint import main
            
        @main.command()
        def {}():
        print('bank api')
    """.format(proj_name)
    
    try:
        if project == None:
            with open(os.path.join(path, proj_name+'.py'), 'w') as f:
                f.write(data)
        else:
            os.mkdir(os.path.join(path, proj_name))
            os.chdir(os.path.join(path, proj_name))
            parent_dir = os.path.join(path, proj_name)
            with open(os.path.join(parent_dir, proj_name+'.py'), 'w') as f:
                f.write(data)
            Projects().insert(
                proj_name, 
                parent_dir,
                0, 
            )
            create_with_git(parent_dir)
    except FileExistsError as e:
        click.secho((e), fg=const.ERROR_CLR)
    # terminate_proces()
    click.secho(('Script project created'), fg=const.SUCCES_CLR)
        
    # python_frameworksBasic_install()
    # os.system('pipenv install Click')
    # os.system('pipenv install selenium')
    # os.system('pipenv install setuptools')
    # create_with_git()
    
@create.command('pkg')
@click.option('--packgmanager', '-pm', help='specify the package manager to use(ex: npm, pip etc..) depending on the language')
@click.argument('packgs', nargs=-1)
def packages(packgs):
    """
    Install additional packages
    yanr pkg --help for more information about packages install
    """
    for package in packgs:
        os.system(f'pipenv install {package}')

@main.group()
@click.option('--username', '-u') # help='GitHub username'
@click.option('--password', '-p', hide_input=True)
@click.pass_context
def git_repo(ctx, username, password):
    """
    Add your project to GitHub
    \b
    git-repo commands optionals arguments
    \b
    add (create a new GitHub repository and add the project to it):
        # --repositoryname, -rn : let you choose a name for your new github repository, if you don't specify it the project name is used as name for the new repository
        
        # --readme, -rm         : Initialize your repository with a readme
        
        # --commit, -cm         : The first commit (default=First commit)
    \b
    del (delete the given repository name from GitHub):
        # reponame : Is an argument not optional, it has to be specified
    """
    ctx.ensure_object(dict)
    # ctx.obj['repoName'] = repoName
    ctx.obj['username'] = username
    ctx.obj['password'] = password

@git_repo.command('add')  
@click.option('--repositoryname', '-rn', help='let you choose a name for your new github repository, if you don t specify it the project name is used as name for the new repository') # help='Use project name store in config file when no name specify'
@click.option('--readme', '-rm', is_flag=True, help='Initialize your repository with a readme')
@click.option('--commit', '-cm', default='First commit', help='The first commit (default=First commit)')
@click.pass_context
def create_repo(ctx, repositoryname,  readme, commit):
    """[summary]

    Arguments:
        ctx {[dict]} -- [variables from parent]
        repositoryname {[str]} -- [name of repository]
        readme {[bool]} -- [add a readme if true]
        commit {[str]} -- [first commit]
    """
    # config = fs.read_config()
    
    if os.path.exists(os.path.join(os.getcwd(), '.yaml')):
        repository_name = gw.get_repo_name(repositoryname, os.path.join(os.getcwd(), '.yaml'))
        #get github username and password from the config table
        config_data = db().select('config', False).fetchone()
        if config_data[2] == None and config_data[3] == None:
            # gw.git_automation(repository_name, ctx.obj['username'], ctx.obj['password'], readme, commit)
            if ctx.obj['username'] == None and ctx.obj['password'] == None:
                username_input = click.prompt('Github username')
                pass_input = click.prompt('Github password')
                gw.git_automation(repository_name, username_input, pass_input, readme, commit)
            elif ctx.obj['password'] == None and ctx.obj['password'] != None:
                username_input = click.prompt('Github username')
                gw.git_automation(repository_name, username_input, ctx.obj['password'], readme, commit)
            elif ctx.obj['password'] != None and ctx.obj['password'] == None:
                pass_input = click.prompt('Github password')
                gw.git_automation(repository_name, ctx.obj['username'],pass_input, readme, commit)
            else:
                gw.git_automation(repository_name, ctx.obj['username'],ctx.obj['password'], readme, commit)
        else:
            click.secho(('4'), fg=const.ERROR_CLR)
            gw.git_automation(repository_name, config_data[2], config_data[3], readme, commit)
    else:
        click.secho(('None project initialize or project is deleted.'), fg=const.ERROR_CLR, bold=True)
        click.secho(('yanr list'), fg=const.CMD_CLR)+\
        click.secho((' to list all existing project'), fg=const.INFO_CLR)
        
        click.secho(('yanr init'), fg=const.CMD_CLR)+\
        click.secho((' to initialize the current working directory'), fg=const.INFO_CLR)
        
        click.secho(('yanr create --help'), fg=const.CMD_CLR)+\
        click.secho((' ,for more information about creating a new project'), fg=const.INFO_CLR)

    
# abort callback for dangereous action(delete)
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@git_repo.command('del')
@click.argument('reponame') # help='Use project name store in config file when no name specify'
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='Are you sure you want to remove the current repository from GitHub?')
@click.option('--password', '-p', prompt='GitHub password', hide_input=True)
@click.pass_context
def delete_repo(ctx, reponame, password):
    """
    delete the given repository name from GitHub
        # reponame : Is an argument not optional, it has to be specified
    """
    git_path = os.path.join(os.getcwd(), '.git')
    if os.path.exists(git_path):
        if ctx.obj['username'] == None:
            user_name = click.prompt('GitHub username')
            gw.del_repo(user_name, password, reponame)
        else:
            gw.del_repo(ctx.obj['username'], password, reponame)
        try:
            shutil.rmtree(git_path)
            click.secho(('Git unlinked from project'), fg=const.INFO_CLR)
        except OSError as e:
            print('Directory not founded')
    else:
        click.secho(('This project is not initialize with git.'), fg=const.ERROR_CLR)

# @main.command()
# @click.argument('reponame') # help='Use project name store in config file when no name specify'
# @click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='Are you sure you want to remove the current project from your computer and GitHub?')
# def remove(reponame):
#     """
#     Remove project from local computer en Github
#     """
#     pass
    
@main.command()
@click.option('--username', '-u', help='GitHub username') #help='GitHub username'
@click.option('--password', '-p', help='GitHub password')
@click.option('--yanrdir', '-yd', help='path to the cli creator')
def global_config(username, password, yanrdir):
    """
    Set your Github username, password  the directory where you want your projects to be stored as default
    and your favorite EDI and browser so that your project automatically ope in the browser or IDE once created
    so you don't have to do it anytime you create a new project. 
    """
    if username != None:
        db().update('config', 1, github_username=username, add_on=const.NOW)
        click.secho(('github username updated...'), fg=const.SUCCES_CLR)
        
    if password != None:
        db().update('config', 1, github_password=password, add_on=const.NOW)
        click.secho(('github password updated...'), fg=const.SUCCES_CLR)
        
    if yanrdir != None:
        db().update('config', 1, cli_dir=yanrdir, add_on=const.NOW)
        click.secho(('cli creator path updated...'), fg=const.SUCCES_CLR)

    # config = fs.read_config()
    # if username != None and password != None and projectdir != None:
    #     fs.update_configFile('username', username)
    #     fs.update_configFile('password', password)
    #     fs.update_configFile('project_dir', projectdir)
    # else:
    #     click.secho(('None of the option is given, see'), fg=const.INFO_CLR)
    #     click.secho(('yanr global_config --help'), fg=const.CMD_CLR)
    #     click.secho(('for more information'), fg=const.INFO_CLR)
        
# @main.command()
# def go():
#     """
#     implemente with a db, it wil get all your project created with yanr and go to it in the cmd
#     it will also reinialize the project to been used again with yanr en open it in a browser (if it is a web project)
#     and in your default text editor or given
#     """
    
    
@main.command()
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='Are you sure you want to terminate? You can t use yanr for this project anymore')
def terminate():
    """
    Remove .yaml of the project
    """
    # click.secho(('Yanr is deactivate from this project.'), fg=const.INFO_CLR)
    pass
    
    
# from bank_cli import *
# if __name__ == '__main__':
#     main()

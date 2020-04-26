import time, click, os, sys, shutil, fnmatch, json, shutil
import yaml
import modules.constants as const

def check_dir(name, path, directory):
    if os.path.isdir(os.path.join(path, name)):
        click.secho(('Directory already exist'), fg=const.ERROR_CLR, bold=True)
        os.system('yanr terminate')
        sys.exit('Abort')
    else:
        if directory:
            os.mkdir(os.path.join(path, name))
            os.chdir(os.path.join(path, name))
        click.secho(('Project Directory create succesfully'), fg=const.SUCCES_CLR, bold=True)
        
def check_path(proj_name, path, directory):
    status = False
    if os.path.exists(path):
        check_dir(proj_name, path, directory)
        status = True
    else:
        status = False
        click.secho((f'Directory {path} don t exist choose another'), fg=const.ERROR_CLR, bold=True)
        while True:
            project_path = click.prompt('Enter your path')
            if os.path.exists(project_path):
                check_dir(proj_name, project_path, directory)
                status = True
                break
            else:
                status = False
                click.secho((f'Directory {project_path} don t exist choose another'), fg=const.ERROR_CLR, bold=True)
    return status

def update_configFile(key, value):
    try:
        with open (const.CONFIG_PATH, 'r') as f:
            data = json.load(f)
            # print(data['project_dir'])
            data[key] = value
            with open(const.CONFIG_PATH, 'w') as fw:
                json.dump(data, fw)
    except FileNotFoundError as e:
        print(e)
        user_path = click.prompt('Enter the path to the python_cli folder')
        
def update_yamlFile(path, key, value):
    try:
        with open (path, 'r') as f:
            data = yaml.full_load(f)
            # print(data['project_dir'])
            data[key] = value
            with open(path, 'w') as fw:
                yaml.dump(data, fw)
    except FileNotFoundError as e:
        print(e)
        user_path = click.prompt('Enter the path to the python_cli folder')
            
def read_config():
    try:
        with open(const.CONFIG_PATH, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError as e:
        print(e)
        user_path = click.prompt('Enter the path to the python_cli folder')
        
def read_yaml(path):
    try:
        with open(path, 'r') as f:
            config = yaml.full_load(f)
        return config
    except FileNotFoundError as e:
        print(e)
        user_path = click.prompt('Enter the path to the python_cli folder')

def store_data(ctx, path, proj_name):
    ctx.obj['proj_name'] = proj_name
    ctx.obj['path'] = path
    #update config file
    # update_configFile('project_name', proj_name)
    # update_configFile('yanr_init', True)
    if path != None:
        ctx.obj['path'] = path 
        update_configFile('project_dir', path)
        # update_configFile('current_project_dir', os.path.join(path, proj_name))
    else:
        user_path = click.prompt('Enter the path to the directory where you want the project to be stored')
        update_configFile('project_dir', user_path)
        # update_configFile('current_project_dir', os.path.join(user_path, proj_name))
        ctx.obj['path'] = user_path 
            
def store_dataIn_configFile(ctx, path, proj_name):
    config = read_config()
    if os.path.exists(path):
        store_data(ctx, path, proj_name)
    else:
        #if the path don't exist, the project are been sended to
        #the framework function and is checked again with the fs.check_path function.
        store_data(ctx, path, proj_name)
        
def create_yanr_file(path, proj_name, on_github):
    with open(os.path.join(path, '.yaml'), 'w') as f:
        proj_data = {
            'project_name': proj_name,
            'project_dir': path,
            'on_github': on_github,
            'repository_name': None
        }
        yaml.dump(proj_data, f)
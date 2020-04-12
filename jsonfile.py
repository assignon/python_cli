import json
import click, os, subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import entrypoint

# # --| Setup
# options = Options()
# options.add_argument("--headless")
# caps = webdriver.DesiredCapabilities().FIREFOX
# caps["marionette"] = True
# browser = webdriver.Firefox(firefox_options=options, capabilities=caps, executable_path=r"./geckodriver")
# # browser = webdriver.Firefox(executable_path='./geckodriver')
# #--| Parse
# browser.get('https://duckduckgo.com')
# logo = browser.find_elements_by_css_selector('#logo_homepage_link')
# print(logo[0].text)

# with open('global_config.json', 'r') as f:
#     data = json.load(f)
#     print(data['project_dir'])
#     data['project_dir'] = '/home/yanick.py/Dev'
#     with open('global_config.json', 'w') as fw:
#         json.dump(data, fw)

# with open('global_config.json', 'r') as f:
#         config = json.load(f)

# try:
#     os.rmdir(os.path.join(config['current_project_dir'], '.git'))
#     click.secho((config['current_project_dir']), fg='red')
#     click.secho((os.path.join(config['current_project_dir'], '.git')), fg='red')
#     click.secho(('Git unlinked from project'), fg='blue')
# except OSError as e:
#     click.secho((os.path.join(config['current_project_dir'], '.git')), fg='red')
#     click.secho((config['current_project_dir']), fg='red')
#     print('Directory not founded')

# try:
#     os.system('yarn add axios')
# except Exception as error:
#     print('hallo there')

# def read_config():
#     with open('global_config.json', 'r') as f:
#         config = json.load(f)
#     return config
# config = read_config()
# print(config['username'])

# print(os.getcwd())

# @click.command()
# @click.option('--expl', '-e', is_flag=True)
# def test(expl):
#     print(expl)
    
# test()

# subprocess.call('start', shell=True)

# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
# driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

# click.secho(('hallo there'), fg='cyan')

# fullpath = os.path.abspath('global_config.json')
# print(fullpath)

# entrypoint.main()

#  entry_points=''' 
#         [console_scripts]
#         yanr=proj_creator:main
#         yanr=bank_cli:main
#     '''

# entry_points={
#         "console_scripts": [
#             "yanr=proj_creator:main", "yanrb=bank_cli:main"
#         ]
#     }

# with open('test.py', 'w') as f:
#     data = """
#         import time, click, os, sys, shutil, fnmatch, json, shutil
#         from modules import fs, constants as const
#         from entrypoint import main
            
#         @main.command()
#         def {}():
#         print('bank api')
#     """.format('newname')
#     data = f.write(data)

    # print(data)
    # data['project_dir'] = '/home/yanick.py/Dev'
    # with open('global_config.json', 'w') as fw:
    #     json.dump(data, fw)
    
# with open('modules/constants.py', 'r') as fr:
#     new_file_content = ''
#     data = fr.readlines()
#     print(data[6])
#     # for line in fr:
#     #   stripped_line = line.strip()
#     #   print(stripped_line)
#     # new_line = stripped_line.replace("os.path.abspath('global_config.json')", '/home/yanick.py/Dev/cli_creator/global_config.json')
#     # new_file_content += new_line +"\n"
    
#     with open('modules/constants.py', 'w') as fw:
#         try:
#             data[6] = """
#                 CONFIG_PATH = '/home/yanick.py/Dev/cli_creator/global_config.json'
#             """
#             fw.writelines(data[6])
#         except SyntaxError as e:
#             print(e)
    
#         # newpath = data.replace(data[6], CONFIG_PATH = '/home/yanick.py/Dev/cli_creator/global_config.json')
#         print(data[6])
        


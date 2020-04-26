from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import time, click, os, sys, shutil, fnmatch, json, shutil
from modules import fs, constants as const

def get_repo_name(repoName, path):
    config = fs.read_yaml(path)
        
    if repoName == None:
        repoName = config['project_name']
    elif config['project_name'] == None:
        reponame = click.prompt('Enter a repository name')
        fs.update_yamlFile(path, 'project_name', reponame)
        repoName = reponame
    else:
        repoName = repoName
        
    return repoName

def init_with_readMe(browser, readme):
    if readme:
        checkbox = browser.find_element_by_xpath('//*[@id="repository_auto_init"]')
        checkbox.click()
        
def make_repo(browser, commit):
    create_btn = browser.find_element_by_xpath('//*[@id="new_repository"]/div[3]/button')
    create_btn.click()
    config = fs.read_config()
    os.chdir(config['current_project_dir'])
    #add project to GitHub
    os.system('git init')
    os.system('git add .')
    os.system('git commit -m "first commit"')
    os.system('git remote add origin {}'.format(browser.current_url))
    os.system('git remote -v')
    os.system('git push -f origin master')
    os.chdir(os.path.join(config['cli_dir'], const.CLI_NAME))
    click.secho(('Project added succesfully to git'),fg=const.SUCCES_CLR, bold=True)
    time.sleep(5)
    
def add_repo(browser, reponame, readme, commit):
    try:
        newRepo_btn = browser.find_element_by_xpath('/html/body/div[4]/div/aside[1]/div[2]/div[1]/div/h2/a')
        newRepo_btn.click()
        repo_name_input = browser.find_element_by_xpath('//*[@id="repository_name"]') 
        repo_name_input.send_keys(reponame)
        time.sleep(2)
        # repo_exist = browser.find_element_by_css_selector('dd.error')
        try:
            repo_exist = browser.find_element_by_xpath('//*[@id="new_repository"]/div[2]/auto-check/dl/dd[2]') 
            if 'available' in repo_exist.text:
                click.secho(('repo created'),fg=const.INFO_CLR)
                init_with_readMe(browser, readme)
                make_repo(browser, commit)
            else:
                click.secho((repo_exist.text), fg=const.ERROR_CLR)
        except NoSuchElementException as e:
            click.secho(('repo created'),fg=const.INFO_CLR)
            init_with_readMe(browser, readme)
            make_repo(browser, commit)            
    except NoSuchElementException as e:
        pass
        # print(e)
        
def git_automation(reponame, username, password, readme, commit):
    """
    Git site automate with selenium
    """
    
    #--| Setup
    options = Options()
    options.add_argument("--headless")
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps["marionette"] = True
    browser = webdriver.Firefox(firefox_options=options, capabilities=caps, executable_path=r"./geckodriver") #without opening the browser
    # browser = webdriver.Firefox(executable_path='./geckodriver')#penig the browser
    # browser.set_window_size(900, 900)
    browser.get('https://github.com/login')
    
    usrname = browser.find_element_by_xpath('//*[@id="login_field"]')
    usrname.send_keys(username)
    passw = browser.find_element_by_xpath('//*[@id="password"]')
    passw.send_keys(password)
    sign = browser.find_element_by_xpath('//*[@id="login"]/form/div[4]/input[9]')
    sign.click()
   
    try:
        sign_error = browser.find_element_by_xpath('//*[@id="js-flash-container"]/div/div')
        print(sign_error.text)
        add_repo(browser, reponame, readme, commit)
    except NoSuchElementException as e:
        # print(e)
        add_repo(browser, reponame, readme, commit)
        
def del_repo(username, password, repoName):
    #--| Setup
    options = Options()
    options.add_argument("--headless")
    caps = webdriver.DesiredCapabilities().FIREFOX
    caps["marionette"] = True
    browser = webdriver.Firefox(firefox_options=options, capabilities=caps, executable_path=r"./geckodriver") #without opening the browser
    # browser = webdriver.Firefox(executable_path='./geckodriver')
    # browser.set_window_size(900, 900)
    browser.get('https://github.com/login')
    
    usrname = browser.find_element_by_xpath('//*[@id="login_field"]')
    usrname.send_keys(username)
    passw = browser.find_element_by_xpath('//*[@id="password"]')
    passw.send_keys(password)
    sign = browser.find_element_by_xpath('//*[@id="login"]/form/div[4]/input[9]')
    sign.click()
    
    try:
        sign_error = browser.find_element_by_xpath('//*[@id="js-flash-container"]/div/div')
        print(sign_error.text)
    except NoSuchElementException as e:
        time.sleep(2)
        home_page = browser.current_url
        #go to the project repository page
        browser.get(f'{home_page}{username}/{repoName}')
        #go to repository settings
        settings = browser.find_element_by_xpath('//*[@id="js-repo-pjax-container"]/div[1]/nav/a[5]')
        settings.click()
        #delete repository
        time.sleep(5)
        delete_btn = browser.find_element_by_xpath('/html/body/div[4]/div/main/div[2]/div/div/div[2]/div/div[8]/ul/li[4]/details/summary')
        # delete_btn = browser.find_elements_by_class_name('btn-danger')
        delete_btn.click()
        time.sleep(2)
        #confirm delection of the repository
        confirm_input = browser.find_element_by_xpath('//*[@id="options_bucket"]/div[8]/ul/li[4]/details/details-dialog/div[3]/form/p/input')
        confirm_input.send_keys(f'{username}/{repoName}')
        confirm_btn = browser.find_element_by_xpath('//*[@id="options_bucket"]/div[8]/ul/li[4]/details/details-dialog/div[3]/form/button')
        confirm_btn.click()
        click.secho((f'Repository {repoName} delected succesfully'), fg=const.SUCCES_CLR)
        
# gw.git_automation('test', 'assignon', '', True, 'First commit')
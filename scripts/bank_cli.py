import time, click, os, sys, shutil, fnmatch, json, shutil
from modules import fs, constants as const
from entrypoint import main
    
@main.command()
def ing():
    print('bank api')
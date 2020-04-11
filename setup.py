from setuptools import setup

setup(
    name='yanr',
    version='0.01',
    py_modules=[
        'scripts.proj_creator',
        'scripts.bank_cli'
    ],
    # find_packages()
    install_requires=['Click','selenium',],
    entry_points=''' 
        [console_scripts]
        yanr=entrypoint:main
    '''
)
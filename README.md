# python_cli
CLI make with click and python to automate and create web and scripting project.
Automate pyhon web, scripting ad vue.js project creatng process.

  1. Choose the right framework
  2. Create a virtualenv
  3. Activate your virtual env
  4. Install the framework
  5. Install additional packages for your project
  6. Create a new Github repository
  7. Add your project op GitHub
  
This CLI will automate all that boring proces for you.
Cretae in one command line a new project with a framework in your choice and add it to GitHub without opening your browser.

INSTALLATION:

pull the project frome this repository:
git clone https://github.com/assignon/python_cli

in de command line go in the directory where you pull it
path/to/the/directory/of/python_cli

Run the following command to install it on your machine to be able to run it from everywhere
make sure you are in the python_cli directory in your cmd
for Windows users
python entrypoint.py install-yanr

For Linux and Mac users
python entrypoint.py install-yanr -os
(if you run it from a venv, run it without -os)

Now the installation is done you ca go a head and run it fron everywhere in le cmd with
yanr --help for more information about how you can use it.

CHANGE yanr DEFAULT COMMAND
If you want to change yanr to your own en use something like: mycmmd --help
you can edit the setup.py file in the prthon_cli folder. Just open it in a text editor 
and change the where ever yanr is with your own.

Save the file and run this command from the cmd:
For Windows users:
pip install --editable .

For Mac and Linux users if you are not in a venv:
pip install --editable . --user
(in a venv run it without --user)

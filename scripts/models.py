from scripts.data_base import DataBase
import sqlite3, click, os
import modules.constants as const

class Projects(DataBase):
    
    def __init__(self):
        super().__init__()
        self.conn = super().conn_instance()
        #create projects table if not exist
        self.project_table()
        
    def project_table(self):
        try:
            self.conn.execute('''CREATE TABLE projects
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name   CHAR(50)   NOT NULL,
                    project_dir    CHAR(100)  NOT NULL,
                    repository_name CHAR(100) NOT NULL,
                    on_github      BOOLEAN,
                    folder_id      INT        NOT NULL,
                    add_on         DATETIME
                );
            ''')
        except sqlite3.OperationalError as e:
            print(e)
            
    def insert(self, project_name, project_dir, ongithub):
        """check if a project already exist before adding it to the DB

        Arguments:
            project_name {string} -- [name of the project]
            project_dir {[string]} -- [the path to the project]
            on_github {[boolean]} -- [if the project is host on github]
        """
        query = "SELECT \
        count(*) \
        FROM projects \
        WHERE project_name=? and project_dir=?"
        counts = self.conn.cursor().execute(query, [project_name, os.path.join(project_dir, project_name)]).fetchall()[0]
        self.conn.commit()

        if list(counts)[0] == 0:
            try:
                # folder_record = super().insert('folders', project_folder=project_dir, add_on=const.NOW)
                folder_record = ProjectFolder().insert(project_dir)
            except sqlite3.OperationalError as e:
                print(e)
                ProjectFolder()
                folder_record = super().insert('folders', project_folder=project_dir, add_on=const.NOW)
            super().insert('projects',
                            project_name=project_name,
                            project_dir=os.path.join(project_dir, project_name),
                            repository_name=None,
                            on_github=ongithub, 
                            folder_id=folder_record,
                            add_on=const.NOW)
            self.conn.cursor().close()
        else:
            click.secho((f'The project {project_name} stored in {project_dir} already exist, choose another name or change directory.'), fg=const.ERROR_CLR)
    
    
class Config(DataBase):
    
    def __init__(self):
        super().__init__()
        self.conn = super().conn_instance()
        #create config table if not exist
        self.config_table()
        
    def config_table(self):
        try:        
            self.conn.execute('''CREATE TABLE config
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cli_dir   CHAR(100)   NOT NULL,
                        github_username       CHAR(100)  NOT NULL,
                        github_password       CHAR(100)  NOT NULL,
                        editor                CHAR(100),
                        browser               CHAR(100),
                        add_on                DATETIME 
                    );
                ''')
        except sqlite3.OperationalError as e:
            print(e)
            
            
    def insert(self, cli_dir, username, password):
        query = "SELECT \
        COUNT(*) \
        FROM config"
        counts = self.conn.cursor.execute(query).fetchall()[0]
        if list(counts[0]) == 0:
            super().insert('config', cli_dir=cli_dir,  
                           github_username=username, 
                           github_password=password, 
                           editor=None, 
                           browser=None, 
                           add_on=const.NOW)
        else:
            # click.secho((''), fg=const.ERROR_CLR)
            pass
    
    
class ProjectFolder(DataBase):
    
    def __init__(self):
        super().__init__()
        self.conn = super().conn_instance()
        #create folders table if not exist
        self.project_folder_table()
        
    def project_folder_table(self):
        """folder where the projects are stored.
        """
        try:
            self.conn.execute('''CREATE TABLE folders
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    folder_path  CHAR(100)  NOT NULL,
                    add_on                  DATETIME 
                );
            ''')
        except sqlite3.OperationalError as e:
            print(e)
            
    def insert(self, project_folder):
        counts = super().row_count('folders', folder_path=project_folder)
        folder_id = None
        if counts == 0:
            folder_id = super().insert('folders', folder_path=project_folder, add_on=const.NOW).lastrowid
        else:
            click.secho(('This project folder already exist'), fg=const.ERROR_CLR)
            select_folder = super().select('folders', True, folder_path=project_folder)
            folder_id = select_folder.fetchone()[0]
        return folder_id
            
# print(repr(Projects().conn_instance()))
# proj = Projects()
# proj.insert('fys', '/home/yanick.py/Dev', 0)
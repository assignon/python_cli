import sqlite3, datetime

class DataBase:
    
    def __init__(self):
        self.conn = sqlite3.connect("db.sqlite3")
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE projects
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name   CHAR(50)   NOT NULL,
                project_dir    CHAR(100)  NOT NULL,
                on_github      BOOLEAN,
                add_on         DATETIME
            );
            ''')
        except sqlite3.OperationalError as e:
            print(e)
        self.cursor.close()
        
    def db_instance(self):
        return self.cursor
     
    def select(self, clause, **kwargs):
        """
        @clause(bool): determine if the query is a prepare statement or not
        @kwargs: a dict of the query where conditions
        """
        if clause:
            data = self.cursor.execute("SELECT * from projects WHERE dict(kwargs)")
        else:
            data = self.cursor.execute("SELECT * from projects")
        self.conn.commit()
        return data
        self.cursor.close()
    
    def insert(self, proj_name, proj_dir, github, date_time):
        proj_name = proj_name
        proj_dir = proj_dir
        github = github
        query = (
            "INSERT INTO projects (project_name, project_dir, on_github, add_on) \
            VALUES (?, ?, ?, ?)"
        )
        self.cursor.execute(query, [proj_name, proj_dir, github, date_time])
        self.conn.commit()
        print('record added')
        self.cursor.close()
        
    def drop_db(self, tablename):
        self.cursor.execute("DROP TABLE {}".format(tablename))

# now = datetime.datetime.now()  
# DataBase().create_table()
# DataBase().insert('test', '/home/yanick.py/Dev/test', 0, now.strftime("%Y-%M-%d-%H:%M:%S"))
# for p in DataBase().select(False).fetchall():
#     print(p[0])

# proj = DataBase().db_instance().execute("SELECT * from projects WHERE project_name=?", ['test3'])
# DataBase().db_instance().commit()
# print(proj.fetchone())
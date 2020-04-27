import sqlite3
import datetime


class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect("db.sqlite3")
        self.cursor = self.conn.cursor()
        # self.create_tables()

    def create_tables(self):
        self.project_table()
        self.config_table()
        self.project_folder()
        self.cursor.close()

    def project_table(self):
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

    def config_table(self):
        try:
            self.cursor.execute('''CREATE TABLE config
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cli_dir   CHAR(100)   NOT NULL,
                        github_username       CHAR(100)  NOT NULL,
                        github_password       CHAR(100)  NOT NULL,
                        add_on                DATETIME 
                    );
                ''')
        except sqlite3.OperationalError as e:
            print(e)

    def project_folder(self):
        """folder where the projects are stored.
        """
        try:
            self.cursor.execute('''CREATE TABLE folders
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_folders  CHAR(100)  NOT NULL,
                    add_on                DATETIME 
                );
            ''')
        except sqlite3.OperationalError as e:
            print(e)

    def db_instance(self):
        return self.cursor

    def select(self, table_name, prepare, **kwargs):
        """
        @prepare(bool): determine if the query is a prepare statement or not
        @kwargs: a dict of the query where conditions
        """
        if prepare:
            for row_name, value in kwargs.items():
                data = self.cursor.execute(
                    "SELECT * from {} WHERE {}=?".format(table_name, row_name), [value])
        else:
            data = self.cursor.execute("SELECT * from {}".format(table_name))

        self.conn.commit()
        return data
        self.cursor.close()

    # def insert(self, proj_name, proj_dir, github, date_time):
    def insert(self, table_name, **kwargs):
        """DB insert statement

        Arguments:
            self {[class instance]} -- [reference to current class]
            table_name {string} -- [DB table name]
        """
        rows = []
        vals = []
        for row_name, values in kwargs.items():
            rows.append(row_name)
            vals.append(values)

        self.cursor.execute(
            "INSERT INTO {} {} \
            VALUES {}".format(table_name, tuple(rows), tuple(vals))
        )

        self.conn.commit()
        print('record added')
        self.cursor.close()

    def update(self, table_name, condition, **kwargs):
        """update data in DB

        Arguments:
            table_name {string} -- [DB table name]
            kwargs {[string]} -- [table row name to update]
            condition {[string, int, date, boolean]} -- [new data]
        """
        for row_name, vals in kwargs.items():
            self.cursor.execute("UPDATE {}\
            SET {}=? \
            WHERE id=?".format(table_name, row_name), [vals, condition])

        self.conn.commit()
        print(f"record with id {condition} updated")
        self.cursor.close()

    def delete(self, table_name, condition):
        query = "DELETE from {} where id = ?".format(table_name)
        self.cursor.execute(query, [condition])
        self.conn.commit()
        print(f"record with id {condition} deleted")
        self.cursor.close()

    def drop_table(self, tablename):
        self.cursor.execute("DROP TABLE {}".format(tablename))

# now = datetime.datetime.now()
# DataBase().create_table()
# DataBase().insert('test', '/home/yanick.py/Dev/test', 0, now.strftime("%Y-%M-%d-%H:%M:%S"))
# for p in DataBase().select(False).fetchall():
#     print(p[0])

# proj = DataBase().db_instance().execute("SELECT * from projects WHERE project_name=?", ['test3'])
# DataBase().db_instance().commit()
# print(proj.fetchone())
# DataBase().insert(
#     'projects',
#     project_name='portfolio',
#     project_dir='/home/yanick.py/Dev',
#     on_github=0,
#     add_on=datetime.datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
# )

# DataBase().update('projects', 1, project_name='webshop',
#     project_dir='/home/yanick.py/Documnets'
# )


DataBase().delete('projects', 6)

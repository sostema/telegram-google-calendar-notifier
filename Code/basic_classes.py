import os
import sqlite3


class SQLDatabase:
    def __init__(self, database_name, database_path="../Data/"):
        self.database_path = os.path.join(database_path, str(database_name) + '.sqlite')

    def create_connection(self):
        """ create a database connection to the SQLite database
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.database_path)
        except sqlite3.Error as e:
            pass

        return conn

    def create_table(self, table_name, columns):
        conn = self.create_connection()
        with conn:
            query = f'CREATE TABLE IF NOT EXISTS {table_name} (\n'
            query += f"{columns[0][0]} {columns[0][1]}"
            for column in columns[1:]:
                query += ',\n'
                query += f'{column[0]} {column[1]}'
            query += f'\n);'
            try:
                c = conn.cursor()
                c.execute(query)
            except sqlite3.Error as e:
                pass

    def add_rows(self, table_name, rows):
        conn = self.create_connection()
        with conn:
            for row in rows:
                query = f"INSERT INTO {table_name} VALUES {row}"
                try:
                    c = conn.cursor()
                    c.execute(query)
                except sqlite3.Error as e:
                    pass

    def get_table(self, table_name):
        conn = self.create_connection()
        with conn:
            try:
                c = conn.cursor()
                c.execute(f"SELECT * FROM {table_name}")
                results = c.fetchall()
                return results
            except sqlite3.Error as e:
                pass

    def get_query(self, query):
        conn = self.create_connection()
        with conn:
            try:
                c = conn.cursor()
                c.execute(query)
                results = c.fetchall()
                return results
            except sqlite3.Error as e:
                pass

    def execute_query(self, query):
        conn = self.create_connection()
        with conn:
            try:
                c = conn.cursor()
                c.execute(query)
                conn.commit()
            except sqlite3.Error as e:
                pass

    def check_table_existance(self, table_name):
        query = f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result = self.get_query(query)
        return result[0][0] == 1

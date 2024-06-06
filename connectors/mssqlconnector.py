import pyodbc
import pandas as pd
import traceback


class Connector:
    def __init__(self, server = r'NDMAWPU\NDMAWPU', database= 'Firo_MLBA', username = 'sa', password='ndmawpu'):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

        self.conn = None

    def init_connection(self):
        try:
            connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=" \
                + self.server \
                + ",1433;DATABASE=" \
                + self.database \
                + ";UID=" \
                + self.username \
                + ";PWD=" \
                + self.password
            print(connection_string)
            self.conn = pyodbc.connect(connection_string)
            return self.conn
        except Exception as e:
            self.conn = None
            traceback.print_exc()
        return None
    
    def close_connection(self):
        if self.conn is not None:
            self.conn.close()

    def run_query(self, query):
        conn = self.init_connection()
        data = pd.read_sql(query, conn)
        return data
    
    def execute_query(self, query, params=None):
        conn = self.init_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
        except Exception as e:
            traceback.print_exc()
            return None
        finally:
            self.close_connection()

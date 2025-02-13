import pyodbc
from mysql.connector import MySQLConnection

class BaseRepository:
    def __init__(
        self,
        database_name: str,
        username: str,
        password: str,
        host: str,
        port: str,
        dbms_name: str
    ):
        self.database_name = database_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.dbms_name = dbms_name
    
    def connect(self):
        if self.dbms_name=="SQLServer":
            connection_string = "Driver={ODBC Driver 17 for SQL Server};"+ \
                                f"Server={self.host};"+ \
                                f"Database={self.database_name};"+ \
                                f"UID={self.username};"+ \
                                f"PWD={self.password};"
            print("\nconnection_string =",connection_string)
            conn=pyodbc.connect(connection_string)
        elif self.dbms_name=="MySQL":
            conn = MySQLConnection(user=self.username
                                ,password=self.password
                                ,host=self.host
                                ,port=self.port
                                ,database=self.database_name
                                ,autocommit=True
                                ,connection_timeout=1000)
        return conn


class MainDb(BaseRepository):
    pass

class WasaAiMl(BaseRepository):
    pass

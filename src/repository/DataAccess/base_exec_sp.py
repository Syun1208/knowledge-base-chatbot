from src.repository.DataAccess.data_access_connection import BaseRepository
from typing import List

class SPExecutor:
    def __init__(self,
                 repository: BaseRepository):
        self.repository = repository

    def call_sql_server_sp(self, sp, params, cursor):
        param_placeholders = ', '.join(['?' for _ in params]) 
        param_values = tuple(params)
        query = "{" + f"CALL {sp} (" + param_placeholders + ")}"
        cursor.execute(query, param_values)
        dba_results = []
        dba_results.append(cursor.fetchall())
        while (cursor.nextset()): 
            result = cursor.fetchall()
            if result:
                dba_results.append(result)
            

        if len(dba_results)==1:
            return dba_results[0]
        else:
            return dba_results

    def call_mysql_sp(self, sp, params, cursor):
        cursor.callproc(sp, params)
        dba_results = [r.fetchall() for r in cursor.stored_results()]

        return dba_results
    
    def call_sp(self, conn, cursor):
        try:
            db_results = None
            if self.repository.dbms_name=="SQLServer":
                db_results = self.call_sql_server_sp(self.repository.sp
                                , self.repository.param(), cursor)
            elif self.repository.dbms_name=="MySQL":
                db_results = self.call_mysql_sp(self.repository.sp
                                , self.repository.param(), cursor)
            conn.commit()
            return db_results
        
        except Exception as err:
            raise ValueError(err)
        
    def init_sp_info(self, sp, param):
        self.repository.sp = sp
        self.repository.param = param
        self.repository.output_exception_msg = f" ERROR: Execute SP {sp} failed: "
        self.repository.output_sperror_msg = f" ERROR: Error from SP {sp}: "

    def connect(self):
        self.connection = self.repository.connect() 
        self.cursor = self.connection.cursor()

    def close_connection(self):
        if (self.connection) or (self.main_db_sp_executor is not None):
            self.connection.close()

    def manage_sp_operation(self, sp_name, sp_params):
        ip_param = sp_params()
        self.init_sp_info(sp_name, ip_param)
        with self.repository.connect() as conn:
            with conn.cursor() as cursor:
                sp_result = self.call_sp(conn, cursor)

        return sp_result

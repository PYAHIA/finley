# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 17:14:01 2021

@author: pyahia
"""

import sys
sys.path.append("/usr/local/bin/")
try:
    from pypyodbc import connect, ProgrammingError
except:
    raise Exception(str(sys.path))

import os

_HOST = os.getenv("pgsqlhost")
_PORT = "5432"
_DATABASE = "finley"
_UID = os.getenv("pgsqluid")
_PWD = os.getenv("pgsqlpwd")


class AirConn():
    
    def __init__(self):
        self.reconnect()
        
    def reconnect(self):
        self.conn = connect('DRIVER={'+self.driver+'};SERVER='+_HOST+';DATABASE='+_DATABASE+';UID='+_UID+';PWD='+ _PWD+';Autocommit=True;')
    
    def close(self):
        self.conn.close()
        
    @property
    def driver(self):
        if os.name == 'nt':
            return 'PostgreSQL Unicode(x64)'
        else:
            return  "/usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so"
        
    def execute(self, sql):
        error = None
        res = None
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
        except ProgrammingError as e:
            error = e
        finally:
            cursor.close()
            
        return res, error 
        
    def commit(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("COMMIT;")
        finally:
            cursor.close()
        


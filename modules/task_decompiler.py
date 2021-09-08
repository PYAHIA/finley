# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 23:01:47 2021

@author: pyahia
"""

import os
import sys
if os.name == 'nt':
     sys.path.append(r"C:/Users/pyahia/git/finley/modules")
else:
    sys.path.append( r"opt/airflow/modules")
    
from finley_connection import AirConn

class TaskDecompiler:
    
    def __init__(self, procedure_id):
        self.id = procedure_id
        
    def get_elements(self):
        conn = AirConn()
        
        res, err = conn.execute("SELECT id FROM finley.t_procedure_server;")
        
        if err:
            raise err
            
        self.psid = [x for x in self.res]
        
        conn.close()
        
    def remove_procedure_servers(self, server_id=None):
        conn = AirConn()
        if server_id:
            sql = "DELETE FROM finley.t_procedure_server WHERE procedure_id = %d and server_id = %d" % (int(server_id), int(self.id))
        else:
            sql = "DELETE FROM finley.t_procedure_server WHERE procedure_id = %d" % (int(server_id))
        
        _, err = conn.execute(sql)
        
        if err:
            raise err
        conn.close()
        
    def decompile(self, server_id=None):
        conn = AirConn()
        sql = "DELETE FROM finley.t_procedure WHERE id = %d" % (int(server_id))
        _, err = conn.execute(sql)
        
        if err:
            raise err
        
        conn.close()
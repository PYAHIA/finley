# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 19:13:47 2021

@author: pyahia
"""

import toml
import os
from finley_connection import AirConn
from task_compiler import TaskCompiler
from jinja2 import Template

class TaskConfig:
    
    def __init__(self, subdir):
        self.subdir = subdir
        self.path = self.root_path+os.sep+subdir+os.sep+"config.toml"
        self.contents = toml.load(self.path)
        
        self.conn = AirConn()
        self.gen_parameters()
        self.gen_schedules()
        self.gen_defaults()
        self.start_date=""
        self.end_date=""
        
    def build(self):
        _ , err = self.conn.execute("DELETE FROM finley.toml_parameters WHERE toml_path = '%s' " % (self.subdir))
        if err:
            raise Exception(err)
        self.conn.commit()
        
        for p, v in self.defaults:                
            res, err = self.conn.execute("""
                                         INSERT INTO finley.toml_parameters 
                                         (toml_path, parameter_name, parameter_value)
                                         VALUES ('%s','%s','%s')
                                         """  % (self.subdir, p, v)
                                         )  
        if err:
            raise Exception(err)
        self.conn.commit()
        tasks_in_toml = [ "'"+self.subdir+os.sep+file+"'" for file in os.listdir(self.root_path+os.sep+self.subdir) if not file.endswith(".toml")]
        task_string = ",".join(tasks_in_toml).replace("\\","/")
        #remove existing schedules
        res , err = self.conn.execute("""DELETE FROM finley.tj_procedure_server_schedule t
                                        WHERE EXISTS (
                                        SELECT NULL
                                        FROM finley.t_procedures x
                                        JOIN finley.t_procedure_server xs on xs.procedure_id = x.id
                                        WHERE x.procedure_name IN (%s)
                                        and xs.id =t.procedure_server_id 
                                        ) """ % (task_string))                
        if err:
            raise Exception(err)
        self.conn.commit()
        res, err = self.conn.execute("""
                                    SELECT DISTINCT
                                    procedure_name, ps.server_id
                                    FROM finley.t_procedure_server ps
                                    JOIN finley.t_procedures p on p.id = ps.procedure_id
                                    WHERE procedure_name in (%s)""" % (task_string)
                                    )
        if err:
            raise Exception(err)     
            
        task_server = self.tuple_to_dict(res)

        for schedule in self.schedules:
            for file in tasks_in_toml:
                file = file.replace("\\","/").replace("'","")
                if file in task_server.keys():
                    for server in task_server[file]:
                        TaskCompiler(file).full_build(int(server), int(schedule))

    def gen_schedules(self):
        _schedules = self.contents["METADATA"]["schedules"]
        self.schedules = []
        
        for schedule in _schedules:
            if not schedule.isdigit():
                res, err = self.conn.execute("SELECT id FROM finley.t_schedule WHERE schedule_name = '%s'" % (schedule))
                if err:
                    raise err
                self.schedules.append(res[0][0])
            else:
                self.schedules.append(schedule)
    
    def gen_parameters(self):
        parameters = self.contents["PARAMETERS"]
        start_date = parameters.get("start_date")
        end_date = parameters.get("end_date")
        self.raw_parameters = []
        if start_date:
            self.raw_parameters.append(("start_date", start_date))
        if end_date:
            self.raw_parameters.append(("end_date", end_date))

    def gen_defaults(self):
        parameters = self.contents["DEFAULT"]
        start_date = parameters.get("start_date")
        end_date = parameters.get("end_date")
        self.defaults = []
        if start_date:
            self.defaults.append(("start_date", start_date))
        if end_date:
            self.defaults.append(("end_date", end_date))
            
    @property
    def root_path(self):
        if os.name == 'nt':
            return r"C:/Users/pyahia/git/finley/repos"
        else:
            return r"/opt/airflow/repos"


    def tuple_to_dict(self, raw):
        data = {}
        for k, v in raw:
            if k in data.keys():
                data[k].append(v)
            else:
                data[k] = [v]
        return data
    
    @property
    def parameters(self):
        if not self.start_date == "" and not self.end_date == "": #just check once.
            sql = "SELECT parameter_name, parameter_value FROM finley.toml_parameters  WHERE toml_path = '%s'" % (self.subdir)
            res, err = self.conn.execute(sql)
            if err:
                raise err
            
            data = {k:v for k,v in res}
            config = {k:v for k,v in self.raw_parameters}
            
            start_date_raw = data.get("start_date")
            end_date_raw = data.get("end_date")
            start_date_cfg = config.get("start_date")
            end_date_cfg = config.get("end_date")
            
            if start_date_raw and start_date_cfg:
                self.start_date =Template(end_date_cfg).render(start_date=start_date_raw)
            if end_date_raw and end_date_cfg:
                self.end_date =Template(end_date_cfg).render(start_date=end_date_raw)    
        
        return {'start_date': self.start_date, 'end_date': self.end_date}
        
if __name__ == "__main__":
    tom = TaskConfig(r"dvd-dw/misc")
    tom.build()
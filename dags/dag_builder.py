# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 17:42:36 2021

@author: pyahia
"""

import sys
sys.path.append("/opt/airflow/modules")
sys.path.append("c:/users/pyahia/git/finley/modules")
from finley_connection import AirConn

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import timedelta, datetime
from jinja2 import Template
from toml_handler import TaskConfig
import sqlparse
import os
import re

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


class AirflowDAG:
    """
        This extracts DAG data from godb to build dependency graph for the DAG
    
    """
    def __init__(self, dagid):
        self.get_dependencies(dagid)
    
    def get_dependencies(self,dagid):
        conn = AirConn()

        self._dependencies, err =  conn.execute("SELECT * FROM finley.vw_procedure_dependencies") #TO DO--alter query search just relevant.
        
        if err:
            raise Exception(err)
        
        conn.reconnect()
        self.nodes, err  = conn.execute("SELECT DISTINCT Procedure_Id, Procedure_Name FROM finley.vw_procedure_server_schedule_DAG WHERE schedule_id = '{0}'".format(dagid))
        conn.close()
        
        if err:
            raise Exception(err)

    def build_objects(self):
        self.executables = {} # { procedure_name : PostgresOperator, }
        
        for pid, node in self.nodes:
            with open(self.root_path + os.sep + node, "r") as f:
                contents = f.read()
            sql = sqlparse.split(contents)
            
            subdir, _  = os.path.split(node)
            
            toml = TaskConfig(subdir)
            params = toml.parameters
            start_date = params.get("start_date")
            end_date = params.get("end_date")
            sql = [Template(statement).render(start_date=start_date, end_date=end_date) for statement in sql]
            self.executables[node] = PostgresOperator(
                    task_id = re.findall(".+/(.+.sql)", node)[0],  # str(pid),
                    postgres_conn_id='pgsql',
                    sql = sql
                    )
        
        self.dependencies = [(a,b) for a, b in self._dependencies if a in self.executables.keys()]
        
    @property
    def root_path(self):
        if os.name == "nt":
            return r"C:\Users\pyahia\git\finley\repos"
        else:
            return r"/opt/airflow/repos"



dag_prefix = datetime.now().strftime("%Y%m%d-")

conn = AirConn()
res , _ = conn.execute("SELECT id, schedule_name, cron FROM finley.t_schedule")
for schedule_id, schedule_name, cron in res:
    dagger = AirflowDAG(schedule_id)
    dag_name = dag_prefix + str(schedule_id) + "__" + schedule_name
    
    with DAG(dag_name,
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now(),
            max_active_runs=1,
            schedule_interval=cron,
            default_args=default_args,
            template_searchpath='/opt/airflow/repo', #'/usr/local/airflow/include',
            catchup=False
        ) as dag:
    
        dagger.build_objects()
        for p, s in dagger.dependencies:
            dagger.executables[p] >> dagger.executables[s]
            
        globals()[schedule_name] = dag
conn.close()
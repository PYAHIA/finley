# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 18:43:34 2021

@author: pyahia
"""
from airflow import DAG
from airflow.contrib.operators.postgres_operator import PostgresOperator

from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('postgres_stuff',
         start_date=datetime(2021, 9, 2),
         max_active_runs=3,
         schedule_interval='@daily',
         default_args=default_args,
         template_searchpath='/opt/airflow/repo', #'/usr/local/airflow/include',
         catchup=False
         ) as dag:

         opr_call_sproc1 = PostgresOperator(
             task_id='call_sproc1',
             postgres_conn_id='airflow_pgsql',
             sql='call-sproc1.sql'
         )
         
         opr_call_sproc2 = PostgresOperator(
             task_id='call_sproc2',
             postgres_conn_id='airflow_pgsql',
             sql='call-sproc2.sql'
         )

         opr_call_sproc1 >> opr_call_sproc2
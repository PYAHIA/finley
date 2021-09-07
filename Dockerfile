FROM apache/airflow:2.1.3 

USER airflow
RUN pip install --no-cache-dir --user pypyodbc
RUN pip install --no-cache-dir --user sqlparse

USER root
RUN apt-get update && apt-get install -y apt-transport-https

RUN apt-get update \
    && apt-get install -y curl apt-transport-https \
    && apt-get install -y odbc-postgresql
    #/usr/lib/x86_64-linux-gnu/odbc/psqlodbca.so

RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean

RUN apt-get install -y vim


#cd C:\Users\pyahia\git\finley
#docker exec -it --user airflow finley_airflow-worker_1 bash
#docker exec -it --user root finley_airflow-worker_1 bash



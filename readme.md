### CONFIGURATIONS:
* Install postgres on it's on instance
* In ./finley/pgsql-init edit `finley_agen (TEMPLATE).sh`.
    * Replace `{{EC2 PUBLIC IP}}` with the corresponding IP for the EC2 that Finley will be hosted on

### INITIALIZATION:

Navigate to root directory ./finley/
Execute the following
* `docker-compose up init airflow`
* `docker-compose up --build`
* Open a shell into the container with `docker exec -it --user airflow airflow-docker_airflow-worker_1 bash`
* `cd /opt/airflow/pgsql-init/`
* `./finley_agen.sh` (or what ever you renamed the file to in Step 1)
* This will generate the finley db & sa. 

## ADDING SERVERS:
To add within the Airflow UI add a new connection.
Connect to Finley and run the following:
`INSERT INTO finley.t_server (server_name) ('{SERVER_NAME}')';`
* Make sure the server name matches the name in Airflow

## ADDING SCHEDULES:
`INSERT INTO finley.t_schedule (schedule_name, cron) VALUES ('{SCHEDULE_NAME}','{CRON EXPRESSION}');`
* `schedule_name` is the display on how it will appear in the DAG (ie, "Hourly-business-hours").
* `cron` is a cron-expression for the runtime.

## ADDING TASKS:
* Deploy the scripts to `./finley/repos/`(`/opt/airflow/` in container/shell)
* Compile the script by running 
```python
from task_compiler import TaskCompiler
TaskCompiler('{task_name'}).full_build(server_id, schedule_id)
```











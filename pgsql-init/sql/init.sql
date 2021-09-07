DROP SCHEMA finley CASCADE;
CREATE SCHEMA finley;

CREATE TABLE finley.t_procedures (
	ID INT GENERATED ALWAYS AS IDENTITY,
	Procedure_Name varchar(255) NOT NULL
);

CREATE TABLE finley.t_procedure_server(
	ID int GENERATED ALWAYS AS IDENTITY NOT NULL,
	Procedure_ID int NULL,
	Server_ID int NULL
);

CREATE TABLE finley.t_schedule(
	ID int GENERATED ALWAYS AS IDENTITY NOT NULL,
	schedule_name varchar(255) NULL,
	cron VARCHAR(1000) NULL
);

CREATE TABLE finley.t_server(
	ID int GENERATED ALWAYS AS IDENTITY NOT NULL,
	server_name varchar(50) NULL
);

CREATE TABLE finley.t_source_target(
	ID int GENERATED ALWAYS AS IDENTITY NOT NULL,
	Table_Name varchar(200) NULL
);

CREATE TABLE finley.tj_procedure_server_schedule(
	ID int GENERATED ALWAYS AS IDENTITY NOT NULL,
	procedure_server_id int NOT NULL,
	schedule_id int NOT NULL
);


CREATE TABLE finley.tj_procedure_source(
	ID int GENERATED ALWAYS AS IDENTITY NOT NULL,
	Procedure_ID int NOT NULL,
	Source_ID int NOT NULL
);

CREATE TABLE finley.tj_procedure_target(
	ID int GENERATED ALWAYS AS IDENTITY NOT NULL,
	Procedure_ID int NOT NULL,
	Target_ID int NOT NULL
)
;

CREATE OR REPLACE VIEW finley.vw_procedure_dependencies AS 
	SELECT 
		pt.Procedure_Name as Upstream,
		ps.Procedure_Name  as Downstream
	FROM finley.tj_procedure_target jpt 
	JOIN finley.tj_procedure_source jps  ON jps.Source_ID = jpt.Target_ID --match sources t- targets
	JOIN finley.t_procedures pt ON pt.id = jpt.Procedure_ID
	JOIN finley.t_procedures ps ON ps.id = jps.Procedure_ID
;

DROP VIEW finley.vw_procedure_server_schedule_DAG;
CREATE OR REPLACE VIEW finley.vw_procedure_server_schedule_DAG AS 
SELECT
	schedule_id,
	p.id as Procedure_Id,
	Procedure_Name
FROM finley.tj_procedure_server_schedule as pss
	JOIN finley.t_procedure_server as ps  on ps.id = pss.procedure_server_id
	JOIN finley.t_procedures as p on p.id = ps.procedure_id
	JOIN finley.t_schedule as s on s.id = pss.schedule_id
;


INSERT into finley.t_schedule (schedule_name, cron)
VALUES ('Every_15mins--_from_8am-4pm','YYYYMMDD-01','*/15 8-16 * * *');

INSERT into finley.t_schedule (schedule_name, cron)
VALUES ('Hourly','YYYYMMDD-02','37 0-23 * * *');

INSERT into finley.t_schedule (schedule_name, cron)
VALUES ('8pm_Daily', '0 8 * * *');

INSERT into finley.t_schedule (schedule_name, cron)
VALUES ('Every_three_hours--business_hours','0 9-18/3 * * *');

INSERT INTO  finley.t_server (server_name)
VALUES ('pgsql'); --this must match the airflow connection settings

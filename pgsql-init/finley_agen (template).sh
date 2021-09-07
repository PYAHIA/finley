source ~/.bashrc

if [ -z ${pgsqlpwd+x} ]; then echo export pgsqlpwd=\"$(head -c 16  /dev/random | md5sum | cut -f 1 -d\ )\" >> ~/.bashrc; else echo "var is set"; fi 
if [ -z ${pgsqluid+x} ]; then echo export pgsqluid=\"finleysa\" >> ~/.bashrc; else echo "var is set"; fi 
if [ -z ${pgsqlhost+x} ]; then echo export pgsqlhost=\"{{EC2 PUBLIC IP}}\" >> ~/.bashrc; else echo "var is set"; fi


source ~/.bashrc

su - airflow -c "echo export pgsqlpwd=$pgsqlpwd"
su - airflow -c "echo export pgsqluid=$pgsqluid"
su - airflow -c "echo export pgsqlhost=$pgsqlhost"

ssh -i /opt/airflow/ssh/finley.pem ubuntu@$pgsqlhost "echo chmod 777 /opt/ "

ssh -i /opt/airflow/ssh/finley.pem  ubuntu@$pgsqlhost <<EOF 
echo chmod 777 /opt/ 
echo export pgsqlpwd=$pgsqlpwd >> /opt/.pgsqlcreds
echo export pgsqluid=$pgsqluid >> /opt/.pgsqlcreds
sudo su postgres
source /opt/.pgsqlcreds
psql -c "create role $pgsqluid with login password '$pgsqlpwd'"
EOF

scp -i /opt/airflow/ssh/finley.pem /opt/airflow/pgsql-init/sql/finley_init.sql ubuntu@$pgsqlhost:/opt/





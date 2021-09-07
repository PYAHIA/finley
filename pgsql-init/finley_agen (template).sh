source ~/.bashrc

if [ -z ${pgsqlpwd+x} ]; then echo export pgsqlpwd=\"$(head -c 16  /dev/random | md5sum | cut -f 1 -d\ )\" >> ~/.bashrc; else echo "var is set"; fi 
if [ -z ${pgsqluid+x} ]; then echo export pgsqluid=\"finleysa\" >> ~/.bashrc; else echo "var is set"; fi 
if [ -z ${pgsqlhost+x} ]; then echo export pgsqlhost=\"{{EC2 PUBLIC IP}}\" >> ~/.bashrc; else echo "var is set"; fi

source ~/.bashrc

ssh -i /opt/airflow/ssh/finley.pem -y  ubuntu@$pgsqlhost "sudo echo export pgsqlpwd=$pgsqlpwd >> /opt/.pgsqlcreds"
ssh -i /opt/airflow/ssh/finley.pem -y  ubuntu@$pgsqlhost "sudo echo export pgsqluid=$pgsqluid >> /opt/.pgsqlcreds"

sudo su postgres
source /opt/.pgsqlcreds

createuser --interactive --pwprompt
$pgsqluid
$pgsqlpwd
$pgsqlpwd
yes

sudo rm /opt/.pgsqlcreds

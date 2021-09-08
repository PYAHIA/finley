
import sys
import os

if os.name == 'nt':
     sys.path.append(r"C:/Users/pyahia/git/finley/modules")
else:
    sys.path.append( r"opt/airflow/modules")
    


from update_dependencies import update_dependencies
from finley_connection import AirConn

class TaskCompiler:
    
    def __init__(self, procedure_name):
        self.procedure_name=procedure_name.replace("\\","/")
        self.conn = AirConn() 
        
    def build(self):
        sql = "SELECT ID FROM finley.t_procedures WHERE procedure_name = '%s'" % (self.procedure_name)
        res, err = self.conn.execute(sql)
        if err:
            raise Exception(err)
        if res:
            self.procedure_id = res[0][0]
        else:
            sql = "INSERT INTO finley.t_procedures (procedure_name) VALUES('%s') RETURNING ID " % (self.procedure_name)  
            res, err = self.conn.execute(sql)
            self.procedure_id = res[0][0]
            res, err = self.conn.execute("COMMIT;")
        update_dependencies(self.procedure_id)
            
        self.procedure_id = int(self.procedure_id)


    def assign_server(self, server_id): #add handling is already exists
        sql = "SELECT procedure_server_id FROM finley.t_procedure_server WHERE procedure_id = %d and server_id = %d" % (self.procedure_id, server_id)      
        res, err = self.conn.execute(sql)
        if res:
            self.procedure_server_id = res[0][0]
            print("testing...", self.procedure_id)
            return
    
        sql = "INSERT INTO finley.t_procedure_server (procedure_id, server_id) VALUES(%d,%d) RETURNING ID " % (self.procedure_id, server_id)      
        res, err = self.conn.execute(sql)
        if err:
            raise err
        self.procedure_server_id = res[0][0]
        self.conn.execute("commit;")
        
    
    def assign_schedule(self, schedule_id):#add handling is already exists 
        sql = "SELECT 1 FROM finley.t_procedure_server_schedule WHERE procedure_server_id = %d and schedule_id = %d" % (self.procedure_server_id, schedule_id)      
        res, err = self.conn.execute(sql)
        if res:
            return
        
        sql = "INSERT INTO finley.tj_procedure_server_schedule (procedure_server_id, schedule_id) VALUES(%d,%d) RETURNING ID " % (self.procedure_server_id, schedule_id)  
        res, err = self.conn.execute(sql)
        if err:
            raise err
        self.procedure_server_schedule_id = res[0][0]
        self.conn.execute("commit;")

    def full_build(self, server_id, schedule_id):
        self.build()
        self.assign_server(server_id)
        self.assign_schedule(schedule_id)
        
        
        
def dev_cleanup():
    conn = AirConn()
    r,e = conn.execute("SELECT procedure_name from finley.t_procedures")
    files = [x[0] for x in r]
    root = r"c:/users/pyahia/git/finley/repos"
    dels = []
    for file in files:
        f = root+"/"+file
        if not os.path.isfile(f):
            dels.append(file)
    dels = ["'"+d+"'"for d in dels]
    s = ",".join(dels)
    _, e = conn.execute("DELETE FROM finley.t_procedures WHERE procedure_name in (%s)" % s)
    conn.close()
    
    
    
if __name__ == "__main__":
    for i in [1,2,3,4]:
        TaskCompiler(r'dvd-dw\misc\actor.sql').full_build(1,i)
        TaskCompiler(r'dvd-dw\film\film.sql').full_build(1,i)
        TaskCompiler(r'dvd-dw\film\film_pre.sql').full_build(1,i)
        TaskCompiler(r'dvd-dw\misc\inventory.sql').full_build(1,i)
        TaskCompiler(r'dvd-dw\store\store.sql').full_build(1,i)
        TaskCompiler(r'dvd-dw\store\store_pre.sql').full_build(1,i)
        
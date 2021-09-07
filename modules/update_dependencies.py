from parse_code import Procedure
from finley_connection import AirConn


def update_dependencies(procedure_id):
      ac = AirConn()
      proc = get_new_dependencies(procedure_id, ac)
      delete_sources_and_targets(procedure_id, ac)
      for source in proc.sources:
          src = source.lower()
          source_id = get_source_id(src, ac)
          sql = "INSERT INTO finley.tj_procedure_source (procedure_id, source_id) VALUES (%s, %s);" % (procedure_id, source_id)
          r,err = ac.execute(sql)
          ac.commit()
          if err:
              raise err
              
      for target in proc.targets:
          targ = target.replace('..', '.dbo.')
          targ =  targ.lower()
          target_id = get_target_id(targ, ac)
          ac.execute("INSERT INTO finley.tj_procedure_target (procedure_id, target_id) VALUES (%s, %s)" % (procedure_id, target_id))
          ac.commit()
      
def get_source_id(source_name, conn):
    res, err = conn.execute("SELECT id FROM finley.t_source_target WHERE table_name = '%s'" % (source_name))
    conn.commit()
    if res:
        return res[0][0]
    else:
        c, err = conn.execute("INSERT INTO finley.t_source_target (table_name) VALUES ('%s') RETURNING ID" % (source_name))
        conn.commit()
        return c[0][0]

def get_target_id(target_name, conn):
    res, err = conn.execute("SELECT id FROM finley.t_source_target WHERE table_name = '%s'" % (target_name))
   # print(err)
    if res:
        return res[0][0]
    else:
        c, e = conn.execute("INSERT INTO finley.t_source_target (table_name) VALUES ('%s') RETURNING ID" % (target_name))
        conn.commit()
        return c[0][0]
        
        
def delete_sources_and_targets(procedure_id, conn):
    conn.execute( "DELETE FROM finley.tj_procedure_target WHERE Procedure_ID = %s" % (procedure_id))
    conn.execute( "DELETE FROM finley.tj_procedure_source WHERE Procedure_ID = %s" % (procedure_id))
    
def get_new_dependencies(procedure_id, conn):
    sql = """
        SELECT procedure_name
        FROM finley.t_procedures
        WHERE ID = '%s' """ % (procedure_id)
    proc_name = conn.execute(sql)[0][0][0]
    return Procedure(proc_name)
    

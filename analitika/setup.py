import sql_agent as sql
import os
#create a data_base
sql_ag = sql.sql_data('test.db','test')
try:
    sql_ag.create_db()
except:
    print('The database is already created.')
